from pathlib import Path

base_dir = Path.cwd()
dirs_to_create = [
    base_dir / "python" / "tests" / "test_data_files",
    base_dir / ".github" / "workflows",
    base_dir / "data_files" / "backups"
]

files_to_create = {
    base_dir / "python" / "tests" / "test_data_files" / "example.txt": (
        "This is a test file.\n"
        "It has multiple lines.\n"
        "Use this for backups.\n"
    ),
    base_dir / "python" / "tests" / "test_runner.py": '''
import hashlib
import shutil
from pathlib import Path

DATA_DIR = Path(__file__).parent / "test_data_files"
BACKUP_DIR = Path(__file__).parents[1] / "data_files/backups"
TEST_FILE = DATA_DIR / "example.txt"
MODIFIED_FILE = DATA_DIR / "example_modified.txt"

def md5(path):
    return hashlib.md5(path.read_bytes()).hexdigest()

def run_test():
    original_checksum = md5(TEST_FILE)
    backup_path = BACKUP_DIR / f"{TEST_FILE.name}.bak"

    # Simulate edit
    shutil.copy2(TEST_FILE, MODIFIED_FILE)
    MODIFIED_FILE.write_text("This line was modified.\\n")

    # Simulate restoring from backup
    shutil.copy2(TEST_FILE, backup_path)
    shutil.copy2(backup_path, MODIFIED_FILE)

    # Check integrity
    restored_checksum = md5(MODIFIED_FILE)
    assert original_checksum == restored_checksum, "MD5 mismatch after restore"

    print("✅ File restored successfully and matches original")

if __name__ == "__main__":
    run_test()
''',
    base_dir / ".github" / "workflows" / "test-edit-restore.yml": '''
name: Test Edit & Restore Flow

on: [push, pull_request]

jobs:
  check-and-test:
    runs-on: ubuntu-latest

    steps:
      - name: 📦 Checkout code
        uses: actions/checkout@v3

      - name: 🐍 Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: 3.10

      - name: ✅ Install dependencies
        run: pip install flake8

      - name: 🔍 Lint the script
        run: flake8 python/search_edit.py

      - name: 🚧 Run test script
        run: python python/tests/test_runner.py

      - name: 🧹 Clean .bak files after test
        run: |
          find data_files/backups -name "*.bak" -delete
''',
    base_dir / "data_files" / ".gitkeep": ""
}

# Create directories
for directory in dirs_to_create:
    directory.mkdir(parents=True, exist_ok=True)

# Create and write files
for file_path, content in files_to_create.items():
    file_path.write_text(content.strip() + '\n')

"✅ Setup script has created test structure, GitHub workflow, and example files."

