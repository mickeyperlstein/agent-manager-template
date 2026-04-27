#!/bin/bash
# push_template.sh
# Wrapper script for push_template.py

set -e

# Set temp directory
TEMP_DIR="~/Documents/agent-manager-template-release"
ORIGINAL_DIR=$(pwd)
#create temp dir
cd ~/Documents
rm -rf $TEMP_DIR
git clone https://github.com/mickeyperlstein/agent-manager-template.git $TEMP_DIR
cd $TEMP_DIR
#update states
git fetch origin
#merge latest changes
git merge origin/main
$ORIGINAL_DIR/push_template.py $@



echo "Created temp directory: $TEMP_DIR"

# Run the Python script
ARGS1="$@"
python3 push_template.py $ARGS1

echo "cleanup in https://github.com/mickeyperlstein/agent-manager-template/"
