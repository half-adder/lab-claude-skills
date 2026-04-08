---
name: deploy-hpc-job
description: Deploy Python scientific computing jobs to an HPC cluster via SLURM. Scaffolds uv projects, generates SLURM scripts, handles rsync deployment, remote setup, and job management. Use when setting up or managing GPU/CPU jobs on HPC, or when the user mentions SLURM, cluster, or HPC.
---

<essential_principles>

**Before any workflow, load the user's cluster config:**

Read `cluster-config.toml` in this skill's directory. If it does not exist, tell the user:

> You need to configure your cluster settings first. Copy `cluster-config.example.toml` to `cluster-config.toml` and fill in your SSH host, username, scratch path, and email.

Then read the example file and help them fill it in. Do not proceed until the config exists.

Use the config values everywhere instead of hardcoded paths. Reference them as `{ssh.host}`, `{ssh.user}`, `{paths.scratch}`, etc. throughout the workflows.

**Python on HPC:**
- Always use `uv`, never pip, conda, or module-loaded Python
- Pin `requires-python = ">=3.11,<3.14"` (PyTorch lacks wheels for bleeding-edge CPython)
- For GPU jobs, configure PyTorch CUDA index in `pyproject.toml`:
  ```toml
  [tool.uv.sources]
  torch = [{ index = "pytorch" }]

  [[tool.uv.index]]
  name = "pytorch"
  url = "https://download.pytorch.org/whl/cu124"
  explicit = true
  ```
- Install uv on cluster: `curl -LsSf https://astral.sh/uv/install.sh | sh`
- Run `uv sync` on login node (compute nodes may lack internet)
- SLURM scripts need `export PATH="$HOME/.local/bin:$PATH"` for uv

**Common pitfalls:**
- Set `torch.set_float32_matmul_precision("medium")` to use tensor cores on modern GPUs
- Match `num_workers` in data loaders to `--cpus-per-task` in SLURM (default can be 128+)
- Create remote directories before rsync'ing files into them
- Use `rsync -avz` for deployment, not scp

</essential_principles>

<intake>
What would you like to do?

1. **New project** -- scaffold a Python project, write SLURM scripts, deploy to cluster, and submit
2. **Manage existing job** -- monitor, cancel, resubmit, or retrieve results from a running/completed job

**Wait for response before proceeding.**
</intake>

<routing>
| Response | Workflow |
|----------|----------|
| 1, "new", "create", "set up", "deploy", "scaffold" | `workflows/new-project.md` |
| 2, "manage", "monitor", "check", "cancel", "retrieve", "results", "status" | `workflows/manage-job.md` |

**After reading the workflow, follow it exactly.**
</routing>

<reference_index>
**Cluster reference:** references/cluster.md -- partitions, resource limits, SLURM templates, interactive sessions
</reference_index>

<workflows_index>
| Workflow | Purpose |
|----------|---------|
| new-project.md | Full scaffold-to-submit pipeline for a new HPC job |
| manage-job.md | Monitor, cancel, resubmit, retrieve results |
</workflows_index>
