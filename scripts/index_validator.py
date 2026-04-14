#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""
index_validator.py -- check Illumina index pools for Hamming distance and color balance.

Two modes:

  validate   Given a specific per-sample (i5, i7) assignment, report Hamming
             distances and color balance per cycle.

  optimize   Given a pool of candidate indexes, enumerate all subsets of a given
             size and return the top-K ranked by color balance.

Input formats:

  validate:  CSV with columns `sample,i5,i7` (one row per library).
  optimize:  CSV with columns `id,sequence` (one row per candidate primer).

Usage:

  uv run index_validator.py validate pool.csv [--chemistry 2ch|4ch]
  uv run index_validator.py optimize candidates.csv --pick 6 [--top 5] [--chemistry 2ch|4ch] [--min-hamming 2]

Example:

  # Pool sheet: sample,i5,i7 ...
  uv run index_validator.py validate my_pool.csv --chemistry 2ch

  # 15 i7 candidates; pick the best 6 for 2-channel NextSeq 2000:
  uv run index_validator.py optimize i7_candidates.csv --pick 6 --top 5 --chemistry 2ch
"""
from __future__ import annotations

import argparse
import csv
import sys
from collections import Counter
from dataclasses import dataclass
from itertools import combinations
from pathlib import Path


# --- Color balance ----------------------------------------------------------

# 2-channel chemistry (NextSeq 500/550/2000, NovaSeq):
#   A = green only
#   C = red only
#   T = both
#   G = dark
# 4-channel chemistry (MiSeq, HiSeq 2500):
#   A = green, C = red, G = blue, T = yellow (one color per base).


def cycle_channels_2ch(bases_at_cycle: list[str]) -> dict[str, float]:
    """Return {green, red, dark} fractions across the cluster population at one
    cycle on 2-channel chemistry.
    """
    n = len(bases_at_cycle)
    if n == 0:
        return {"green": 0.0, "red": 0.0, "dark": 0.0}
    c = Counter(bases_at_cycle)
    green = (c.get("A", 0) + c.get("T", 0)) / n
    red = (c.get("C", 0) + c.get("T", 0)) / n
    dark = c.get("G", 0) / n
    return {"green": green, "red": red, "dark": dark}


def cycle_base_fractions(bases_at_cycle: list[str]) -> dict[str, float]:
    """Return {A,C,G,T} fractions for 4-channel color-balance analysis."""
    n = len(bases_at_cycle)
    if n == 0:
        return {"A": 0.0, "C": 0.0, "G": 0.0, "T": 0.0}
    c = Counter(bases_at_cycle)
    return {b: c.get(b, 0) / n for b in "ACGT"}


def per_cycle_report(
    indexes: list[str],
    chemistry: str,
    weights: list[int] | None = None,
) -> list[dict]:
    """For a list of index strings (weighted optional), return per-cycle stats.

    Each row is a dict with:
      - cycle (1-indexed)
      - bases: ordered string of each contributing base at this cycle
      - 2ch: {green, red, dark} fractions
      - 4ch: {A, C, G, T} fractions
      - min_signal_2ch: min(green, red) as a proxy for 2-channel weakness
      - max_base_4ch: max(A, C, G, T) as a proxy for 4-channel dominance
    """
    if not indexes:
        return []
    L = len(indexes[0])
    if not all(len(i) == L for i in indexes):
        raise ValueError("All indexes must be the same length")

    # Expand by weights (use integer weights so equimolar = weight 1).
    if weights is None:
        weights = [1] * len(indexes)
    expanded: list[str] = []
    for idx, w in zip(indexes, weights):
        expanded.extend([idx] * w)

    rows = []
    for c in range(L):
        bases = [seq[c] for seq in expanded]
        rec = {
            "cycle": c + 1,
            "bases": "".join(bases),
            "2ch": cycle_channels_2ch(bases),
            "4ch": cycle_base_fractions(bases),
        }
        rec["min_signal_2ch"] = min(rec["2ch"]["green"], rec["2ch"]["red"])
        rec["max_base_4ch"] = max(rec["4ch"].values())
        rows.append(rec)
    return rows


# --- Hamming ----------------------------------------------------------------

def hamming(a: str, b: str) -> int:
    if len(a) != len(b):
        raise ValueError(f"Length mismatch: {a!r} vs {b!r}")
    return sum(x != y for x, y in zip(a, b))


def pairwise_hamming(seqs: list[str]) -> list[tuple[int, int, int]]:
    """Return list of (i, j, distance) for every unordered pair i<j."""
    return [(i, j, hamming(seqs[i], seqs[j])) for i, j in combinations(range(len(seqs)), 2)]


# --- Scoring ----------------------------------------------------------------

def score_2ch(indexes: list[str], weights: list[int] | None = None) -> float:
    """Higher is better.  Min-of-mins: across all cycles, what is the weaker
    channel's signal?  Fraction in [0, 0.5].  0.5 is perfect balance, 0 means
    one channel is completely dark at some cycle.
    """
    rows = per_cycle_report(indexes, "2ch", weights)
    return min(r["min_signal_2ch"] for r in rows)


def score_4ch(indexes: list[str], weights: list[int] | None = None) -> float:
    """Higher is better.  1 - max single-base dominance.  1 is perfect, 0 means
    every cluster has the same base at some cycle.
    """
    rows = per_cycle_report(indexes, "4ch", weights)
    return 1.0 - max(r["max_base_4ch"] for r in rows)


def verdict_2ch(min_signal: float) -> str:
    # Rough thresholds inspired by Illumina's low-plex guidance (~15% per channel).
    if min_signal >= 0.30:
        return "PASS"
    if min_signal >= 0.15:
        return "WARN"
    if min_signal > 0:
        return "FAIL (one channel <15%)"
    return "FAIL (zero channel cycle)"


def verdict_4ch(max_base: float) -> str:
    if max_base <= 0.60:
        return "PASS"
    if max_base <= 0.80:
        return "WARN"
    return "FAIL (single base dominates)"


# --- Input parsing ---------------------------------------------------------

@dataclass
class ValidateRow:
    sample: str
    i5: str
    i7: str


def read_validate_csv(path: Path) -> list[ValidateRow]:
    rows = []
    with path.open() as f:
        reader = csv.DictReader(f)
        required = {"sample", "i5", "i7"}
        if not required.issubset(reader.fieldnames or []):
            raise SystemExit(f"validate CSV needs columns {sorted(required)}; got {reader.fieldnames}")
        for r in reader:
            rows.append(ValidateRow(sample=r["sample"].strip(), i5=r["i5"].strip(), i7=r["i7"].strip()))
    return rows


def read_candidates_csv(path: Path) -> list[tuple[str, str]]:
    """Return list of (id, sequence) pairs."""
    items = []
    with path.open() as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames or "sequence" not in reader.fieldnames:
            raise SystemExit("candidates CSV needs a `sequence` column (optional `id`)")
        for r in reader:
            seq = r["sequence"].strip().upper()
            ident = r.get("id", "").strip() or seq
            items.append((ident, seq))
    return items


# --- Report printing -------------------------------------------------------

def print_hamming(title: str, seqs_with_ids: list[tuple[str, str]]) -> int:
    """Print pairwise Hamming table; return min distance."""
    print(f"\n{title}")
    if len(seqs_with_ids) < 2:
        print("  (fewer than 2 sequences; skipping)")
        return 999
    dists = []
    for (ida, sa), (idb, sb) in combinations(seqs_with_ids, 2):
        d = hamming(sa, sb)
        dists.append(d)
        print(f"  {ida:20s} {sa}  vs  {idb:20s} {sb}   H={d}")
    min_d = min(dists)
    verdict = "PASS" if min_d >= 2 else "FAIL (Hamming <2)"
    print(f"  Min Hamming distance: {min_d}   [{verdict}]")
    return min_d


def print_color_balance(title: str, indexes: list[str], chemistry: str, weights: list[int] | None = None) -> None:
    print(f"\n{title}")
    if not indexes:
        print("  (empty pool)")
        return
    rows = per_cycle_report(indexes, chemistry, weights)
    if chemistry == "2ch":
        print(f"  {'cycle':>5} {'bases':<12} {'green%':>7} {'red%':>7} {'dark%':>7}  verdict")
        for r in rows:
            g = r["2ch"]["green"] * 100
            rd = r["2ch"]["red"] * 100
            dk = r["2ch"]["dark"] * 100
            weak = min(g, rd)
            v = "FAIL" if weak < 15 else ("WARN" if weak < 30 else "")
            print(f"  {r['cycle']:>5} {r['bases']:<12} {g:>7.1f} {rd:>7.1f} {dk:>7.1f}  {v}")
        overall = score_2ch(indexes, weights)
        print(f"\n  Min weak-channel signal across cycles: {overall*100:.1f}%   [{verdict_2ch(overall)}]")
    else:
        print(f"  {'cycle':>5} {'bases':<12} {'A%':>6} {'C%':>6} {'G%':>6} {'T%':>6}  verdict")
        for r in rows:
            fr = r["4ch"]
            vmax = max(fr.values())
            v = "FAIL" if vmax > 0.80 else ("WARN" if vmax > 0.60 else "")
            print(f"  {r['cycle']:>5} {r['bases']:<12} "
                  f"{fr['A']*100:>6.1f} {fr['C']*100:>6.1f} {fr['G']*100:>6.1f} {fr['T']*100:>6.1f}  {v}")
        overall = score_4ch(indexes, weights)
        print(f"\n  Max single-base fraction (lower=better): {(1-overall)*100:.1f}%   [{verdict_4ch(1-overall)}]")


# --- Commands -------------------------------------------------------------

def cmd_validate(args: argparse.Namespace) -> int:
    rows = read_validate_csv(Path(args.csv))
    print(f"=== Validate mode: {len(rows)} libraries, {args.chemistry} chemistry ===")
    for r in rows:
        print(f"  {r.sample:20s}  i5={r.i5}  i7={r.i7}")

    # Per-read Hamming analysis (i5s and i7s separately, only unique values).
    i5_unique = []
    seen = set()
    for r in rows:
        if r.i5 not in seen:
            i5_unique.append((r.sample + "_i5", r.i5))
            seen.add(r.i5)
    i7_unique = []
    seen = set()
    for r in rows:
        if r.i7 not in seen:
            i7_unique.append((r.sample + "_i7", r.i7))
            seen.add(r.i7)

    print_hamming("i5 pairwise Hamming distances", i5_unique)
    print_hamming("i7 pairwise Hamming distances", i7_unique)

    # Color balance: every library contributes one cluster-population unit at
    # each position, so count duplicates explicitly.
    i5_seqs = [r.i5 for r in rows]
    i7_seqs = [r.i7 for r in rows]

    print_color_balance(f"i5 color balance (n={len(rows)}, {args.chemistry})", i5_seqs, args.chemistry)
    print_color_balance(f"i7 color balance (n={len(rows)}, {args.chemistry})", i7_seqs, args.chemistry)

    return 0


def cmd_optimize(args: argparse.Namespace) -> int:
    candidates = read_candidates_csv(Path(args.csv))
    n = args.pick
    if n > len(candidates):
        raise SystemExit(f"Cannot pick {n} from {len(candidates)} candidates")
    print(f"=== Optimize mode: picking {n} of {len(candidates)} candidates, {args.chemistry} chemistry ===")

    ids = [c[0] for c in candidates]
    seqs = [c[1] for c in candidates]

    scored: list[tuple[float, tuple[int, ...], int]] = []
    total = 0
    kept = 0
    for subset in combinations(range(len(candidates)), n):
        total += 1
        subseqs = [seqs[i] for i in subset]
        # Hamming filter
        min_h = min(hamming(a, b) for a, b in combinations(subseqs, 2))
        if min_h < args.min_hamming:
            continue
        kept += 1
        score = score_2ch(subseqs) if args.chemistry == "2ch" else score_4ch(subseqs)
        scored.append((score, subset, min_h))

    scored.sort(key=lambda x: x[0], reverse=True)
    print(f"\nEnumerated {total} subsets, {kept} passed min-Hamming={args.min_hamming}")
    if not scored:
        print("No subsets meet the Hamming filter.")
        return 1

    top = scored[: args.top]
    for rank, (score, subset, min_h) in enumerate(top, start=1):
        print(f"\n--- Rank {rank}:  score={score*100:.1f}%  minH={min_h} ---")
        print("  " + ", ".join(f"{ids[i]} ({seqs[i]})" for i in subset))
        subseqs = [seqs[i] for i in subset]
        print_color_balance("  Color balance", subseqs, args.chemistry)

    return 0


# --- CLI -------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    v = sub.add_parser("validate", help="Validate a specific pool (CSV: sample,i5,i7)")
    v.add_argument("csv", help="Path to the pool CSV")
    v.add_argument("--chemistry", choices=["2ch", "4ch"], default="2ch")
    v.set_defaults(func=cmd_validate)

    o = sub.add_parser("optimize", help="Find best subset of a given size (CSV: id,sequence)")
    o.add_argument("csv", help="Path to the candidate CSV")
    o.add_argument("--pick", type=int, required=True, help="Number of indexes to pick")
    o.add_argument("--top", type=int, default=5, help="Number of top subsets to print")
    o.add_argument("--chemistry", choices=["2ch", "4ch"], default="2ch")
    o.add_argument("--min-hamming", type=int, default=2, help="Min pairwise Hamming distance")
    o.set_defaults(func=cmd_optimize)

    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
