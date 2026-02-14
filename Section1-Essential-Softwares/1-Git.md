
# Git Command Overview
## Introduction

Git is a distributed version control system that tracks changes in your code. This guide covers the essential commands you'll use daily for managing repositories, collaborating with teammates, and maintaining a clean project history.

## Getting Started
```bash
git config --global user.name "Your Name"
git config --global user.email "your@email.com"
git init                    # Initialize repository
```

## Basic Commands

Essential commands for daily version control workflows, including staging changes, committing work, and synchroncing with remote repositories.

```bash
git add <file>              # Stage changes
git add .                   # Stage all changes
git commit -m "message"     # Commit staged changes
git push                    # Push to remote
git pull                    # Fetch and merge remote changes
```

## Branching
```bash
git branch                  # List branches
git branch <name>           # Create branch
git checkout <branch>       # Switch branch
git checkout -b <branch>    # Create and switch branch
git merge <branch>          # Merge branch
```

## Viewing History
```bash
git log                     # View commit history
git status                  # Check repository status
git diff                    # Show unstaged changes
git show <commit>           # Show commit details
```

## Undoing Changes
```bash
git restore <file>          # Discard changes
git reset HEAD~1            # Undo last commit (keep changes)
git revert <commit>         # Create new commit undoing changes
```

## Remote
```bash
git clone <url>             # Clone repository
git remote -v               # List remote repositories
git remote add origin <url> # Add remote
```
