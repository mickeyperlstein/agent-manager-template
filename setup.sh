#!/bin/bash
# setup.sh — initialize a fresh agent-manager project
# Run once after cloning from template.

set -e

echo "Setting up agent-manager project..."

# Create Kanban column folders
COLUMNS=(
  "Features/1-Backlog"
  "Features/2-HLD"
  "Features/3-HLD-Review"
  "Features/4-Task"
  "Features/5-TaskReview"
  "Features/6-Implementation"
  "Features/7-Test"
  "Features/8-Review"
  "Features/9-Done"
)

for col in "${COLUMNS[@]}"; do
  mkdir -p "$col"
  touch "$col/.gitkeep"
done

echo "  Created Features/ column structure"

chmod +x template_workflow/scripts/*.py
chmod +x template_workflow/scripts/*.sh

echo "  Scripts ready at template_workflow/scripts/"

echo ""
echo "Done. Next steps:"
echo "  1. Add your first feature stub to Features/1-Backlog/{feature}.md"
echo "  2. Read template_workflow/Agent-HowTos/Kanban.md for the workflow"
echo "  3. Configure your agent rules in CLAUDE.md / .clinerules / .windsurfrules"
