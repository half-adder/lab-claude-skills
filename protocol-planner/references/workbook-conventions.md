# Workbook Conventions

## Sheet naming and order

Left to right:

1. `Samples` -- per-sample inputs and per-pool derived quantities. The single source of truth for #IPs.
2. `Day 1 Buffers`, `Day 2 Buffers`, ... -- one per protocol phase. Numbered to match the protocol.
3. `Day 1 Bench`, `Day 2 Bench`, ... -- bench-ready stripped views, one per planning day.

If a protocol has only one day, drop the "Day 1" prefix: `Buffers`, `Bench`.

## Global inputs (top of every sheet)

- **Title row** (row 1) -- bold, size 14.
- **Brief italic note** (row 2) -- one line on what the sheet derives and from where.
- **Dead-volume factor** (row 3) -- editable cell.
- **# IPs** (row 4) -- formula referencing `Samples` (e.g. `=COUNTA('Samples'!B20:B39)`).

Override behavior: the user can type over any derived cell. Comment in italic explains how.

## Dead-volume conventions

- `1.1x` -- one-shot pipetting (RIPA+, master mixes, anything aliquoted once).
- `1.2x` -- buffers pipetted in 1 mL aliquots multiple times (wash buffers I/II/IV, tagmentation wash).
- Per-buffer override is YAGNI unless asked for.

## CalcProperties

```python
from openpyxl.workbook.properties import CalcProperties
wb.calculation = CalcProperties(fullCalcOnLoad=True)
wb.save(path)
```

Without this, Excel sometimes opens the file with formula cells appearing blank until clicked. The `save_with_full_calc()` helper in `scripts/workbook_helpers.py` does this for you.

## Styling palette

- Header fill: `E8E8E8` (light gray)
- Block title fill: `F3F7FF` (very light blue)
- Italic comment color: `555555`
- Bold for all column headers and section titles.

Column widths default: A=46, B=12, C=12, D=14, E=34, F=12, G=12. Adjust per sheet.

## Writing style rules (non-negotiable)

- **No em dashes (--) in cell values.** Replace with a colon, comma, or period. The user explicitly disallows them.
- **No emoji** in cell values.
- **No leading `=` on label/comment cells** -- Excel parses them as formulas and shows `#NAME?`. If you want a label that begins with an equals, prefix with a single quote in the literal source value.
- **µ (Greek mu)**, not `u`, for microliters and micromolar. Always µL, µM.

## Backup before edit

Before modifying an existing workbook in place:

```bash
cp "$WORKBOOK" "/tmp/$(basename "$WORKBOOK" .xlsx)-backup-$(date +%s).xlsx"
```

Tell the user the backup path.
