<required_reading>
**Read these files NOW:**
1. `cluster-config.toml` (for user's cluster settings)
2. `references/cluster.md` (for SLURM templates and resource guidelines)
</required_reading>

<process>

**Step 1: Gather requirements**

Ask the user (one question at a time, infer what you can from context):
- What software/algorithm to run? (fetch docs if URL provided)
- What input data? (inspect files locally -- check shape, dtype, metadata)
- Where on the cluster should the project live? (default: `{paths.scratch}<project-name>/`)
- GPU or CPU job? How many resources needed?

**Step 2: Scaffold the uv project**

Create locally under `{paths.local_code}/<project-name>/`:

```
<project-name>/
├── pyproject.toml    # uv project, pinned Python, CUDA torch index if GPU
├── <script>.py       # Main computation script(s)
├── <job>.sl          # SLURM submission script(s)
└── data/             # (created on remote, not synced empty)
```

`pyproject.toml` must include:
- `requires-python = ">=3.11,<3.14"`
- All dependencies including torch if GPU
- PyTorch CUDA index if GPU job (see essential_principles)

Python scripts must include:
- `torch.set_float32_matmul_precision("medium")` if using PyTorch on GPU
- Sensible `num_workers` matching SLURM CPU allocation (8-12, not default)

SLURM scripts must include (see references/cluster.md for templates):
- Appropriate partition and resources from cluster config
- `export PATH="$HOME/.local/bin:$PATH"` for uv
- `mkdir -p logs` for output
- `cd` to project directory
- `uv run python <script>.py`
- Mail notification to `{email.address}`

**Step 3: Deploy to cluster**

```bash
# Sync project files
rsync -avz {paths.local_code}/<project-name>/ {ssh.host}:{paths.scratch}<project-name>/

# Create data directory on remote
ssh {ssh.host} 'mkdir -p {paths.scratch}<project-name>/data'

# Sync input data (if local)
rsync -avz --progress '<local-data-path>' {ssh.host}:{paths.scratch}<project-name>/data/<filename>
```

**Step 4: Remote setup**

```bash
# Install uv if needed
ssh {ssh.host} 'which uv 2>/dev/null || (curl -LsSf https://astral.sh/uv/install.sh | sh)'

# Sync dependencies (must run on login node -- has internet)
ssh {ssh.host} 'export PATH="$HOME/.local/bin:$PATH" && cd {paths.scratch}<project-name> && uv sync'
```

**Step 5: Verify**

Run a quick import check on the login node:
```bash
ssh {ssh.host} 'export PATH="$HOME/.local/bin:$PATH" && cd {paths.scratch}<project-name> && uv run python -c "import <key_package>; print(\"OK\")"'
```

For GPU jobs, CUDA won't be available on login node -- that's expected. Verify imports work.

**Step 6: Submit**

```bash
ssh {ssh.host} 'cd {paths.scratch}<project-name> && sbatch <job>.sl'
```

Report the job ID and provide monitoring commands.

</process>

<success_criteria>
This workflow is complete when:
- [ ] Project scaffolded locally with all scripts
- [ ] Files rsync'd to cluster
- [ ] Dependencies installed via `uv sync` on login node
- [ ] Import check passes
- [ ] Job submitted and job ID reported
- [ ] User given monitoring commands (squeue, tail logs)
</success_criteria>
