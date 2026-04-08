#!/usr/bin/env bash
set -euo pipefail

REPO_URL="git@github.com:half-adder/lab-claude-skills.git"
INSTALL_DIR="${HOME}/code/lab-claude-skills"
SKILLS_DIR="${HOME}/.claude/skills"
COMMANDS_DIR="${HOME}/.claude/commands"

# Clone if not already present
if [ -d "$INSTALL_DIR" ]; then
    echo "Already cloned at $INSTALL_DIR, pulling latest..."
    git -C "$INSTALL_DIR" pull
else
    echo "Cloning to $INSTALL_DIR..."
    mkdir -p "$(dirname "$INSTALL_DIR")"
    git clone "$REPO_URL" "$INSTALL_DIR"
fi

# Symlink skills
mkdir -p "$SKILLS_DIR"
for skill_dir in "$INSTALL_DIR"/*/; do
    name=$(basename "$skill_dir")
    # Skip non-skill directories
    [ "$name" = "commands" ] && continue
    [ ! -f "$skill_dir/SKILL.md" ] && continue

    if [ -L "$SKILLS_DIR/$name" ]; then
        echo "Skill '$name' already linked, skipping."
    elif [ -e "$SKILLS_DIR/$name" ]; then
        echo "WARNING: $SKILLS_DIR/$name exists but is not a symlink. Skipping."
    else
        ln -s "$skill_dir" "$SKILLS_DIR/$name"
        echo "Linked skill: $name"
    fi
done

# Copy slash commands
mkdir -p "$COMMANDS_DIR"
for cmd in "$INSTALL_DIR"/commands/*.md; do
    [ ! -f "$cmd" ] && continue
    name=$(basename "$cmd")
    if [ -f "$COMMANDS_DIR/$name" ]; then
        echo "Command '$name' already exists, skipping."
    else
        cp "$cmd" "$COMMANDS_DIR/$name"
        echo "Installed command: $name"
    fi
done

echo ""
echo "Done! Skills are ready to use in Claude Code."
echo "Run /ncbi-datasets to get started."
