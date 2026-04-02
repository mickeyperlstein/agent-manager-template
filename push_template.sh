#!/bin/bash
# push_template.sh
# Bumps minor version, syncs current state to the main (template) branch.
# Stages everything except Features/, meetings/, and tasks.csv, then force-pushes to main.

set -e

VERSION_FILE="template_workflow/version.json"

# Bump minor version
current=$(python3 -c "import json; v=json.load(open('$VERSION_FILE'))['version'].split('.'); v[1]=str(int(v[1])+1); v[2]='0'; print('.'.join(v))")
python3 -c "import json; d=json.load(open('$VERSION_FILE')); d['version']='$current'; json.dump(d, open('$VERSION_FILE','w'))"
echo "Version bumped to $current"

# Stage everything
git add .

# Remove Features/, meetings/, and tasks.csv from the staging area
git restore --staged Features/ 2>/dev/null && echo "  Excluded Features/" || true
git restore --staged meetings/ 2>/dev/null && echo "  Excluded meetings/" || true
git restore --staged tasks.csv 2>/dev/null && echo "  Excluded tasks.csv" || true

# Commit
git commit -m "chore: release template v$current"

# Force push to main
git push origin HEAD:main --force

echo ""
echo "Done. main is now template v$current."
