# Workflow: Add a Day to an Existing Planner

<required_reading>
1. `references/workbook-conventions.md`
2. `references/buffer-block-pattern.md`
3. `references/bench-vs-planning.md`
4. `scripts/workbook_helpers.py`
</required_reading>

<process>

## Step 1: Gather inputs

Ask for:
1. **Path to the existing planner workbook**.
2. **Which day to add** (e.g. "Day 3"). Default to the next unused number.
3. **Path to the protocol PDF** (or relevant section/page range).

## Step 2: Inspect the existing workbook

```python
from openpyxl import load_workbook
wb = load_workbook(path)
print(wb.sheetnames)
```

Confirm:
- A `Samples` sheet exists with the standard `# IPs` source range.
- The new day name doesn't already exist (`Day N Buffers`, `Day N Bench`).

If the workbook was hand-edited and doesn't follow conventions, ask the user how to proceed rather than overwriting silently.

## Step 3: Read the protocol day

Read just the relevant section of the PDF. Identify the same things as in `create-planner.md` Step 2: per-IP volumes, compositions, mastermixes, bench-add reagents, dead-volume class.

## Step 4: Confirm with user

List the new buffer blocks and their per-IP volumes. Wait for confirmation.

## Step 5: Backup

```bash
cp "$WORKBOOK" "/tmp/$(basename "$WORKBOOK" .xlsx)-backup-$(date +%s).xlsx"
```

## Step 6: Generate

Write a script that loads the existing workbook, deletes the target day's sheets if present (so the operation is idempotent), creates `Day N Buffers` and `Day N Bench`, and saves with `save_with_full_calc()`.

```python
# /// script
# dependencies = ["openpyxl"]
# ///
import sys
sys.path.insert(0, "/Users/sean/code/lab-claude-skills/protocol-planner/scripts")
from openpyxl import load_workbook
from workbook_helpers import (
    put, write_stocks_table, write_unit_factor_table,
    buffer_block, per_sample_mix_block, bench_add_block,
    save_with_full_calc, STYLES,
)

WB_PATH = "<absolute path>"
DAY = "Day 3"

wb = load_workbook(WB_PATH)
for sheet in [f"{DAY} Buffers", f"{DAY} Bench"]:
    if sheet in wb.sheetnames:
        del wb[sheet]

# Build the new sheets here using the same patterns as create-planner.

save_with_full_calc(wb, WB_PATH)
```

## Step 7: Verify

Reload, check sheet list, scan formulas for `#REF`. Tell user the path and any spot-check value.

</process>

<success_criteria>
- New `Day N Buffers` and `Day N Bench` sheets exist.
- Existing sheets unchanged.
- Backup written to /tmp.
- # IPs formula on the new buffers sheet references `Samples`, not a hardcoded number.
- No `#REF` errors.
</success_criteria>
