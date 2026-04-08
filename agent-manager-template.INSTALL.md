# Installation Guide

This guide covers three scenarios: **new projects**, **existing projects**, and **updating an existing install**.

---

## Scenario 1: New Project (Cleanest)

If you're starting a new project and want the full template:

```bash
# Clone the template
git clone https://github.com/mickeyperlstein/agent-manager-template.git my-project
cd my-project

# Remove template's git history and start fresh
rm -rf .git
git init
git add .
git commit -m "Initial commit from agent-manager-template"

# Initialize the Kanban structure
bash setup.sh

# Run onboarding for your agent (Claude, Windsurf, or Cline)
./template_workflow/scripts/claude_onboarding.sh
# OR: ./template_workflow/scripts/windsurf_onboarding.sh
# OR: ./template_workflow/scripts/cline_onboarding.sh
```

---

## Scenario 2: Existing Project (Recommended)

Add the template to your existing project **without overwriting your code**:

### Step 1: Add template as a remote
```bash
git remote add template https://github.com/mickeyperlstein/agent-manager-template.git
git fetch template main
```

### Step 2: Checkout specific template files

Only pull the safe template files (not Features/, meetings/, or tasks.csv, which are project-specific):

```bash
git checkout template/main -- \
  template_workflow/ \
  setup.sh \
  agent-manager-claude.md \
  agent-manager-cline.md \
  agent-manager-template.KANBAN.md \
  .claude/commands/ \
  .windsurf/workflows/ \
  .clinerules \
  .windsurfrules
```

### Step 3: Merge agent rules

If you already have `CLAUDE.md`, `.clinerules`, or `.windsurfrules`:

The template files contain `### AGENT_MANAGER_TEMPLATE_START` and `### AGENT_MANAGER_TEMPLATE_END` markers for easy merging.

**Option A: Keep both (recommended for maintaining existing rules)**
```bash
# Rename the new template files
mv agent-manager-claude.md agent-manager-template.CLAUDE.md
mv CLAUDE.md CLAUDE.md.bak  # backup your existing file

# In your CLAUDE.md, add this after your existing content:
echo "" >> CLAUDE.md.bak
echo "See agent-manager-template.CLAUDE.md for Kanban workflow rules." >> CLAUDE.md.bak
mv CLAUDE.md.bak CLAUDE.md
```

**Option B: Merge manually**
```bash
# Edit CLAUDE.md, .clinerules, .windsurfrules and merge the template sections
# marked with ### AGENT_MANAGER_TEMPLATE_START/END
```

### Step 4: Create Kanban structure

```bash
bash setup.sh
```

This creates the Features/ column folders and makes scripts executable.

### Step 5: Update .gitignore

Add these lines to `.gitignore` if not present:
```
meetings/
tasks.csv
Features/**/temp_*
.DS_Store
```

### Step 6: Commit

```bash
git add .
git commit -m "Add agent-manager-template workflow"
```

---

## Scenario 3: Updating an Existing Install

If you already have the template and want to pull the latest version:

```bash
# Fetch latest from template repo
git fetch template main

# Review what changed
git diff HEAD template/main -- template_workflow/

# Pull just the template files (not Features/, meetings/, tasks.csv)
git checkout template/main -- \
  template_workflow/ \
  agent-manager-template.KANBAN.md \
  agent-manager-claude.md \
  agent-manager-cline.md \
  setup.sh

# Review and merge agent rule changes (if any)
git diff HEAD agent-manager-claude.md
git diff HEAD .clinerules
git diff HEAD .windsurfrules

# Commit the update
git commit -m "Update agent-manager-template to latest version"
```

---

## Maintenance

### Rebuild task.csv from Features/ structure

After creating or moving features:
```bash
python3 template_workflow/scripts/folders_to_csv.py
```

This regenerates `tasks.csv` from the Features/ folder structure. Use it to sync with Google Sheets or GitHub Projects.

### Run Kanban housekeeping

Automatically runs at startup, or manually:
```bash
/housekeeping
```

Prunes empty epic folders and moves stragglers (feature files stuck in the wrong stage).

### Make scripts executable

After checking out scripts:
```bash
chmod +x template_workflow/scripts/*.py
chmod +x template_workflow/scripts/*.sh
```

Or run `setup.sh` which does this automatically.

---

## Troubleshooting

**Q: Git won't let me checkout specific files from template/main**
- Ensure you ran `git fetch template main` first
- Try: `git checkout -b temp template/main` then `git checkout HEAD -- <files>`, then `git checkout dev`

**Q: I have conflicts in CLAUDE.md or .clinerules**
- Both files use marker comments (`### AGENT_MANAGER_TEMPLATE_START/END`)
- Copy the template section into your file between the markers, or keep them separate (rename template to `agent-manager-template.CLAUDE.md`)

**Q: setup.sh says "command not found"**
- Ensure you're in the project root (where setup.sh is)
- Make it executable: `chmod +x setup.sh`

**Q: Which branch do I pull from?**
- Always use `main` (the template branch, kept clean by `push_template.sh`)
- Never pull `dev` (the working branch with examples)
