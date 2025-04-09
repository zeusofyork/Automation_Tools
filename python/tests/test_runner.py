import hashlib
import shutil
from pathlib import Path

# Correct path references relative to project root
BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data_files"
BACKUP_DIR = DATA_DIR / "backups"
TEST_FILE = DATA_DIR / "example.txt"
MODIFIED_FILE = DATA_DIR / "example_modified.txt"

def md5(path):
    return hashlib.md5(path.read_bytes()).hexdigest()

def run_test():
    # Create test file if not present
    TEST_FILE.write_text("Line 1\nLine 2\nLine 3\n", encoding="utf-8")

    original_checksum = md5(TEST_FILE)
    backup_path = BACKUP_DIR / f"{TEST_FILE.name}.bak"

    # Ensure backup dir exists
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)

    # Backup file
    shutil.copy2(TEST_FILE, backup_path)

    # Modify the file
    MODIFIED_FILE.write_text("MODIFIED\n" + TEST_FILE.read_text(), encoding="utf-8")
    shutil.copy2(MODIFIED_FILE, TEST_FILE)

    # Confirm it's different
    modified_checksum = md5(TEST_FILE)
    assert original_checksum != modified_checksum, "File not modified for test"

    # Restore the backup
    shutil.copy2(backup_path, TEST_FILE)

    # Confirm it's restored
    restored_checksum = md5(TEST_FILE)
    assert original_checksum == restored_checksum, "Restoration failed"

    print("✅ Test passed: Backup, modify, and restore")

if __name__ == "__main__":
    run_test()
