# 🛠 Automation Tools - Text File Editor & Backup Manager

![CI](https://github.com/zeusofyork/Automation_Tools/actions/workflows/test-edit-restore.yml/badge.svg)

A terminal-based tool for safely searching and editing `.txt` files with backup, restore, and rollback capabilities.

---

## 🚀 Features

- 🔍 Search text files for matching strings
- ✏️ Edit individual or all matched lines:
  - Replace part of a line
  - Replace the full line
  - Delete the line
- 🔁 Batch edit with `*` to update all matches at once
- 🧱 Saves timestamped `.bak` backups in `data_files/backups/`
- 🧪 Rollback to the most recent `.bak` for any file
- 🗃 Tracks all changes in per-user `logs/`
- 🧭 Save and reuse directories for future searches
- ✅ GitHub Actions CI:
  - Lints your code
  - Simulates edits and restoration
  - Verifies using MD5 checksums
  - Cleans up backup files
- 🔒 Pre-commit Git hook to prevent accidental commits of `.bak` files

---

## 📁 Project Structure

```
Automation_Tools/
├── data_files/
│   ├── backups/              # Stores .bak files
│   └── .gitkeep              # Placeholder to keep folder in Git
├── python/
│   ├── search_edit.py        # Main script
│   └── tests/
│       ├── test_runner.py    # Test automation with md5 restore checks
│       └── test_data_files/
│           └── example.txt   # Sample file for automated test
├── .github/
│   └── workflows/
│       └── test-edit-restore.yml
└── README.md
```

---

## ▶️ Usage

Run the script:

```bash
python python/search_edit.py
```

Choose to:
- Edit files (with full backup and logging)
- Rollback from backup files

When editing:
- Use comma-separated line numbers to edit individually
- Use `*` to batch-edit all matches with a single action

---

## 🧪 Run Tests Locally

```bash
python python/tests/test_runner.py
```

This test:
- Edits a file
- Restores it from a `.bak`
- Confirms the restore using MD5 checksum match

---

## 🚫 Git Pre-Commit Hook

To prevent accidental commits of `.bak` files:

1. Add this to `.gitignore`:

```gitignore
*.bak
```

2. Use the `pre-commit` hook script:

```bash
# .git/hooks/pre-commit
#!/bin/bash

bak_files=$(git diff --cached --name-only | grep '\.bak$')

if [[ -n "$bak_files" ]]; then
  echo "⚠️  The following .bak files are staged:"
  echo "$bak_files"
  read -p "Delete these files before commit? [y/N]: " confirm
  if [[ "$confirm" =~ ^[Yy]$ ]]; then
    for file in $bak_files; do
      git rm --cached "$file"
      rm -f "$file"
      echo "🗑️  Deleted $file"
    done
  else
    echo "❌ Commit aborted."
    exit 1
  fi
fi
```

Make it executable:

```bash
chmod +x .git/hooks/pre-commit
```

---

## 🛠 GitHub Actions Workflow

The included GitHub Actions workflow:

- Checks for Python syntax errors using `flake8`
- Runs `test_runner.py` to simulate edit/restore
- Confirms file integrity using MD5 checksums
- Deletes `.bak` files after test

You’ll find this in:

```
.github/workflows/test-edit-restore.yml
```

---

## 🧠 Coming Soon Ideas

- GUI with Tkinter
- Configurable `.ini`/`.env` for default settings
- Test coverage badge
- GitHub release automation with zipped logs/backups

---
