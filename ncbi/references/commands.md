<overview>
Complete command reference for the `datasets` and `dataformat` CLI tools.
</overview>

<datasets_global_flags>
- `--api-key string` -- NCBI API key (increases rate limit to 10 req/sec)
- `--debug` -- emit debugging info
- `--help` -- detailed help for any command
- `--version` -- print version
</datasets_global_flags>

<datasets_download>

**`datasets download genome`**

Subcommands:
- `accession ACC [ACC...]` -- by assembly accession (GCF_/GCA_) or BioProject (PRJNA)
- `taxon NAME_OR_ID` -- by taxonomic name or NCBI Taxonomy ID

Flags:
- `--include <types>` -- comma-separated: `genome`, `rna`, `protein`, `cds`, `gff3`, `gtf`, `gbff`, `seq-report`, `all`, `none` (default: `genome`)
- `--exclude <types>` -- exclude specific data types
- `--filename <name>` -- output filename (default: `ncbi_dataset.zip`)
- `--reference` -- reference genomes only
- `--annotated` -- annotated genomes only
- `--assembly-level chromosome|complete|contig|scaffold`
- `--assembly-source refseq|genbank`
- `--assembly-version latest|all`
- `--chromosomes 2L,2R,X` -- specific chromosomes
- `--released-after YYYY-MM-DD` / `--released-before YYYY-MM-DD`
- `--search <text>` -- text search (repeatable)
- `--dehydrated` -- metadata-only package (for large downloads)
- `--exclude-atypical` -- remove atypical assemblies
- `--from-type` -- only type material records
- `--mag include|exclude|all` -- metagenome assembled genomes filter
- `--preview` -- show details without downloading
- `--no-progressbar` -- hide progress bar
- `--inputfile <file>` -- read accessions from file (one per line)

**`datasets download gene`**

Subcommands:
- `gene-id ID [ID...]` -- by NCBI Gene ID
- `symbol SYM [SYM...] --taxon ORGANISM` -- by gene symbol (requires --taxon)
- `accession ACC [ACC...]` -- by RefSeq nucleotide/protein accession
- `taxon NAME_OR_ID` -- by taxonomy
- `locus-tag TAG [TAG...]` -- by locus tag

Flags:
- `--include <types>` -- comma-separated: `gene`, `rna`, `protein`, `cds`, `5p-utr`, `3p-utr`, `product-report`, `none` (default: `rna,protein`)
- `--fasta-filter <accessions>` -- limit sequences to specified RefSeq accessions
- `--fasta-filter-file <file>` -- accession filter from file
- `--filename <name>` -- output filename
- `--preview` -- show info without downloading
- `--taxon ORGANISM` -- required for symbol lookups

**`datasets download virus`**

Subcommands:
- `genome accession ACC` -- viral genome by accession
- `genome taxon NAME` -- viral genome by taxonomy
- `protein` -- viral protein data

**`datasets download taxonomy taxon NAME`** -- taxonomy data by taxon

</datasets_download>

<datasets_summary>

**`datasets summary genome`**

Subcommands:
- `accession ACC [ACC...]` -- by assembly/BioProject accession
- `taxon NAME_OR_ID` -- by taxonomy

**`datasets summary gene`**

Subcommands:
- `gene-id ID [ID...]` -- by Gene ID(s)
- `symbol SYM [SYM...] --taxon ORGANISM` -- by gene symbol
- `accession ACC [ACC...]` -- by RefSeq accession
- `taxon NAME_OR_ID` -- by taxonomy
- `locus-tag TAG [TAG...]` -- by locus tag

Flags:
- `--report product` -- include transcript/protein details

**`datasets summary virus`**

Subcommands:
- `genome accession ACC` -- by accession
- `genome taxon NAME --host ORGANISM` -- by taxonomy with optional host filter

**`datasets summary taxonomy taxon NAME`** -- taxonomy metadata

**Critical flag for all summary commands:**
- `--as-json-lines` -- **REQUIRED** when piping to `dataformat`
- `--report sequence` -- access genome sequence-level data

</datasets_summary>

<datasets_rehydrate>

`datasets rehydrate --directory DIR`

Restores sequence files for a previously downloaded dehydrated package. Can be interrupted and resumed.
</datasets_rehydrate>

<datasets_completion>

`datasets completion bash|zsh|fish|powershell`

Generates shell autocompletion scripts.
</datasets_completion>

<dataformat_commands>

**Output formats:**
- `dataformat tsv REPORT_TYPE` -- tab-separated values
- `dataformat excel REPORT_TYPE` -- Excel workbook

**Report types** (used with both tsv and excel):

| Report type | Data source |
|-------------|-------------|
| `genome` | Genome assembly metadata |
| `genome-seq` | Genome sequence/chromosome report |
| `gene` | Gene metadata |
| `gene-product` | Transcript/protein details |
| `virus-genome` | Virus genome data |
| `virus-annotation` | Virus annotation data |
| `taxonomy` | Taxonomy information |
| `microbigge` | MicroBIGG-E data |
| `prok-gene` | Prokaryote gene |
| `prok-gene-location` | Prokaryote gene location |
| `genome-annotations` | Genome annotation report |
| `organelle` | Organelle report |

**Flags:**
- `--fields field1,field2,...` -- select output columns
- `--template name` -- predefined column sets (`summary`, `gene-ontology`)
- `--elide-header` -- suppress column header
- `--inputfile FILE` -- read from JSONL file instead of stdin
- `--force` -- bypass type check prompts

**Other commands:**
- `dataformat catalog` -- show available data in a package
- `dataformat version` -- print version
- `dataformat completion bash|zsh|fish|powershell` -- shell autocompletion

</dataformat_commands>
