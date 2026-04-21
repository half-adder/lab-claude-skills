---
name: molmass
description: Compute molecular weight from a chemical formula via the molmass CLI. Use whenever a lab calculation needs an MW (buffer recipes, dilutions, stoichiometry, peptide mass, mg/mL to molarity). Supports empirical formulas, isotopes, and 1-letter peptides. Does NOT resolve common names (Tris, DTT, PMSF, HEPES) — needs the actual formula.
---

<objective>
Look up molecular weight from a chemical formula with the `molmass` CLI and use the result in a downstream lab calculation.
</objective>

<quick_start>
```bash
molmass "CH3(CH2)2OH"
```

For most lab calculations, grab the **Average mass** line (natural isotopic abundance — matches what's on the bottle). Use **Monoisotopic mass** only for MS work.

Install (if missing): `uv tool install molmass`
</quick_start>

<when_to_use>
Trigger this skill whenever the next step of a calculation needs a molecular weight AND the formula is known. Examples:

- "How much NaCl do I need for 500 mL of 1 M?" → run `molmass "NaCl"`, use average mass
- Converting a stock's mg/mL to molarity
- Computing peptide mass for synthesis / MS
- Stoichiometry on a small molecule whose MW isn't already in hand

Do NOT use this skill when:
- The user has already provided an MW
- Only a trade/common name is available (Tris, DTT, PMSF, HEPES, Triton X-100) — molmass errors on these. Look up the formula from the vendor page or protocol, then run molmass.
- The target is a full protein / complex mixture where the "molecular weight" is empirical (e.g., BSA stock, antibody stock) — use the vendor's reported value.
</when_to_use>

<usage>

Input forms molmass accepts:

```bash
molmass "CH3(CH2)2OH"          # empirical formula, parens OK
molmass "C6H12O6"              # glucose
molmass "Na2HPO4"              # disodium phosphate
molmass "(NH4)2SO4"            # ammonium sulfate
molmass "CaCl2(H2O)2"          # hydrate — write waters explicitly
molmass "[13C]C5H12O6"         # isotope-labeled
molmass "peptide(ACDEFGHIK)"   # peptide, 1-letter codes
molmass "CH3OH" "C2H5OH"       # multiple formulas per call
```

Output (truncated) for `molmass "CH3(CH2)2OH"`:
```
Hill notation: C3H8O
Nominal mass: 60
Average mass: 60.095153
Monoisotopic mass: 60.057515 (96.500%)
```

Parsing: grab `Average mass` for bench calculations, `Monoisotopic mass` for MS, `Hill notation` to confirm the input parsed as intended.
</usage>

<anti_patterns>
<pitfall name="common-names">
molmass errors on `Tris`, `DTT`, `PMSF`, `EDTA`, `HEPES`, etc. It parses formulas, not names. Look up the formula first (Tris = C4H11NO3) and retry.
</pitfall>

<pitfall name="hydrates-with-dots">
Write hydrates as `CaCl2(H2O)2`, not `CaCl2·2H2O` or `CaCl2.2H2O`. The dot notation is not parsed.
</pitfall>

<pitfall name="dumping-output">
Don't paste the full molmass output into a lab note. Record the formula and the MW used, e.g. `CaCl2(H2O)2, MW 147.01 g/mol`. The isotope distribution table is noise for bench work.
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
