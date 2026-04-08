# McKay Lab Claude Code Skills

Shared [Claude Code](https://claude.ai/claude-code) skills for the McKay Lab. These provide domain-specific capabilities for common research workflows.

## Available Skills

| Skill | Directory | Description |
|-------|-----------|-------------|
| `ncbi-datasets` | `ncbi/` | Query and download biological sequence data from NCBI using the `datasets` and `dataformat` CLI tools. Includes Drosophila cytological band lookups with subdivision-level resolution. |

## Setup

1. Clone this repo:
   ```bash
   git clone git@github.com:seanjohnsen/lab-claude-skills.git ~/code/lab-claude-skills
   ```

2. Symlink the skills you want into your Claude Code skills directory:
   ```bash
   mkdir -p ~/.claude/skills
   ln -s ~/code/lab-claude-skills/ncbi ~/.claude/skills/ncbi-datasets
   ```

3. Copy the slash command(s) to your commands directory:
   ```bash
   mkdir -p ~/.claude/commands
   cp ~/code/lab-claude-skills/commands/* ~/.claude/commands/
   ```

4. Install prerequisites for the NCBI skill:
   ```bash
   # Install datasets + dataformat CLI
   conda install -c conda-forge ncbi-datasets-cli
   # Or direct download (macOS):
   curl -o /usr/local/bin/datasets 'https://ftp.ncbi.nlm.nih.gov/pub/datasets/command-line/v2/mac/datasets'
   curl -o /usr/local/bin/dataformat 'https://ftp.ncbi.nlm.nih.gov/pub/datasets/command-line/v2/mac/dataformat'
   chmod +x /usr/local/bin/datasets /usr/local/bin/dataformat
   ```

## Usage

Invoke a skill via its slash command:

```
/ncbi-datasets download the Drosophila melanogaster reference genome
/ncbi-datasets get GenBank for band 68C13
/ncbi-datasets look up gene Ubx in Drosophila
```

Or just type `/ncbi-datasets` for an interactive menu.

## Caching

The NCBI skill caches downloaded chromosome GenBank files at `~/.cache/ncbi-datasets/gbff/` to avoid re-downloading when extracting multiple regions from the same chromosome. Clear with `rm -rf ~/.cache/ncbi-datasets/`.

## Adding New Skills

Each skill lives in its own directory with a `SKILL.md` entry point. See the [Claude Code docs](https://docs.anthropic.com/en/docs/claude-code/skills) or use the `/create-agent-skills` skill for guidance.
