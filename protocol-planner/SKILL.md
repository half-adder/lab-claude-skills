---
name: protocol-planner
description: Build linked Excel workbooks that plan an experiment from a protocol PDF. Produces a Samples sheet, one Buffers sheet per protocol day (with dynamic unit-aware recipes), and bench-ready sheets stripped of planning clutter. Use when starting a new protocol, adding a day to an existing planner, or producing a bench-ready printout from a planning sheet.
---

<essential_principles>

**The artifact is one workbook with linked sheets.**

A finished planner has, at minimum:

- `Samples` -- per-sample inputs (label, pool, antibody, dose, embryos) and per-pool derived quantities (sonication volumes, # IPs, totals).
- `Day N Buffers` -- one per protocol phase. Each buffer block computes total volume from #IPs (looked up from `Samples`) and breaks it into stock components.
- `Day N Bench` -- a stripped, printable view of `Day N Buffers` and the relevant per-sample table. No planning controls, no sanity checks.

Sheets reference each other by formula. Never copy-paste values across sheets.

**Volumes are derived, not typed.**

Per-IP volumes come from the protocol. Total volumes are always `per_IP * #IPs * dead_volume_factor`. Component volumes use the unit-factor lookup pattern (see `references/buffer-block-pattern.md`) so changing a stock concentration or unit recomputes everything.

**Two dead-volume defaults:**
- `1.1x` for one-shot pipetting (RIPA+, master mixes).
- `1.2x` for buffers pipetted in 1 mL aliquots multiple times (wash buffers).

Each Buffers sheet has its own dead-volume cell; do not share across sheets.

**Always set `fullCalcOnLoad=True`** on the workbook before saving, or formulas can render blank in Excel until clicked. Use `scripts/workbook_helpers.py:save_with_full_calc()`.

**Writing style:**
- No em dashes anywhere -- use a colon, comma, or period.
- No emoji in cell values.
- Cell text starting with `=` becomes a formula. Sanity-check labels like "should equal D22" must NOT start with `=`.

**Source the per-IP volumes from the protocol.**

Read the protocol PDF before guessing. The user may reference protocols in `3. Resources/Protocols/` of their lab notebook. If a per-IP volume or composition is unclear, ask -- do not invent.

</essential_principles>

<intake>
What would you like to do?

1. **New planner** -- build Samples + Buffers + Bench sheets from a protocol PDF
2. **Add a day** -- add a new Day N Buffers + Bench sheet to an existing planner
3. **Derive bench sheet** -- strip an existing planning sheet to a bench-ready view

**Wait for response before proceeding.**
</intake>

<routing>
| Response | Workflow |
|----------|----------|
| 1, "new", "create", "build", "from scratch" | `workflows/create-planner.md` |
| 2, "add", "day", "extend", "another buffer sheet" | `workflows/add-buffer-day.md` |
| 3, "bench", "strip", "printable", "derive" | `workflows/derive-bench-sheet.md` |

**After reading the workflow, follow it exactly.**
</routing>

<reference_index>
**Workbook conventions:** `references/workbook-conventions.md` -- sheet naming, dead-volume defaults, calcProperties, writing style.
**Buffer-block pattern:** `references/buffer-block-pattern.md` -- stocks table, unit-factor lookup, dynamic stock-name display, water balance, sanity check.
**Bench vs planning:** `references/bench-vs-planning.md` -- what stays, what gets dropped when producing a bench-ready sheet.
</reference_index>

<workflows_index>
| Workflow | Purpose |
|----------|---------|
| create-planner.md | Read protocol PDF, gather sample structure, build full workbook |
| add-buffer-day.md | Add a new Day N Buffers + Day N Bench pair to an existing workbook |
| derive-bench-sheet.md | Produce a stripped, printable bench view of an existing planning sheet |
</workflows_index>

<helper_script>
All workflows import `scripts/workbook_helpers.py`. It exposes:

- `put(ws, cell, value, ...)` -- write with optional font/fill/format.
- `unit_factor_expr(unit_cell, units_range)` -- generates the VLOOKUP-with-IFERROR formula.
- `write_stocks_table(ws, start_row, stocks)` -- writes the editable Conc/Unit/Chemical table with formula display name.
- `write_unit_factor_table(ws, anchor_cell)` -- writes the unit -> factor lookup. Returns the range string.
- `buffer_block(ws, start_row, ...)` -- writes one full buffer block (per-IP, total, components, water balance, sanity check).
- `save_with_full_calc(wb, path)` -- sets `CalcProperties(fullCalcOnLoad=True)` then saves.

Run all scripts with `uv run` (the helper module is uv-script compatible).
</helper_script>
