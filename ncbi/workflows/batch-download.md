# Workflow: Batch Download (Dehydrated)

<required_reading>
**Read these reference files NOW:**
1. references/commands.md (for rehydrate flags)
</required_reading>

<process>

**When to use this workflow:**
- Downloading more than ~50 genomes
- Total download size exceeds 15 GB
- Need to resume interrupted downloads

The dehydrated workflow downloads metadata first, then fetches sequence files separately. This is more reliable for large downloads.

**Step 1: Prepare accession list (if using accessions)**

Create a text file with one accession per line:
```bash
# accessions.txt
GCF_000001215.4
GCF_000005575.2
GCF_000002035.6
```

**Step 2: Download dehydrated package**

By accession file:
```bash
datasets download genome accession --inputfile accessions.txt \
  --include genome,gff3,protein \
  --dehydrated \
  --filename dehydrated.zip
```

By taxon:
```bash
datasets download genome taxon 'Drosophila' \
  --include genome,gff3 \
  --dehydrated \
  --filename dehydrated.zip
```

**Step 3: Extract the dehydrated package**

```bash
unzip dehydrated.zip -d my_genomes
```

This creates the directory structure with metadata but without sequence files.

**Step 4: Rehydrate (download actual sequences)**

```bash
datasets rehydrate --directory my_genomes/
```

This fetches all sequence files. It can be interrupted and resumed by re-running the same command.

**Step 5: Verify**

```bash
ls my_genomes/ncbi_dataset/data/
```

Each accession gets its own subdirectory with the requested files.

</process>

<success_criteria>
This workflow is complete when:
- [ ] Dehydrated package downloaded
- [ ] Package extracted to target directory
- [ ] Rehydration completed (all sequences downloaded)
- [ ] Expected files present in per-accession subdirectories
</success_criteria>
