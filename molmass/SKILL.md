---
name: molmass
description: Compute molecular weight from a chemical formula via the molmass CLI. Use whenever a lab calculation needs an MW (buffer recipes, dilutions, stoichiometry, peptide mass, mg/mL to molarity). Supports empirical formulas, isotopes, and 1-letter peptides. Does NOT resolve common names (Tris, DTT, PMSF, HEPES) — needs the actual formula.
---

<objective>
Look up molecular weight from a chemical formula with the `molmass` CLI and use the result in a downstream lab calculation.
</objective>

<quick_start>
```bash
molmass "CH3(CH2)2OH" | grep -E "Hill notation|Average mass"
```

Default pattern: **pipe to `grep` to filter out noise.** The full molmass output includes a nominal mass, monoisotopic mass, elemental composition breakdown, and a multi-line isotope distribution table — none of that is relevant for bench calculations and all of it wastes context.

For most lab calculations, grab the **Average mass** line (natural isotopic abundance — matches what's on the bottle). Use **Monoisotopic mass** only for MS work. `Hill notation` confirms the input parsed as intended.

Install (if missing): `uv tool install molmass`
</quick_start>

<when_to_use>
Trigger this skill whenever the next step of a calculation needs a molecular weight AND the formula is known. Examples:

- "How much NaCl do I need for 500 mL of 1 M?" → run `molmass "NaCl" | grep "Average mass"`, use that value
- Converting a stock's mg/mL to molarity
- Computing peptide mass for synthesis / MS
- Stoichiometry on a small molecule whose MW isn't already in hand

Do NOT use this skill when:
- The user has already provided an MW
- Only a trade/common name is available (Tris, DTT, PMSF, HEPES, Triton X-100) — molmass errors on these. Look up the formula from the vendor page or protocol, then run molmass.
- The target is a full protein / complex mixture where the "molecular weight" is empirical (e.g., BSA stock, antibody stock) — use the vendor's reported value.
</when_to_use>

<usage>

Input forms molmass accepts (always pipe to `grep` — see quick_start):

```bash
molmass "CH3(CH2)2OH" | grep "Average mass"       # empirical formula, parens OK
molmass "C6H12O6" | grep "Average mass"           # glucose
molmass "Na2HPO4" | grep "Average mass"           # disodium phosphate
molmass "(NH4)2SO4" | grep "Average mass"         # ammonium sulfate
molmass "CaCl2(H2O)2" | grep "Average mass"       # hydrate — write waters explicitly
molmass "[13C]C5H12O6" | grep "Average mass"      # isotope-labeled
molmass "peptide(ACDEFGHIK)" | grep "Average mass" # peptide, 1-letter codes
```

Include Hill notation when you want to confirm the formula parsed as intended (helpful for hydrates, parenthesized groups, or any formula you're typing for the first time):

```bash
molmass "Na2HPO4(H2O)7" | grep -E "Hill notation|Average mass"
```

**Batch pattern (multiple formulas).** molmass does NOT accept multiple formulas as separate positional arguments — it concatenates them into a single formula. Use a shell loop instead:

```bash
for f in "NaH2PO4(H2O)" "Na2HPO4(H2O)7" "NaCl"; do
  echo -n "$f: "
  molmass "$f" | grep "Average mass"
done
```

**When you actually need the full output** (e.g. debugging a formula that won't parse, or inspecting the isotope distribution for MS work), run `molmass "X"` without the pipe. This should be rare for bench calculations.
</usage>

<anti_patterns>
<pitfall name="common-names">
molmass errors on `Tris`, `DTT`, `PMSF`, `EDTA`, `HEPES`, etc. It parses formulas, not names. Look up the formula first (Tris = C4H11NO3) and retry.
</pitfall>

<pitfall name="hydrates-with-dots">
Write hydrates as `CaCl2(H2O)2`, not `CaCl2·2H2O` or `CaCl2.2H2O`. The dot notation is not parsed.
</pitfall>

<pitfall name="dumping-output">
Don't paste the full molmass output into a lab note, a conversation response, or a tool result. Pipe to `grep "Average mass"` (or `grep -E "Hill notation|Average mass"`) so only the relevant line(s) come back. The isotope distribution and elemental composition tables are noise for bench work. Record the formula and the MW used, e.g. `CaCl2(H2O)2, MW 147.01 g/mol`.
</pitfall>

<pitfall name="multiple-args-concatenate">
`molmass "A" "B" "C"` does NOT compute each formula separately. molmass concatenates all positional arguments into one combined formula and returns a single MW for that combined formula. To compute MWs for multiple reagents, use a shell `for` loop (see Batch pattern in usage).
</pitfall>

<pitfall name="wrong-mass-mode">
Default to **Average mass** for weighing out reagents — reagent bottles are natural-abundance. Monoisotopic mass is for interpreting MS spectra, not for calculating how many milligrams to weigh.
</pitfall>
</anti_patterns>

<success_criteria>
- molmass invoked with a valid formula or peptide sequence
- Correct mass variant selected (average for bench, monoisotopic for MS)
- MW used in the downstream calculation with units preserved (g/mol)
- When written into a lab note: formula and MW recorded together, not the full CLI dump
</success_criteria>
