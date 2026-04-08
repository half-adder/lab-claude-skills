# Workflow: Download Data

<required_reading>
**Read these reference files NOW:**
1. references/commands.md (for available flags and subcommands)
</required_reading>

<process>

**Step 1: Determine data type**

Ask what kind of data if not already clear:
- **Genome** -- assembly sequences, annotations (GFF3, GTF), proteins, CDS
- **Gene** -- gene sequences, transcripts, proteins for specific genes
- **Virus** -- viral genome or protein data

**Step 2: Identify the target**

Genomes can be specified by:
- Assembly accession (`GCF_000001215.4`)
- BioProject accession (`PRJNA12345`)
- Taxonomic name (`'Drosophila melanogaster'`)
- NCBI Taxonomy ID (`7227`)

Genes can be specified by:
- Gene symbol + taxon (`Ubx --taxon 'Drosophila melanogaster'`)
- NCBI Gene ID (`42034`)
- RefSeq accession
- Locus tag

**Step 3: Build the download command**

**Genome download:**
```bash
datasets download genome taxon 'ORGANISM' \
  --include genome,gff3,protein \
  --filename output.zip
```

Common genome flags:
- `--reference` -- reference genomes only
- `--annotated` -- annotated genomes only
- `--assembly-level chromosome|complete|contig|scaffold`
- `--assembly-source refseq|genbank`
- `--include genome,rna,protein,cds,gff3,gtf,gbff,seq-report,all,none`
- `--released-after YYYY-MM-DD` / `--released-before YYYY-MM-DD`
- `--chromosomes 2L,2R,3L,3R,X`

**Gene download:**
```bash
datasets download gene symbol GENE_SYMBOL \
  --taxon 'ORGANISM' \
  --include gene,rna,protein,cds \
  --filename gene_data.zip
```

Gene include options: `gene`, `rna`, `protein`, `cds`, `5p-utr`, `3p-utr`, `product-report`, `none`

**Virus download:**
```bash
datasets download virus genome taxon 'VIRUS_NAME' \
  --filename virus_data.zip
```

**Step 4: Preview before downloading (optional)**

Add `--preview` to see what will be included without downloading:
```bash
datasets download genome taxon 'Drosophila melanogaster' --reference --preview
```

**Step 5: Extract and inspect**

```bash
unzip output.zip -d output_dir
ls output_dir/ncbi_dataset/data/
```

</process>

<success_criteria>
This workflow is complete when:
- [ ] ZIP file downloaded successfully
- [ ] Extracted contents contain expected files (FASTA, GFF3, etc.)
- [ ] User has the data they need for their analysis
</success_criteria>
