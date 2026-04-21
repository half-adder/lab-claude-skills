---
name: geo-database
description: Search NCBI GEO and download gene expression / functional genomics datasets (GSE, GSM, GPL). Use when pulling published Drosophila chromatin, RNA-seq, ChIP-seq, or CUT&Tag datasets for reanalysis, or looking up GEO metadata for a paper.
---

<essential_principles>

**GEO accession types:**
- `GSE` -- Series (a full study, e.g. GSE123456)
- `GSM` -- Sample (one library/replicate)
- `GPL` -- Platform (array or sequencer model)
- `GDS` -- Curated dataset (rare; skip in favor of GSE)

**Two access paths:**
- **GEOparse (Python)** -- best for Series Matrix + metadata (processed expression tables, sample annotations)
- **FTP / SRA Toolkit** -- best for raw FASTQ / supplementary files (the usual path for ChIP-seq, CUT&Tag, RNA-seq reanalysis)

**Rules:**
1. For raw-read reanalysis (ChIP-seq, CUT&Tag, RNA-seq), you almost always want FASTQs from SRA, not the GEO series matrix. GEO supplementary files are often processed bigwigs/peaks, not reads.
2. Set `Entrez.email` before any Biopython calls. Use an API key for >3 req/s.
3. Raw data is large. Ask whether to run on the **HPC cluster** or **locally** before downloading.
4. Drosophila context: typical organism filter is `Drosophila melanogaster[Organism]`. Common platforms: GPL13304 (HiSeq 2000), GPL17275 (HiSeq 2500), GPL19132 (NextSeq 500), GPL21306 (HiSeq 4000).
5. Always cite the original GSE in experiment notes when reanalyzing.
</essential_principles>

<intake>
What would you like to do?

1. **Look up a GSE** -- fetch metadata, sample list, and platform info for a known accession
2. **Search GEO** -- find datasets by keyword / organism / assay type
3. **Download processed data** -- series matrix / supplementary files (bigwigs, peak calls, count tables)
4. **Download raw reads** -- FASTQ via SRA for reanalysis
5. **Inspect samples** -- list GSMs in a series with their metadata (conditions, replicates, antibodies)

**Also ask: where will the analysis run?**
- **HPC cluster** (default for raw reads / large downloads) -- generate an `sra-tools` + `prefetch`/`fasterq-dump` script, hand off to `/deploy-hpc-job`
- **Local machine** -- small metadata pulls, processed tables, quick inspection

**Wait for response before proceeding.**
</intake>

<quick_start>

**Install (local, only needed once):**
```bash
uv pip install GEOparse biopython
```

**Look up a series (metadata only, fast):**
```python
from Bio import Entrez
Entrez.email = "seanjohnsen@unc.edu"

h = Entrez.esearch(db="gds", term="GSE123456[Accession]")
uid = Entrez.read(h)["IdList"][0]
summary = Entrez.read(Entrez.esummary(db="gds", id=uid))[0]
print(summary["title"], summary["taxon"], summary["n_samples"])
```

**Full series + sample metadata with GEOparse:**
```python
import GEOparse
gse = GEOparse.get_GEO(geo="GSE123456", destdir="./geo_cache")
print(gse.metadata["title"][0], gse.metadata["overall_design"][0])
for name, gsm in gse.gsms.items():
    print(name, gsm.metadata["title"][0], gsm.metadata.get("characteristics_ch1", []))
```

**Drosophila chromatin search:**
```python
query = '"Drosophila melanogaster"[Organism] AND ("CUT&Tag"[All Fields] OR "ChIP-seq"[All Fields]) AND Polycomb[All Fields]'
h = Entrez.esearch(db="gds", term=query, retmax=50)
print(Entrez.read(h)["IdList"])
```

**Get SRA run IDs (SRR) for a GSE -- needed for FASTQ download:**
```python
# Use SRA Run Selector: https://www.ncbi.nlm.nih.gov/Traces/study/?acc=GSE123456
# Or programmatically via Entrez link gds -> sra
h = Entrez.elink(dbfrom="gds", db="sra", id=uid)
links = Entrez.read(h)
# Then esummary on sra UIDs to get SRR accessions
```
</quick_start>

<raw_read_workflow>

**For ChIP-seq / CUT&Tag / RNA-seq reanalysis, the normal flow is:**

1. Resolve GSE → list of SRR run accessions (via GEO page "SRA Run Selector" link, or Entrez elink `gds`→`sra`).
2. Save SRR list + sample metadata (GSM title, antibody, genotype, stage) to a TSV. This becomes your samplesheet.
3. On the HPC cluster, run `prefetch` then `fasterq-dump`:
   ```bash
   module load sra-tools
   prefetch --option-file srr_list.txt -O ./sra
   for srr in $(cat srr_list.txt); do
       fasterq-dump --split-files --threads 8 -O ./fastq ./sra/$srr
   done
   pigz fastq/*.fastq
   ```
4. Hand off to downstream pipeline (nf-core/chipseq, custom Snakemake, etc.) via `/deploy-hpc-job`.

**Do not `fasterq-dump` on the laptop for more than 2-3 samples.** It is I/O and disk heavy (each human-sized library is ~10-50 GB uncompressed). Drosophila libraries are smaller (~2-10 GB) but still better on the cluster.
</raw_read_workflow>

<processed_data_workflow>

**Supplementary files (bigwigs, peaks, count tables):**
```python
import GEOparse
gse = GEOparse.get_GEO(geo="GSE123456", destdir="./geo_cache")
gse.download_supplementary_files(directory="./GSE123456_suppl", download_sra=False)
```

**Series matrix (processed expression table, array studies or author-provided counts):**
```bash
wget ftp://ftp.ncbi.nlm.nih.gov/geo/series/GSE123nnn/GSE123456/matrix/GSE123456_series_matrix.txt.gz
```

Author-submitted supplementary files are idiosyncratic. Always open one and check column meaning before assuming it is a count table vs RPKM vs log2-normalized.
</processed_data_workflow>

<deeper_reference>

For detailed E-utilities specs, SOFT/MINiML format internals, FTP directory structure, advanced GEOparse patterns, and troubleshooting, see `references/geo-reference.md`. Load it when:
- Writing a batch-query script across >10 GSEs
- Parsing SOFT/MINiML directly (GEOparse failing)
- Debugging rate-limit or pagination issues
- Working with an older series that lacks a series matrix
</deeper_reference>

<success_criteria>
- Accession(s) confirmed with the user before downloading large files
- Raw-read jobs dispatched to the cluster, not run locally
- A samplesheet (GSM → SRR → condition/antibody/genotype) saved alongside any FASTQ download
- Original GSE cited in the experiment note that uses the data
</success_criteria>
