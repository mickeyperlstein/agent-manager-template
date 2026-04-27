#!/bin/bash
# push_template.sh
# Wrapper script for push_template.py

set -e

# Run the Python script
ARGS1="$@"
python3 push_template.py $ARGS1

echo "cleanup in https://github.com/mickeyperlstein/agent-manager-template/"
