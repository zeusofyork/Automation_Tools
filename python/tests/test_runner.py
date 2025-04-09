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
    MODIFIED_FILE.write_text("This line was modified.\n")

    # Simulate restoring from backup
    shutil.copy2(TEST_FILE, backup_path)
    shutil.copy2(backup_path, MODIFIED_FILE)

    # Check integrity
    restored_checksum = md5(MODIFIED_FILE)
    assert original_checksum == restored_checksum, "MD5 mismatch after restore"

    print("✅ File restored successfully and matches original")

if __name__ == "__main__":
    run_test()
