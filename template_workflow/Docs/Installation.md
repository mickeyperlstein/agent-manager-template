# Installation Guide

This guide covers three scenarios: **new projects**, **existing projects**, and **updating an existing install**.

---

## Scenario 1: New Project

If you're starting a new project and want the full template:

```bash
# Clone the template
mkdir my-project
cd my-project

# Remove template's git history and start fresh
git init

```
# continue to next scenario (You now have a working repo/existing Project) 
---

## Scenario 2: In your existing project

Add the template to your existing project **this will preserve all existing files in your code**:

### Step 1: Add template as a remote called "template"
```bash
git remote add template https://github.com/mickeyperlstein/agent-manager-template.git
```

### Step 2: Checkout all template files from "template" remote

```bash
git fetch template main
git checkout template/main -- .
```

This pulls all template files. Your existing project files (Features/, meetings/, tasks.csv) are preserved.

### Step 3: Handle agent rule conflicts (if any)

If you already have `CLAUDE.md`, `.clinerules`, or `.windsurfrules`, git will show conflicts.

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

**Note:** `tasks.csv` is tracked in git so it can be synced to Google Drive, GitHub Projects, or other external systems. Do not ignore it.

### Step 5: Install ai agents

    # Run onboarding for your agent (Claude, Windsurf, or Cline)
    ./template_workflow/scripts/claude_onboarding.sh
    ./template_workflow/scripts/windsurf_onboarding.sh
    ./template_workflow/scripts/cline_onboarding.sh


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

# Pull all template files (Features/, meetings/, tasks.csv are excluded by push_template.sh)
git checkout template/main -- .

# Resolve conflicts (if any) in CLAUDE.md, .clinerules, .windsurfrules
# These files have markers for easy merging

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

**Q: Checkout says "would overwrite" my files**
- You have untracked files with the same names. Commit or stash them first: `git stash`
- Or specify only the files you want: `git checkout template/main -- template_workflow/`

**Q: I have conflicts in CLAUDE.md or .clinerules**
- Resolve manually — look for `<<<<<<< HEAD` markers
- Files use `### AGENT_MANAGER_TEMPLATE_START/END` comments to show template sections
- Keep both versions (yours + template) or merge the template section into your file

**Q: setup.sh says "command not found"**
- Ensure you're in the project root (where setup.sh is)
- Make it executable: `chmod +x setup.sh`

**Q: Which branch do I pull from?**
- Always use `main` (the clean template branch — safe for all projects)
- Never pull from `dev` (the working branch with examples)
