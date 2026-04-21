# Workflow: Derive a Bench-Ready Sheet

<required_reading>
1. `references/workbook-conventions.md`
2. `references/bench-vs-planning.md`
3. `scripts/workbook_helpers.py`
</required_reading>

<process>

## Step 1: Gather inputs

Ask for:
1. **Path to the workbook**.
2. **Source sheet name** (the planning sheet to strip, e.g. `Day 2 Buffers`).
3. **Target sheet name** (default: source name with "Buffers" replaced by "Bench").

If the target sheet already exists, ask whether to overwrite. Default no.

## Step 2: Inspect the source sheet

Load the workbook, read the source sheet structure:

- Identify each buffer block: title row, total-to-prepare cell, component rows, water balance row.
- Identify any per-sample mastermix blocks and bench-add blocks.
- Identify the per-sample table on the linked `Samples` sheet (the user actually pipettes from this).

Don't read the values; just learn the cell addresses you need to reference.

## Step 3: Plan the bench layout

Per `references/bench-vs-planning.md`:

- One block per buffer. Title + total-to-prepare + component name + volume (µL only). Drop Final/Unit columns. Drop sanity check.
- Per-sample table: only bench-relevant columns (sample #, label, pool, antibody, µL antibody, µL sonicate to pull, µL refill RIPA+ -- whatever applies).
- Order blocks in protocol step order, not alphabetical.

## Step 4: Backup and generate

```bash
cp "$WORKBOOK" "/tmp/$(basename "$WORKBOOK" .xlsx)-backup-$(date +%s).xlsx"
```

Write a script that:
1. Loads the workbook.
2. Deletes the target sheet if present.
3. Creates the target sheet.
4. Writes block titles and component name cells as **formula references** to the source sheet (e.g. `='Day 2 Buffers'!A20`).
5. Writes volume cells the same way (`='Day 2 Buffers'!D24`).
6. Sets larger column widths (A=50, others 16+) and a base font size of 12 for readability.
7. Saves with `save_with_full_calc()`.

## Step 5: Verify

Open the workbook, check:
- Bench sheet has only the relevant columns.
- Cells contain formulas, not literal values.
- Changing the source sheet propagates to the bench sheet on next recalc.

Tell user:
- Bench sheet path inside the workbook.
- Reminder: changes to the source planning sheet automatically update the bench view.

</process>

<success_criteria>
- New bench sheet exists with the agreed name.
- Every value cell on the bench sheet is a formula reference, not a copied value.
- Stocks table, unit-factor table, sanity checks, dead-volume cell, # IPs cell all absent from the bench sheet.
- Layout follows protocol step order.
- Backup written to /tmp.
</success_criteria>
