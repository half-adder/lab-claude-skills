# Buffer-Block Pattern

The core pattern that makes Buffers sheets work. Applied to every recipe.

## The two lookup tables at the top of a Buffers sheet

### 1. Stocks table

Three editable columns plus a formula display column:

| Stock (display, formula) | Conc | Unit | Chemical |
|---|---|---|---|
| `=IF(C8="%", B8&"% "&D8, B8&" "&C8&" "&D8)` | 1 | M | Tris-HCl pH 7.5 |
| ... | 10 | % | SDS |
| ... | 20 | mg/mL | Proteinase K |

Display formula handles the spacing rule: `%` has no space before it; `M` and `mg/mL` do.

Buffer rows reference column A (`=$A$8`, etc.) so changing Conc/Unit/Chemical on the stocks row updates the component name everywhere.

### 2. Unit-factor table

Two columns -- Unit, Factor. Used by VLOOKUP to convert between any unit and a base.

| Unit | Factor |
|---|---|
| M | 1 |
| mM | 0.001 |
| µM | 0.000001 |
| nM | 0.000000001 |
| % | 1 |
| mg/mL | 1 |
| µg/mL | 0.001 |

Factors are relative within a unit family. M, mM, µM, nM share a family (normalize to M). mg/mL and µg/mL share a family. % is its own. Don't mix families on the same component row -- nothing prevents it but the result is meaningless.

To extend: add a new row to the table. Nothing else changes.

## Buffer block layout

For each buffer, write a block with this shape:

```
Row r   : <Buffer name>: <composition string>             [block-fill, merged A:F]
Row r+1 : Per-IP volume    | <µL>  | µL    | <protocol step note>
Row r+2 : Total to prepare | =B*$IP$*$DV$/1000 | mL | =B*$IP$*$DV$ | µL
Row r+4 : Component        | Final val | Unit | Volume (µL) | (stock display)
Row r+5 : =$A$<stock_row>  | <val>     | <unit> | <volume formula> | =$A$<stock_row>
Row r+6 : ... more components
Row r+k : ddH2O (balance)  |           |        | =total_ul - SUM(component vols)
Row r+k+1: TOTAL (sanity check) |      |        | =SUM(...) | should equal D<r+2>
```

### Volume formula

```
= total_ul * (final_val * factor(final_unit)) / (stock_conc * factor(stock_unit))
```

Where `factor(...)` is `IFERROR(VLOOKUP(unit_cell, $units_range, 2, FALSE), 1)`. Fallback to 1 prevents broken cells if a user enters an unknown unit.

### Water balance row

Always last component before the sanity check. Formula:

```
= total_ul - SUM(<first_component_vol_row> : <last_component_vol_row>)
```

The water row is *always* the balance, never a fixed value, so rounding and stock changes stay self-consistent.

### Sanity check row

```
A: "TOTAL (sanity check)"  (italic)
D: =SUM(<all component rows including water>)
E: "should equal D<total_to_prepare_row>"   <-- plain text, no leading =
```

If the sanity check ever differs from the total-to-prepare cell, a unit conversion is broken.

## Per-sample mixes (no water balance)

Some "buffers" are per-sample mastermixes (e.g. tagmentation reaction = 10 µL water + 10 µL 2x buffer + 1 µL Tn5). Use a different block shape:

```
Row r   : <Mix name>: <recipe>                  [block-fill, merged A:F]
Row r+1 : Per-IP volume    | 21    | µL
Row r+2 : Total to prepare | =B*$IP$*$DV$/1000 | mL | =B*$IP$*$DV$ | µL
Row r+4 : Component | µL/sample | Total µL | Notes
Row r+5 : Ultra-clean water | 10 | =10*$IP$*$DV$ | ...
Row r+6 : 2x buffer         | 10 | =10*$IP$*$DV$ | ...
Row r+7 : enzyme            | 1  | =1*$IP$*$DV$  | ...
```

No stock-component lookup; no water balance.

## Reagents added at the bench (not premixed)

Some reagents are added directly into per-sample tubes at the bench (e.g. Proteinase K into elution buffer, step 20 of ChIP-Tn5 Day 2). Do NOT include them as components of a buffer. Make a separate small block:

```
Row r   : <Reagent> (added separately at bench, step N)   [block-fill]
Row r+1 : Per-IP volume    | 5    | µL  | ="<stock display>"&" directly into each tube"
Row r+2 : Total to aliquot | =5*$IP$*$DV$ | µL of <stock display> stock
```

## Worked example

The canonical implementation lives in:

```
/Users/sean/Documents/Obsidian/McKay Lab Notebook/3. Resources/Protocols/Genomics/ChIP-Tn5/ChIP-Tn5 Experiment Calculator.xlsx
```

See the `Day 2 Buffers` sheet. Six blocks: tagmentation wash buffer, tagmentation reaction mix, wash buffer I, wash buffer II, wash buffer IV (TE), elution buffer + ProtK.
