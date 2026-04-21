# Bench vs Planning

A bench-ready sheet is meant to be printed, taped to the bench, and used while pipetting with gloves on. Strip everything that is only useful at the planning stage.

## What stays

For a buffer block:
- Buffer name and composition string (the title row).
- **Total volume to prepare**, in mL.
- Component table: name (display string), volume in µL.
- A "ddH2O (balance)" row with its computed volume.
- Brief protocol step note ("Step 17, 2 x 1 mL washes per IP").

For per-sample tables:
- Sample # | Label | Pool | Antibody | Dose (µg) | µL antibody | µL sonicate to pull | µL refill RIPA+
- Just the bench-relevant columns. Drop anything that's a planning intermediate.

## What gets dropped

- **Stocks table** -- by bench time the buffers are mixed; the stock concentrations are no longer relevant.
- **Unit-factor lookup table** -- internal plumbing.
- **Dead-volume factor cell** -- the totals already include it.
- **# IPs cell** -- the totals already include it.
- **TOTAL (sanity check) rows** -- planning-only.
- **Final val / Unit columns** -- the bench just needs the volume. The composition is already in the title row.
- **Pool definitions** -- planning intermediate. The bench only needs per-sample numbers.

## How values arrive on the bench sheet

Bench sheets contain **only formulas referencing the planning sheet**, never copy-pasted values. If a planning input changes the bench sheet updates automatically.

```
Bench cell:  ='Day 2 Buffers'!D24       <-- volume of Tris in Wash I
```

## Layout

- Larger font (size 12+) for at-a-glance reading.
- Wider columns -- assume the user is squinting through goggles.
- Blocks arranged in **the order the user touches them**, which is protocol order, not alphabetical.
- One blank row between blocks.
- Page-break before each new buffer if the workbook is set up for printing.

## What to do when planning and bench diverge

If a buffer composition changes during planning (e.g. user decides to use 20% SDS instead of 10%), the bench sheet picks it up automatically through the formulas. No manual sync. This is the whole reason for not copy-pasting values.
