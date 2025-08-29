# Submodule Sync Utility

A lightweight Python script to automate committing, pushing, and updating Git submodules (including nested ones) from a single “parent” repo.

## Table of Contents

- [Overview](#overview)  
- [Prerequisites](#prerequisites)  
- [Getting Started](#getting-started)  
  - [Clone this repository](#clone-this-repository)  
  - [Add your submodules](#add-your-submodules)  
  - [Install and run the sync script](#install-and-run-the-sync-script)  
- [How It Works](#how-it-works)  
- [Configuration](#configuration)  
  - [Public vs. Private submodules](#public-vs-private-submodules)  
- [Troubleshooting](#troubleshooting)  
- [License](#license)

## Overview

When you have a “monorepo” or a larger project that pulls in several smaller repos as submodules (even nested submodules), the manual workflow of entering each folder, committing, pushing, then updating the parent’s SHA reference can be tedious.  
This script:

1. Finds all submodules (recursively)  
2. Commits & pushes any local changes within each submodule  
3. Updates the submodule pointers (SHAs) in the root repo and pushes them  

Run one command and everything stays in sync.

## Prerequisites

- Git (2.13+ recommended)  
- Python 3.x (tested on 3.6+)  
- Unix-like shell (Linux, macOS, WSL) or Git Bash on Windows  

## Getting Started

### Clone this repository

```bash
git clone --recurse-submodules <YOUR_NEW_REPO_URL>
cd <YOUR_NEW_REPO_NAME>
```

> If you forget `--recurse-submodules`, you can later run:
> ```bash
> git submodule update --init --recursive
> ```

### Add your submodules

To add a new submodule (public or private):

```bash
git submodule add <URL-TO-SMALL-REPO> path/to/submodule
git commit -m "feat: add submodule at path/to/submodule"
git push
```

Repeat for any nested submodules inside those repos as needed.

### Install and run the sync script

1. Make the Python script executable:
   ```bash
   chmod +x sync_submodules_recursive.py
   ```

2. Run it from the root of **this** repository:
   ```bash
   ./sync_submodules_recursive.py
   ```

   The script will:
   1. Commit & push changes in each submodule (skipping if no changes).  
   2. Stage all submodule folder pointers in the root repo, commit & push once.

## How It Works

- **Detection**  
  Uses `git submodule status --recursive` to list every submodule path.

- **Inside each submodule**  
  ```bash
  git add .
  git commit -m "chore: sync local changes in submodule"
  git push
  ```
  Errors are caught and skipped if there’s nothing to commit.

- **Back in root repo**  
  ```bash
  git add <each-submodule-path>
  git commit -m "chore: update submodule pointers"
  git push
  ```

## Configuration

No additional configuration is needed: the script works out-of-the-box.

### Public vs. Private submodules

- Public: Use HTTPS or SSH URL, no extra step.  
- Private: Prefer SSH URLs (`git@github.com:…`) and ensure your SSH key is loaded (`ssh-agent`).  
  If you prefer HTTPS, configure a credential helper or provide a personal access token.

## Troubleshooting

- “Permission denied” when running the script  
  - Ensure you ran `chmod +x sync_submodules_recursive.py`.  
  - Verify your shell is executing `./sync_submodules_recursive.py`, not a stray file.

- SSH authentication failures  
  - Check `ssh-add -l` to confirm your key is loaded.  
  - Test with `git ls-remote <private-submodule-url>`.

- Script exits early with an error  
  - Read the printed stderr; the script aborts on any unexpected Git failure.  
  - Fix the underlying Git error in the indicated repo or path, then retry.

## License

This project is released under the MIT License. See [LICENSE](LICENSE) for details.
