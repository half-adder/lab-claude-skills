# Workflow: Format Output with dataformat

<required_reading>
**Read these reference files NOW:**
1. references/fields.md (for available --fields values)
</required_reading>

<process>

**Step 1: Identify the data source**

`dataformat` accepts input from two sources:
1. **Piped from `datasets summary`** (must use `--as-json-lines`)
2. **From an extracted data package** (reads `assembly_data_report.jsonl` in the package)

**Step 2: Choose output format**

- `dataformat tsv` -- tab-separated values (most common)
- `dataformat excel` -- Excel workbook (.xlsx)

**Step 3: Choose report type**

Match the report type to your data:

| Report type | Use for |
|-------------|---------|
| `genome` | Genome assembly metadata |
| `genome-seq` | Genome sequence/chromosome info |
| `gene` | Gene metadata |
| `gene-product` | Transcript/protein details |
| `virus-genome` | Virus genome data |
| `virus-annotation` | Virus annotation data |
| `taxonomy` | Taxonomy information |

**Step 4: Select fields**

Option A -- Specify fields explicitly:
```bash
dataformat tsv genome --fields accession,assminfo-name,organism-name
```

Option B -- Use a predefined template:
```bash
dataformat tsv gene --template summary
dataformat tsv gene --template gene-ontology
```

Option C -- Show all fields (no --fields flag):
```bash
dataformat tsv genome
```

**Step 5: Format from piped data**

```bash
datasets summary genome taxon 'Drosophila melanogaster' --reference --as-json-lines | \
  dataformat tsv genome --fields accession,assminfo-name,organism-name
```

**Step 6: Format from extracted package**

```bash
# After extracting a downloaded ZIP
dataformat tsv genome --inputfile ncbi_dataset/data/assembly_data_report.jsonl \
  --fields accession,assminfo-name,organism-name
```

**Additional options:**
- `--elide-header` -- suppress column header row
- `--force` -- bypass type check prompts

</process>

<success_criteria>
This workflow is complete when:
- [ ] Output is in the desired format (TSV or Excel)
- [ ] Correct report type matches the data
- [ ] Selected fields contain the information needed
</success_criteria>
