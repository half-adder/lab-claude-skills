# McKay Lab Claude Code Skills

Shared [Claude Code](https://claude.ai/claude-code) skills for the McKay Lab. These provide domain-specific capabilities for common research workflows.

## Available Skills

| Skill | Directory | Description |
|-------|-----------|-------------|
| `ncbi-datasets` | `ncbi/` | Query and download biological sequence data from NCBI using the `datasets` and `dataformat` CLI tools. Includes Drosophila cytological band lookups with subdivision-level resolution. |
| `deploy-hpc-job` | `deploy-hpc-job/` | Deploy and manage jobs on HPC clusters via SLURM. Supports Python/uv, R, Nextflow, and module-based tools (samtools, STAR, etc.). Handles SLURM script generation, lmod modules, rsync deployment, and job management. Configurable per-user via `cluster-config.toml`. |

## Setup

```bash
curl -fsSL https://raw.githubusercontent.com/half-adder/lab-claude-skills/main/setup.sh | bash
```

Or clone manually and run:

```bash
git clone git@github.com:half-adder/lab-claude-skills.git ~/code/lab-claude-skills
~/code/lab-claude-skills/setup.sh
```

Some skills require per-user configuration. The skill will walk you through this on first use, or you can set it up manually:

```bash
# For the HPC skill, copy and edit the cluster config:
cd ~/code/lab-claude-skills/deploy-hpc-job
cp cluster-config.example.toml cluster-config.toml
# Edit cluster-config.toml with your SSH host, username, scratch path, and email
```

## Updating

Skills are symlinked to the cloned repo, so updating is just a `git pull`:

```bash
cd ~/code/lab-claude-skills && git pull
```

Existing skills update immediately since Claude Code reads them through the symlinks. If new skills or slash commands were added, re-run the setup script to pick them up:

```bash
~/code/lab-claude-skills/setup.sh
```

## Usage

Invoke a skill via its slash command:

```
/ncbi-datasets download the Drosophila melanogaster reference genome
/ncbi-datasets get GenBank for band 68C13
/ncbi-datasets look up gene Ubx in Drosophila
```

Or just type `/ncbi-datasets` for an interactive menu. Each skill will guide you through installing any required CLI tools on first use.

## Adding New Skills

Each skill lives in its own directory with a `SKILL.md` entry point. See the [Claude Code docs](https://docs.anthropic.com/en/docs/claude-code/skills) or use the `/create-agent-skills` skill for guidance.
