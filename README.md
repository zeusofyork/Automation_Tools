📁 Automation Tools - Text File Editor & Backup Manager

This tool allows you to search, edit, and manage .txt files using a powerful terminal interface with built-in backup and rollback functionality.
🔧 Features

    ✅ Search .txt files for any string

    ✅ Edit single or multiple lines:

        Replace part of a string

        Replace entire line

        Delete line

    ✅ Batch mode using * to edit all matched lines at once

    ✅ Automatically backs up files with a timestamped .bak in data_files/backups/

    ✅ Rollback from latest .bak files

    ✅ Tracks changes in per-user log files (logs/)

    ✅ Saves and recalls commonly used search directories

    ✅ Git pre-commit hook to prevent committing .bak files






<pre>
📁 Folder Structure
    Automation_Tools/ 
    ├── data_files/ # Working directory for text files │ 
    ├── backups/ # Where .bak backups are stored │ 
    └── *.txt # Dummy/editable text files 
    ├── python/ │ 
    ├── search_edit.py # Main script │ 
    ├── logs/ # Timestamped change logs │ 
    └── saved_dirs.json # Stores custom directory history 
    ├── .git/hooks/ │ 
    └── pre-commit # Prevents accidental commit of .bak files 
    └── README.md
</pre>



▶️ How to Run

From the python/ directory:

python3 search_edit.py


🧑‍💻 Edit Mode

When you run the script, choose:

1. Edit files
2. Rollback files from backup

In Edit Mode, you'll:

    Select files with match numbers or * for all

    Choose your action (replace, delete, full edit, rollback)

    Optionally select or save directories

♻️ Rollback Mode

In Rollback Mode:

    View all .bak files created

    Select one or more to restore

    Optionally restore all

🛡 Git Integration

To avoid committing temporary backups:

    Add this to .gitignore:

# Ignore all .bak files
*.bak

    Use the included pre-commit hook:

        Located in .git/hooks/pre-commit

        It detects .bak files staged for commit

        Prompts to delete them or abort the commit

🧪 Example Log

logs/2025-04-08_zeuso.log:

[FILE]: data_files/test.txt
[LINE]: 4
[CHANGE]:
!!**API_KEY = "dev"**!! --> !!**API_KEY = "prod"**!!
------------------------------------------------------------

📌 Notes

    Works only on .txt files (future versions can include additional file formats e.g. csv, html, css etc.

    Logs are saved per user per session

    Backup filenames include original name + timestamp
