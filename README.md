# McKay Lab Claude Code Skills

Shared [Claude Code](https://claude.ai/claude-code) skills for the McKay Lab. These provide domain-specific capabilities for common research workflows.

## Available Skills

| Skill | Directory | Description |
|-------|-----------|-------------|
| `ncbi-datasets` | `ncbi/` | Query and download biological sequence data from NCBI using the `datasets` and `dataformat` CLI tools. Includes Drosophila cytological band lookups with subdivision-level resolution. |

## Setup

```bash
curl -fsSL https://raw.githubusercontent.com/half-adder/lab-claude-skills/main/setup.sh | bash
```

Or clone manually and run:

```bash
git clone git@github.com:half-adder/lab-claude-skills.git ~/code/lab-claude-skills
~/code/lab-claude-skills/setup.sh
```

Re-run the setup script anytime to pull updates and pick up new skills.

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
