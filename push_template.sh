#!/bin/bash
# push_template.sh
# Wrapper script for remove_template_dev_internals.py

set -e

log() {
  echo -e "\033[32m$*\033[0m"
}

ORIGINAL_DIR=$(pwd)

# Show help if no args
if [ $# -eq 0 ]; then
  # calling script with no args shows help
  $ORIGINAL_DIR/remove_template_dev_internals.py
  exit 0
fi

ARGS1="$@"

# Set temp directory
TEMP_DIR="$HOME/Documents/agent-manager-template-release"
ORIGINAL_DIR=$(pwd)
log "create $TEMP_DIR"
cd "$HOME/Documents"
rm -rf "$TEMP_DIR" > /dev/null 2>&1
log clone main repo
git clone https://github.com/mickeyperlstein/agent-manager-template.git "$TEMP_DIR"
cd "$TEMP_DIR"
log current directory: $(pwd)
log git fetch origin
git fetch origin
log git merge latest changes from dev
git merge origin/dev || true
log remove template dev internals

$ORIGINAL_DIR/remove_template_dev_internals.py $ARGS1
log git status
git status

log cleanup in https://github.com/mickeyperlstein/agent-manager-template/
