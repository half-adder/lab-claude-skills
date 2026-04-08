---
name: ncbi-datasets
description: Query and download biological sequence data from NCBI using the datasets and dataformat CLI tools. Use when downloading genomes, genes, or viral sequences, looking up gene/genome metadata, or converting NCBI data to TSV/Excel.
---

<essential_principles>

**Two CLI tools work together:**
- `datasets` -- queries and downloads data from NCBI (genomes, genes, viruses, taxonomy)
- `dataformat` -- converts JSON Lines metadata into TSV or Excel

**Critical rules:**
1. **Always use `--as-json-lines`** when piping `datasets summary` to `dataformat`. Without it, the pipe fails.
2. **Quote taxonomic names** with spaces: `'Drosophila melanogaster'`
3. **Accession prefixes:** `GCF_` = RefSeq, `GCA_` = GenBank
4. **Size limits:** Direct downloads work best for <1,000 genomes or <15 GB. Use dehydrated workflow for larger sets.
5. **Rate limiting:** Default 5 req/sec. Use `--api-key` for 10 req/sec.
6. **Data packages** are ZIP archives. When extracted: `ncbi_dataset/data/` contains sequences and `assembly_data_report.jsonl` metadata.

**Before any workflow, check that the CLI tools are installed:**
```bash
which datasets && which dataformat
```

If either is missing, read `references/installation.md` and walk the user through installation before proceeding. Do not skip this step.
</essential_principles>

<quick_start>
**Genome metadata to TSV:**
```bash
datasets summary genome taxon 'Drosophila melanogaster' --reference --as-json-lines | \
  dataformat tsv genome --fields accession,assminfo-name,organism-name,annotinfo-name
```

**Download a reference genome with annotations:**
```bash
datasets download genome taxon 'Drosophila melanogaster' --reference \
  --include genome,gff3,protein --filename dmel_ref.zip
```

**Gene lookup:**
```bash
datasets summary gene symbol Ubx --taxon 'Drosophila melanogaster' --as-json-lines | \
  dataformat tsv gene --fields symbol,gene-id,description
```
</quick_start>

<intake>
What would you like to do?

1. **Download data** -- genome, gene, or virus sequences and annotations
2. **Look up metadata** -- query gene/genome/taxonomy info without downloading
3. **Format output** -- convert existing data package or piped output to TSV/Excel
4. **Batch download** -- large-scale downloads using the dehydrated workflow
5. **Cytological band** -- download GenBank data for a Drosophila cytological band (e.g., 89E)
6. Something else

**Wait for response before proceeding.**
</intake>

<routing>
| Response | Workflow |
|----------|----------|
| 1, "download", "get genome", "get gene" | `workflows/download.md` |
| 2, "look up", "summary", "metadata", "info", "search" | `workflows/summarize.md` |
| 3, "format", "tsv", "excel", "convert", "dataformat" | `workflows/format-output.md` |
| 4, "batch", "dehydrated", "large", "many genomes" | `workflows/batch-download.md` |
| 5, "cytoband", "cytological", "band", "polytene" | `workflows/cytoband-download.md` |
| 6, other | Clarify intent, then route |

**Intent-based routing (if user provides clear intent without selecting menu):**
- "download the Drosophila genome" -> `workflows/download.md`
- "what genes are in this region" -> `workflows/summarize.md`
- "convert to TSV" -> `workflows/format-output.md`
- "download 500 genomes" -> `workflows/batch-download.md`
- "get GenBank for band 89E" -> `workflows/cytoband-download.md`
- "download cytological region 31" -> `workflows/cytoband-download.md`

**After reading the workflow, follow it exactly.**
</routing>

<reference_index>
All domain knowledge in `references/`:

**CLI Reference:** commands.md (full command tree, flags, subcommands)
**Field Names:** fields.md (dataformat field names for --fields flag)
**Installation:** installation.md (install methods for macOS, Linux, conda)
**Drosophila Cytobands:** dmel-cytobands.tsv (593 letter-level bands) and dmel-cytobands-subdivisions.tsv (4,007 individual polytene bands) → R6 coordinates. Try subdivisions first.
</reference_index>

<workflows_index>
| Workflow | Purpose |
|----------|---------|
| download.md | Download genome, gene, or virus data as ZIP packages |
| summarize.md | Query metadata without downloading (summary to stdout) |
| format-output.md | Convert JSON Lines to TSV or Excel with dataformat |
| batch-download.md | Large-scale downloads using dehydrated workflow |
| cytoband-download.md | Download GenBank data for a Drosophila cytological band |
</workflows_index>

<success_criteria>
- Command runs without error
- Output contains expected data (sequences, metadata, TSV)
- For downloads: ZIP extracted and files present in `ncbi_dataset/data/`
- For summaries: metadata displayed or piped to dataformat successfully
</success_criteria>
