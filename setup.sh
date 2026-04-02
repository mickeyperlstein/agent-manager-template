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
  "Features/4-TaskReview"
  "Features/5-Implementation"
  "Features/6-Testing-Agent"
  "Features/7-Testing-Manual"
  "Features/8-Verified"
  "Features/9-Review"
  "Features/10-Done"
)

for col in "${COLUMNS[@]}"; do
  mkdir -p "$col"
  touch "$col/.gitkeep"
done

echo "  Created Features/ column structure"

# Create scripts/ from template
mkdir -p scripts
cp template_workflow/scripts/csv_to_folders.py scripts/
cp template_workflow/scripts/folders_to_csv.py scripts/
cp template_workflow/scripts/kanban_utils.py scripts/
chmod +x scripts/*.py
echo "  Copied sync scripts to scripts/"

# Create tasks.csv with headers only
echo "id,epic,story,state,assignee,column,type,review_gate,approved" > tasks.csv
echo "  Created tasks.csv"

# Create .gitignore
cat > .gitignore << 'EOF'
__pycache__/
*.pyc
.DS_Store
meetings/
EOF
echo "  Created .gitignore"

echo ""
echo "Done. Next steps:"
echo "  1. Add your first feature stub to Features/1-Backlog/"
echo "  2. Read template_workflow/Agent-HowTos/Kanban.md for the workflow"
echo "  3. Configure your agent rules in CLAUDE.md / .clinerules / .windsurfrules"
