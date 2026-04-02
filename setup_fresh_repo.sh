#!/bin/bash

# Setup script for fresh Perli monorepo structure
# Run this in the new perli directory after moving old repo

set -e

echo "Creating Perli monorepo directory structure..."

# Core directories
mkdir -p FE/Bracelet
mkdir -p FE/shared  
mkdir -p FE/Guardian
mkdir -p FE/Docs

mkdir -p BE/services
mkdir -p BE/Docs

mkdir -p Marketing
mkdir -p Docs
mkdir -p Architecture
mkdir -p Tasks
mkdir -p meetings
mkdir -p ai_info

mkdir -p Features/Current
mkdir -p Features/Done
mkdir -p Features/Backlog

# Development directories
mkdir -p FE/packages
mkdir -p Plans
mkdir -p .windsurf/workflows
mkdir -p tools
mkdir -p monitoring
mkdir -p deployments
mkdir -p .vscode
mkdir -p submits
mkdir -p .github/workflows
mkdir -p e2e
mkdir -p test
mkdir -p scripts

echo "Creating basic files..."

# README.md
cat > README.md << 'EOF'
# Perli Monorepo

## Overview
Perli system for kids' safety with Wi-Fi location tracking, security rule engine, and guardian notifications.

## Structure
- `FE/`: Frontend applications (Flutter)
  - `Bracelet/`: Android bracelet app
  - `shared/`: Shared location/Wi-Fi internals
  - `Guardian/`: iOS/Android guardian app
- `BE/`: Backend services (Node.js)
- `packages/`: Shared Flutter packages
- `Plans/`: Windsurf development plans
- `e2e/`: End-to-end tests
- `docs/`: Documentation
- `monitoring/`: Internal monitoring dashboards

## Development
Follow Windsurf rules: TDD, small testable chunks, e2e tests required for sprint completion.

## Setup
[Setup instructions to be added]
EOF

# .gitignore
cat > .gitignore << 'EOF'
# Dependencies
node_modules/
**/node_modules

# Build artifacts
build/
dist/
*.apk
*.ipa

# Logs
*.log
logs/

# IDE
.vscode/settings.json
.idea/

# OS
.DS_Store
Thumbs.db

# Environment
.env
.env.local

# Temporary files
*.tmp
*.swp
EOF

# Basic .windsurf/workflows placeholder
touch .windsurf/workflows/.gitkeep

# Basic placeholders for required directories
touch packages/.gitkeep
touch Plans/.gitkeep
touch tools/.gitkeep
touch monitoring/.gitkeep
touch deployments/.gitkeep
touch submits/.gitkeep
touch e2e/.gitkeep
touch test/.gitkeep
touch scripts/.gitkeep

echo "Fresh Perli monorepo structure created!"
echo "Initializing git repository..."

# Initialize git repo
git init
git add .
git commit -m "Initial monorepo structure"

echo "Git repository initialized with initial commit."

# ============================================================================
# SUBTREE BOOTSTRAP: UPSTREAM TRACCAR-CLIENT → FE/shared
# ============================================================================

echo ""
echo "Embedding upstream traccar-client into FE/shared via subtree..."
git remote add upstream-traccar https://github.com/traccar/traccar-client.git
git subtree add --prefix=FE/shared upstream-traccar main --squash
echo "FE/shared bootstrapped from upstream traccar-client."
echo ""
echo "To pull future upstream updates: git subtree pull --prefix=FE/shared upstream-traccar main --squash"

# ============================================================================
# ADDITIONS — claude-sonnet-4-6
# ============================================================================

echo "Creating additional structure (claude-sonnet-4-6)..."

# ai_information matches path referenced in meeting notes and agent files
mkdir -p ai_information/agents
mkdir -p ai_information/commands-skills

# CONTRIBUTING.md referenced in 2026-04-01 meeting notes (IoC, minimal intrusion rules)
cat > CONTRIBUTING.md << 'EOF'
# Contributing

## Development Rules
- IoC pattern: minimal intrusion on files you didn't create
- One-line changes max on upstream/shared files
- TDD: write tests first, small testable chunks
- e2e tests required for sprint completion

## Upstream (FE/shared)
- Based on traccar-client upstream
- To pull updates: `git subtree pull --prefix=FE/shared upstream-traccar main --squash`
- Keep Wi-Fi/BT additions isolated — do not modify upstream internals inline
EOF

# Windsurf rules placeholder
cat > .windsurf/rules.md << 'EOF'
# Windsurf Rules

- TDD: tests before implementation
- Small testable chunks only
- e2e tests required before sprint close
- IoC pattern for backend services
- No inline logic in shared/upstream files
EOF

touch ai_information/agents/.gitkeep
touch ai_information/commands-skills/.gitkeep

echo ""
echo "Setup complete! Ready for clean component commits."
