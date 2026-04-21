<overview>
Runtime-specific patterns for different job types. Each section covers the SLURM script setup, dependency management, and deployment steps for a particular runtime.
</overview>

<python_uv>

**When to use:** Custom Python scripts, PyTorch/deep learning, data analysis with pandas/numpy, or any pip-installable workflow.

**Why uv:** Faster than pip/conda, deterministic lockfiles, no module-loaded Python needed.

**Project structure:**
```
<project-name>/
├── pyproject.toml
├── <script>.py
├── <job>.sl
└── data/            # created on remote
```

**pyproject.toml essentials:**
```toml
[project]
name = "<project-name>"
version = "0.1.0"
requires-python = ">=3.11,<3.14"
dependencies = ["numpy", "pandas"]

# For GPU/PyTorch jobs, add:
[tool.uv.sources]
torch = [{ index = "pytorch" }]

[[tool.uv.index]]
name = "pytorch"
url = "https://download.pytorch.org/whl/cu124"
explicit = true
```

**SLURM script additions:**
```bash
export PATH="$HOME/.local/bin:$PATH"
uv run python <script>.py
```

**Deployment:**
```bash
# Install uv on cluster (one-time)
ssh {ssh.host} 'which uv 2>/dev/null || (curl -LsSf https://astral.sh/uv/install.sh | sh)'

# Sync project and install deps
rsync -avz <local-project>/ {ssh.host}:{paths.scratch}<project>/
ssh {ssh.host} 'export PATH="$HOME/.local/bin:$PATH" && cd {paths.scratch}<project> && uv sync'
```

