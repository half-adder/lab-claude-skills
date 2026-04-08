---
name: deploy-hpc-job
description: Deploy and manage jobs on an HPC cluster via SLURM. Supports Python (uv), R, Nextflow, and module-based tools. Handles SLURM script generation, rsync deployment, and job management. Use when setting up or managing jobs on HPC, or when the user mentions SLURM, cluster, or HPC.
---

<essential_principles>

**Before any workflow, load the user's cluster config:**

Read `cluster-config.toml` in this skill's directory. If it does not exist, tell the user:

> You need to configure your cluster settings first. Copy `cluster-config.example.toml` to `cluster-config.toml` and fill in your SSH host, username, scratch path, and email.

Then read the example file and help them fill it in. Do not proceed until the config exists.

Use the config values everywhere instead of hardcoded paths.

**Lmod module system:**
- Load software with `module load <name>/<version>` in SLURM scripts
- Check available versions: `ssh {ssh.host} 'module avail <name> 2>&1'`
- Multiple modules can be loaded: `module load samtools/1.23.1 bedtools/2.31.1`
- Module loads go BEFORE the main command in SLURM scripts
- Use `module purge` at the top of SLURM scripts for a clean environment
- Pin specific versions, not defaults, for reproducibility

**Deployment pattern:**
- Use `rsync -avz` for file transfers, never scp
- Create remote directories before rsync'ing into them
- Run setup commands on login node (compute nodes may lack internet)
- Scratch space is for active jobs, not long-term storage

**Common pitfalls:**
- Always specify `--mem` in SLURM, default is often too low
- Match `--cpus-per-task` to actual parallelism in your code
- Quote paths with spaces in SLURM scripts
- Check `.err` log first when jobs fail

</essential_principles>

<intake>
What would you like to do?

1. **New job** -- set up and submit a new job to the cluster
2. **Manage existing job** -- monitor, cancel, resubmit, or retrieve results

**Wait for response before proceeding.**
</intake>

<routing>
| Response | Workflow |
|----------|----------|
| 1, "new", "create", "set up", "deploy", "scaffold", "submit", "run" | `workflows/new-job.md` |
| 2, "manage", "monitor", "check", "cancel", "retrieve", "results", "status" | `workflows/manage-job.md` |

**After reading the workflow, follow it exactly.**
</routing>

<reference_index>
**Cluster details:** references/cluster.md -- partitions, SLURM templates, resource guidelines, interactive sessions
**Runtime guides:** references/runtimes.md -- Python/uv, R, Nextflow, and module-only job patterns
</reference_index>

<workflows_index>
| Workflow | Purpose |
|----------|---------|
| new-job.md | Gather requirements, generate SLURM script, deploy, and submit |
| manage-job.md | Monitor, cancel, resubmit, retrieve results |
</workflows_index>
