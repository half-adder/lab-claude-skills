<overview>
Field names for `dataformat tsv/excel --fields`. Field names use hyphen-separated dot-paths. Run a command without `--fields` to see all available columns for a report type.
</overview>

<genome_fields>
Common fields for `dataformat tsv genome`:

| Field | Description |
|-------|-------------|
| `accession` | Assembly accession (GCF_/GCA_) |
| `assminfo-name` | Assembly name |
| `assminfo-level` | Assembly level (chromosome, scaffold, etc.) |
| `assminfo-status` | Assembly status |
| `assminfo-submitter` | Submitting organization |
| `assminfo-refseq-category` | RefSeq category |
| `organism-name` | Species name |
| `organism-tax-id` | NCBI Taxonomy ID |
| `organism-infraspecific-breed` | Breed/strain info |
| `annotinfo-name` | Annotation name |
| `annotinfo-release-date` | Annotation release date |
| `annotinfo-report-url` | Annotation report URL |
| `assmstats-total-sequence-len` | Total sequence length |
| `assmstats-contig-n50` | Contig N50 |
| `assmstats-scaffold-n50` | Scaffold N50 |
| `assmstats-number-of-contigs` | Number of contigs |
| `assmstats-gc-percent` | GC content percentage |
</genome_fields>

<genome_seq_fields>
Common fields for `dataformat tsv genome-seq`:

| Field | Description |
|-------|-------------|
| `accession` | Assembly accession |
| `chr-name` | Chromosome name |
| `seq-length` | Sequence length |
| `genbank-seq-acc` | GenBank sequence accession |
| `refseq-seq-acc` | RefSeq sequence accession |
| `role` | Sequence role (assembled-molecule, etc.) |
| `mol-type` | Molecule type |
| `gc-percent` | GC content percentage |
| `sequence-name` | Sequence name |
| `ucsc-style-name` | UCSC-style name |
</genome_seq_fields>

<gene_fields>
Common fields for `dataformat tsv gene`:

| Field | Description |
|-------|-------------|
| `gene-id` | NCBI Gene ID |
| `symbol` | Gene symbol |
| `description` | Gene description |
| `gene-type` | Gene type (protein-coding, etc.) |
| `tax-id` | Taxonomy ID |
| `tax-name` | Organism name |
| `synonyms` | Gene synonyms |
| `chromosomes` | Chromosome location |
| `annotation-genomic-range-accession` | Genomic accession for location |
| `annotation-genomic-range-range-start` | Start position |
| `annotation-genomic-range-range-stop` | Stop position |
| `annotation-genomic-range-range-orientation` | Strand orientation |
| `annotation-genomic-range-seq-name` | Sequence name (e.g., 3R) |
| `annotation-assembly-accession` | Assembly accession for annotation |
| `annotation-assembly-name` | Assembly name for annotation |
| `annotation-release-name` | Annotation release name |
| `ensembl-geneids` | Ensembl Gene IDs |
| `omim-ids` | OMIM IDs |
| `swissprot-accessions` | SwissProt accessions |
| `summary-description` | Gene summary/function description |
| `protein-count` | Number of protein products |
| `transcript-count` | Number of transcripts |
</gene_fields>

<gene_product_fields>
Common fields for `dataformat tsv gene-product`:

| Field | Description |
|-------|-------------|
| `symbol` | Gene symbol |
| `gene-id` | NCBI Gene ID |
| `gene-type` | Gene type |
| `transcript-accession` | RefSeq transcript accession |
| `transcript-name` | Transcript name |
| `transcript-length` | Transcript length (nt) |
| `transcript-protein-accession` | RefSeq protein accession |
| `transcript-protein-name` | Protein name |
| `transcript-protein-length` | Protein length (aa) |
| `transcript-genomic-location-accession` | Genomic accession for transcript location |
| `transcript-genomic-location-seq-name` | Sequence name (e.g., 3R) |
| `transcript-select-category` | Transcript selection category |
| `transcript-transcript-type` | Transcript type |
</gene_product_fields>

<templates>
Predefined field templates (use `--template NAME` instead of `--fields`):

- `summary` -- common overview fields for the report type
- `gene-ontology` -- GO term annotations (for gene reports)
</templates>

<tips>
- Run `dataformat tsv REPORT_TYPE` without `--fields` to see all available columns
- Field names are hyphen-separated paths derived from the JSON structure
- Multiple fields are comma-separated: `--fields accession,organism-name,assminfo-name`
- Templates and `--fields` are mutually exclusive
</tips>