**GPU-specific Python tips:**
- Set `torch.set_float32_matmul_precision("medium")` for tensor core GPUs (A100, L40)
- Match `num_workers` in data loaders to `--cpus-per-task` (don't use defaults)
- CUDA won't be available on login node, that's expected during `uv sync`

</python_uv>

<r_scripts>

**When to use:** R scripts, Bioconductor workflows, statistical analysis.

**Module setup:**
```bash
module load r/4.5.0
```

**Project structure:**
```
<project-name>/
├── install_packages.R   # package installation script
├── <script>.R
├── <job>.sl
└── data/
```

**Package installation** (run on login node before submitting):
```r
# install_packages.R
if (!require("BiocManager", quietly = TRUE))
    install.packages("BiocManager")
BiocManager::install(c("DESeq2", "GenomicRanges"))
install.packages(c("tidyverse", "data.table"))
```

```bash
ssh {ssh.host} 'module load r/4.5.0 && cd {paths.scratch}<project> && Rscript install_packages.R'
```

**SLURM script additions:**
```bash
module purge
module load r/4.5.0

Rscript <script>.R
```

**Tips:**
- R packages install to `~/R/` by default, shared across jobs
- For reproducibility, consider using `renv` for lockfiles
- Some Bioconductor packages need system libraries. Check module availability first.

</r_scripts>

<nextflow_pipelines>

**When to use:** nf-core pipelines, custom Nextflow workflows, multi-step bioinformatics pipelines.

**Module setup:**
```bash
module load nextflow/25.04.7
```

**Project structure:**
```
<project-name>/
├── run.sh           # wrapper script with nextflow command
├── <job>.sl         # SLURM script that calls run.sh
├── params.yml       # pipeline parameters (optional)
└── samplesheet.csv  # input sample sheet
```

**SLURM script for Nextflow** (Nextflow manages its own sub-jobs via SLURM):
```bash
module purge
module load nextflow/25.04.7

# Nextflow needs a head job with modest resources
# It submits worker jobs to SLURM automatically

nextflow run nf-core/<pipeline> \
    -profile singularity \
    --input samplesheet.csv \
    --outdir results/ \
    -params-file params.yml \
    -work-dir {paths.scratch}<project>/work
```

**Important Nextflow notes:**
- The SLURM script for Nextflow is a **head job**, not the compute job. Request minimal resources (2 CPUs, 8GB).
- Nextflow submits its own SLURM jobs for each process. It needs `-profile singularity` or `-profile apptainer` on most clusters.
- Use `-work-dir` on **fast scratch** (e.g. `/work` on Longleaf, parallel FS on most sites). Home directories are often NFS-cached and cause slow `.exitcode` propagation, which feeds directly into the failure mode below.
- Resume failed runs with `-resume`
- Clean up work directory after successful runs: `nextflow clean -f`

**SLURM executor configuration (required for reliable runs):**

Nextflow's SLURM grid executor has a well-documented failure mode where a single missing-from-queue reading falsely starts an exit-status timeout, causing tasks to be marked failed while still running (nextflow-io/nextflow #5298, #5813, #1644). Set these in `nextflow.config` to prevent it:

```groovy
profiles {
    slurm {
        executor {
            // Must be longer than your longest task. Once the timer starts
            // (on a single bad squeue reading), Nextflow does not reset it
            // even when subsequent readings show the job running again.
            exitReadTimeout   = '6.h'

            // Biowulf-recommended values to reduce slurmctld RPC load and
            // minimize the chance of transient squeue glitches. Source:
            // https://hpc.nih.gov/apps/nextflow.html
            pollInterval      = '2.min'
            queueStatInterval = '5.min'
            submitRateLimit   = '6/1min'
            queueSize         = 20
        }

        process {
            executor = 'slurm'
            // CRITICAL: do NOT set `queue = '<name>'`. If you do, Nextflow
            // calls `squeue -p <name>`, which misses any child job SLURM
            // auto-routes to a different partition (e.g. hov, spill on
            // Longleaf). Leave unset so `squeue -u $USER` is used.
            errorStrategy = { task.exitStatus in 137..143 ? 'retry' : 'finish' }
            maxRetries    = 1

            // Per-process resources still work fine without process.queue:
            withName: BOWTIE2_ALIGN { cpus = 8; memory = '16.GB'; time = '4.h' }
            // ...
        }
    }
}

// Enable overwrite on these or -resume fails on re-render:
timeline { enabled = true; overwrite = true; file = "<outdir>/pipeline_info/timeline.html" }
report   { enabled = true; overwrite = true; file = "<outdir>/pipeline_info/report.html"   }
trace    { enabled = true; overwrite = true; file = "<outdir>/pipeline_info/trace.txt"      }
```

**Post-Dec 2025 Nextflow** (check your cluster's installed version): `executor.slurm.onlyJobState = true` switches to SchedMD's lightweight `squeue --only-job-state` RPC, which largely sidesteps this class of bug. From PR #6659.

**Verify before long runs:** after submitting, SSH to the cluster and run `squeue -u $USER` (no `-p` filter). Confirm all child jobs appear. If they don't — e.g. they're all under a partition you didn't specify — that's the auto-routing issue; the config above handles it but it's worth sanity-checking on a new cluster.

**Symptom-to-fix map when a Nextflow-on-SLURM run fails:**

| Error in log | Cause | Fix |
|---|---|---|
| `Process ... terminated for an unknown reason -- Likely it has been terminated by the external system` with job actually still RUNNING per `sacct` | `squeue` partial results (often partition filter; sometimes controller overload) | Remove `process.queue`; bump `exitReadTimeout` |
| `Failed to get exit status ... exitStatusReadTimeoutMillis: 1800000; delta: 1800xxx` in `.nextflow.log` | Same as above, just the debug-level message | Same as above |
| `Timeline file already exists` / `Report file already exists` on `-resume` | Missing `overwrite = true` | Add `overwrite = true` to timeline/report/trace |
| `Nextflow-on-fast-FS works but `.exitcode` still slow` | NFS-backed home for workDir | Move workDir to parallel scratch (`/work` etc.), or symlink the old path there to keep the cache valid |

</nextflow_pipelines>

<module_only>

**When to use:** Running installed tools directly (samtools, bedtools, STAR, bowtie2, GATK, deeptools, etc.) without a custom script.

**Common patterns:**

```bash
module purge
module load samtools/1.23.1 bedtools/2.31.1

# Pipeline commands
samtools sort input.bam -o sorted.bam
samtools index sorted.bam
bedtools intersect -a peaks.bed -b genes.bed > overlap.bed
```

**Multi-tool pipeline example (ChIP-seq/CUT&Tag):**
```bash
module purge
module load bowtie2/2.5.4 samtools/1.23.1 picard/3.4.0 deeptools/3.5.6 macs3/3.0.3

# Align
bowtie2 -x $GENOME_INDEX -1 $R1 -2 $R2 --very-sensitive-local | \
    samtools sort -o aligned.bam

# Deduplicate
picard MarkDuplicates I=aligned.bam O=dedup.bam M=metrics.txt REMOVE_DUPLICATES=true

# Index
samtools index dedup.bam

# Call peaks
macs3 callpeak -t dedup.bam -f BAMPE -g dm --outdir peaks/

# Coverage track
bamCoverage -b dedup.bam -o coverage.bw --normalizeUsing RPKM
```

**Tips:**
- Pin module versions for reproducibility
- Check `module avail <tool> 2>&1` for available versions
- Some tools need specific versions to be compatible (e.g., GATK + specific Java)

</module_only>
