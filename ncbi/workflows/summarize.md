# Workflow: Look Up Metadata

<required_reading>
**Read these reference files NOW:**
1. references/fields.md (for available --fields values)
</required_reading>

<process>

**Step 1: Determine what to look up**

- **Genome metadata** -- assembly info, annotation status, organism details
- **Gene metadata** -- gene ID, symbol, description, location, products
- **Taxonomy** -- taxonomic classification, lineage
- **Virus** -- viral genome metadata

**Step 2: Build the summary command**

**Genome summary:**
```bash
datasets summary genome taxon 'ORGANISM' --as-json-lines | \
  dataformat tsv genome --fields accession,assminfo-name,organism-name,annotinfo-name
```

Useful genome summary flags:
- `--reference` -- reference genomes only
- `--annotated` -- annotated genomes only
- `--assembly-source refseq|genbank`
- `--released-after YYYY-MM-DD`

**Gene summary:**
```bash
datasets summary gene symbol GENE --taxon 'ORGANISM' --as-json-lines | \
  dataformat tsv gene --fields symbol,gene-id,description,gene-type
```

Gene summary by ID:
```bash
datasets summary gene gene-id 12345 --as-json-lines | \
  dataformat tsv gene
```

**Gene product report** (transcripts and proteins):
```bash
datasets summary gene symbol GENE --taxon 'ORGANISM' --report product --as-json-lines | \
  dataformat tsv gene-product --fields symbol,transcript-accession,protein-accession,protein-name
```

**Taxonomy summary:**
```bash
datasets summary taxonomy taxon 'ORGANISM' --as-json-lines | \
  dataformat tsv taxonomy
```

**Genome sequence report** (chromosome-level info):
```bash
datasets summary genome accession GCF_000001215.4 --report sequence --as-json-lines | \
  dataformat tsv genome-seq --fields accession,chr-name,seq-length
```

**Step 3: Refine output**

- Use `--fields` to select specific columns (see `references/fields.md`)
- Use `--template summary` or `--template gene-ontology` for predefined column sets
- Pipe to standard tools for further filtering: `| sort -k2 -n | head -20`

</process>

<success_criteria>
This workflow is complete when:
- [ ] Summary command returns data (not empty or error)
- [ ] Output contains the fields the user needs
- [ ] `--as-json-lines` is used when piping to dataformat
</success_criteria>
