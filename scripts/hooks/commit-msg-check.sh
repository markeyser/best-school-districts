#!/bin/sh

# Define the regex pattern for branch names
BRANCH_NAME_REGEX="^(feature|bugfix|data|experiment|model|docs|refactor|test|chore|hotfix|performance|security|build|ci|hyperparameter-tuning|preprocessing|deployment|visualization|evaluation
)\/[a-z0-9-]+-[A-Z]+-[0-9]+(-subtask-[0-9]+)?$"

# Get the current branch name
BRANCH_NAME=$(git rev-parse --abbrev-ref HEAD)

# Define exceptions for branch names
EXCEPTIONS=("dev" "production" "main")

# Check if the branch name is an exception
is_exception() {
  for exception in "${EXCEPTIONS[@]}"; do
    if [ "$BRANCH_NAME" = "$exception" ]; then
      return 0
    fi
  done
  return 1
}

# Check if this is a branch creation (args: 1 for new branch creation, 0 otherwise)
if [ "$3" = "1" ]; then
  # If the branch name is an exception, skip the pattern check
  if is_exception; then
    exit 0
  fi
