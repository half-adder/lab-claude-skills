# Workflow: Create New Planner

<required_reading>
Before doing anything else, read:
1. `references/workbook-conventions.md`
2. `references/buffer-block-pattern.md`
3. `references/bench-vs-planning.md`
4. `scripts/workbook_helpers.py` (the docstring + function signatures)
</required_reading>

<process>

## Step 1: Gather inputs

Ask for:
1. **Path to the protocol PDF** (e.g. `3. Resources/Protocols/Genomics/<protocol>.pdf`).
2. **Where to save the workbook** (default: alongside the PDF, named `<protocol> Experiment Calculator.xlsx`).
3. **Sample structure**: how many samples, what dimensions vary (antibody, dose, genotype, stage, ...). Don't ask for individual sample values yet -- defaults are fine; user fills them in Excel.

## Step 2: Read the protocol

Read the PDF. Identify:
- **Days/phases** -- how many bench sessions, what each does.
- **Per-IP buffer volumes** for each day (e.g. "2 x 1 mL washes" -> 2000 µL per IP).
- **Buffer compositions** -- final concentrations of each component, plus identity of the stock.
- **Per-sample mastermixes** -- e.g. tagmentation reaction mix.
- **Bench-add reagents** -- things added to per-sample tubes, not premixed (e.g. Proteinase K).
- **Dead-volume needs** -- which buffers are pipetted in 1 mL aliquots multiple times (use 1.2x) vs. one-shot (1.1x).

If anything is unclear or ambiguous, ASK rather than guess. The protocol is the source of truth for per-IP volumes.

## Step 3: Confirm structure with user

Before generating, present:
- Sheet list: `Samples`, `Day 1 Buffers`, `Day 1 Bench`, `Day 2 Buffers`, `Day 2 Bench`, ...
- Per-day buffer list with per-IP volumes and dead-volume factors.
- Any non-obvious choices (e.g. "I'll put Proteinase K as a separate bench-add block, not as a component of the elution buffer").

Wait for confirmation before writing files.

## Step 4: Generate the workbook

Write a uv-script generator (see template below). Import from `scripts/workbook_helpers.py`. Use `save_with_full_calc()` at the end.

For each sheet:

- **Samples sheet** -- per-sample table (sample #, label, pool, antibody, dose, embryos, ...). Provide ~20 sample rows by default. Add per-pool derived table if pools are used. The `# IPs` is `=COUNTA(B20:B39)` (count of filled labels), used by every Buffers sheet.

- **Day N Buffers sheet** -- title, dead-volume cell, `# IPs` formula referencing `Samples`, stocks table, unit-factor table (call `write_unit_factor_table`), then one `buffer_block()` per recipe. Use `per_sample_mix_block()` for mastermixes and `bench_add_block()` for bench-add reagents.

- **Day N Bench sheet** -- formulas-only references back to Day N Buffers and Samples. Strip per `references/bench-vs-planning.md`. No stocks table, no unit-factor table, no sanity checks, no Final/Unit columns.

## Step 5: Backup any existing file at the output path

If the output path already exists:
```bash
cp "$OUT" "/tmp/$(basename "$OUT" .xlsx)-backup-$(date +%s).xlsx"
```
Tell the user the backup path before overwriting.

## Step 6: Run the generator

```bash
uv run /tmp/build_<protocol>_planner.py
```

## Step 7: Verify

Re-open with openpyxl and check:
- All expected sheet names exist.
- No `#REF` strings in any formula cell.
- Per-IP volume cells contain the values you intended.

Tell the user:
- Path to the saved workbook.
- Path to the backup (if any).
- A one-line spot-check: with N samples filled, total of largest buffer should be ~X mL.
- Note about the `--` to `,` em-dash rule if any buffer-name compositions came from the protocol verbatim.

## Generator script template

Save as `/tmp/build_<protocol>_planner.py`:

```python
# /// script
# dependencies = ["openpyxl"]
# ///
import sys
sys.path.insert(0, "/Users/sean/code/lab-claude-skills/protocol-planner/scripts")

from openpyxl import Workbook
from workbook_helpers import (
    put, write_stocks_table, write_unit_factor_table,
    buffer_block, per_sample_mix_block, bench_add_block,
    save_with_full_calc, STYLES,
)

OUT = "<absolute path to output xlsx>"

wb = Workbook()

# --- Samples sheet ---
ws = wb.active
ws.title = "Samples"
# ... write per-sample table headers, default rows, per-pool table, etc.

# --- Day 1 Buffers ---
ws = wb.create_sheet("Day 1 Buffers")
put(ws, "A1", "<Protocol> Day 1 Buffer Calculator", STYLES.H1)
put(ws, "A3", "Dead-volume factor", STYLES.BOLD)
put(ws, "B3", 1.1)
put(ws, "A4", "# IPs (from Samples)", STYLES.BOLD)
put(ws, "B4", "=COUNTA('Samples'!B20:B39)")

stocks = [
    ("tris80", 1, "M", "Tris-HCl pH 8.0"),
    # ...
]
stock_row = write_stocks_table(ws, start_row=8, stocks=stocks)
units_range = write_unit_factor_table(ws, anchor_cell="F7")

next_row = 20
next_row = buffer_block(
    ws, next_row,
    title="RIPA+: 1x RIPA + protease inhibitors + DTT",
    per_ip_ul=700,
    per_ip_note="700 µL per sample (Day 1 step 3)",
    components=[
        ("tris80", 50, "mM"),
        # ...
    ],
    stock_row=stock_row,
    units_range=units_range,
)

# --- Day 1 Bench ---
ws = wb.create_sheet("Day 1 Bench")
# Stripped, formulas-only references back to Day 1 Buffers and Samples.

# ... (Day 2 Buffers, Day 2 Bench, ...)

save_with_full_calc(wb, OUT)
print(f"Saved {OUT}; sheets: {wb.sheetnames}")
```

</process>

<success_criteria>
- Output workbook exists at the agreed path.
- Backup of any prior file at `/tmp/...-backup-*.xlsx`.
- All planning sheets have stocks table, unit-factor table, dead-volume cell, # IPs formula.
- All buffer blocks have a sanity-check row whose formula equals the total-to-prepare cell when opened in Excel.
- Bench sheets contain only formula references back to planning sheets, no copy-pasted values.
- Workbook opens in Excel with computed values visible immediately (no click-to-render).
- User has been told the spot-check value to verify in Excel.
</success_criteria>
