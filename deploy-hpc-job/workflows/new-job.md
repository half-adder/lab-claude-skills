<required_reading>
**Read these files NOW:**
1. `cluster-config.toml` (for user's cluster settings)
2. `references/cluster.md` (for SLURM templates and resource guidelines)
3. `references/runtimes.md` (for runtime-specific patterns)
</required_reading>

<process>

**Step 1: Gather requirements**

Determine from context or by asking:
- **What to run?** Python script, R script, Nextflow pipeline, or command-line tools?
- **What input data?** Where is it, what format, how large?
- **Where on cluster?** (default: `{paths.scratch}<project-name>/`)
- **GPU or CPU?** How much memory/time needed?
- **What modules?** Check `ssh {ssh.host} 'module avail <tool> 2>&1'` for available versions

Infer what you can from context. Don't ask what's obvious.

**Step 2: Determine runtime type**

Based on Step 1, identify the runtime and read the corresponding section in `references/runtimes.md`:

| If the user wants to run... | Runtime | Key section |
|---|---|---|
| Custom Python scripts, PyTorch, pip packages | Python/uv | `<python_uv>` |
| R scripts, Bioconductor, tidyverse | R | `<r_scripts>` |
| nf-core or custom Nextflow pipelines | Nextflow | `<nextflow_pipelines>` |
| CLI tools (samtools, STAR, bowtie2, etc.) | Module-only | `<module_only>` |

Multiple runtimes can be combined (e.g., module-loaded tools + Python post-processing).

**Step 3: Scaffold the project**

Create locally or directly describe what to deploy. Typical structure:

```
<project-name>/
├── <script(s)>       # .py, .R, .sh, or pipeline config
├── <job>.sl          # SLURM submission script
├── samplesheet.csv   # if applicable
└── data/             # created on remote, not synced empty
```

**SLURM script must include:**
- `module purge` at the top (clean environment)
- `module load <name>/<version>` for each required tool (pinned versions)
- Appropriate partition and resources from cluster config
- `cd` to project directory on scratch
- `mkdir -p logs` for output
- Mail notification to `{email.address}`

For Python/uv jobs, also add:
- `export PATH="$HOME/.local/bin:$PATH"`
- Use `uv run python` instead of bare `python`

See `references/cluster.md` for GPU and CPU SLURM templates.

**Step 4: Deploy to cluster**

```bash
# Sync project files
rsync -avz <local-project>/ {ssh.host}:{paths.scratch}<project-name>/

# Create data directory on remote
ssh {ssh.host} 'mkdir -p {paths.scratch}<project-name>/data'

# Sync input data (if local)
rsync -avz --progress '<local-data-path>' {ssh.host}:{paths.scratch}<project-name>/data/
```

**Step 5: Remote setup** (runtime-dependent)

**Python/uv:**
```bash
ssh {ssh.host} 'which uv 2>/dev/null || (curl -LsSf https://astral.sh/uv/install.sh | sh)'
ssh {ssh.host} 'export PATH="$HOME/.local/bin:$PATH" && cd {paths.scratch}<project-name> && uv sync'
```

**R:**
```bash
ssh {ssh.host} 'module load r/4.5.0 && cd {paths.scratch}<project-name> && Rscript install_packages.R'
```

**Nextflow / Module-only:** No remote setup needed beyond file transfer. Modules are loaded in the SLURM script.

**Step 6: Verify**

Check that key tools/imports are available:
```bash
# Python
ssh {ssh.host} 'export PATH="$HOME/.local/bin:$PATH" && cd {paths.scratch}<project-name> && uv run python -c "import <pkg>; print(\"OK\")"'

# R
ssh {ssh.host} 'module load r/4.5.0 && Rscript -e "library(<pkg>); cat(\"OK\n\")"'

# Module tools
ssh {ssh.host} 'module load <tool>/<version> && <tool> --version'
```

**Step 7: Submit**

```bash
ssh {ssh.host} 'cd {paths.scratch}<project-name> && sbatch <job>.sl'
```

Report the job ID and provide monitoring commands:
```bash
ssh {ssh.host} 'squeue -j <JOB_ID>'
ssh {ssh.host} 'tail -f {paths.scratch}<project-name>/logs/<job>_<JOB_ID>.err'
```

</process>

<success_criteria>
This workflow is complete when:
- [ ] Runtime type identified and correct modules/dependencies determined
- [ ] Project scaffolded with SLURM script and all necessary files
- [ ] Files deployed to cluster via rsync
- [ ] Dependencies installed (if Python/R)
- [ ] Verification check passes
- [ ] Job submitted and job ID reported
- [ ] User given monitoring commands
</success_criteria>
