import os
import re
import json
import shutil
import datetime
import getpass
import platform
from pathlib import Path

# Paths
SCRIPT_DIR = Path(__file__).resolve().parent
BASE_DIR = SCRIPT_DIR.parent
DEFAULT_DATA_DIR = BASE_DIR / "data_files"
BACKUP_DIR = DEFAULT_DATA_DIR / "backups"
LOGS_DIR = SCRIPT_DIR / "logs"
SAVED_DIRS_FILE = SCRIPT_DIR / "saved_dirs.json"

def get_last_editor(file_path):
    try:
        if platform.system() != 'Windows':
            import pwd
            return pwd.getpwuid(os.stat(file_path).st_uid).pw_name
        else:
            return os.getlogin()
    except Exception:
        return "unknown_user"

def get_log_filename(username):
    now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    return LOGS_DIR / f"{now}_{username}.log"

def create_log_file(username):
    log_filename = get_log_filename(username)
    return open(log_filename, 'a', encoding='utf-8'), log_filename

def load_saved_dirs():
    if SAVED_DIRS_FILE.exists():
        with open(SAVED_DIRS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_directory_to_list(path):
    saved = load_saved_dirs()
    if path not in saved:
        saved.append(path)
        with open(SAVED_DIRS_FILE, 'w', encoding='utf-8') as f:
            json.dump(saved, f, indent=2)

def select_directory():
    print("Use default directory (/Automation_Tools/data_files)?")
    use_default = input("Type 'y' for yes, or any other key to choose another directory: ").strip().lower()

    if use_default == 'y':
        return str(DEFAULT_DATA_DIR)

    saved_dirs = load_saved_dirs()
    if saved_dirs:
        print("\nSaved Directories:")
        for idx, dir_path in enumerate(saved_dirs, 1):
            print(f"{idx}. {dir_path}")
        print(f"{len(saved_dirs)+1}. Specify a new directory")

        try:
            choice = int(input("Select a number from the menu: ").strip())
            if 1 <= choice <= len(saved_dirs):
                return saved_dirs[choice - 1]
        except ValueError:
            pass

    new_dir = input("Enter the full path to the directory you want to search: ").strip()
    if os.path.isdir(new_dir):
        save = input("Would you like to save this directory for future use? (y/n): ").strip().lower()
        if save == 'y':
            save_directory_to_list(new_dir)
        return new_dir
    else:
        print("Invalid directory. Exiting.")
        exit(1)

def search_string_in_files(root_dir, search_str):
    matches = []
    index = 1

    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if not file.lower().endswith(".txt"):
                continue

            file_path = os.path.join(subdir, file)
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()
                    for i, line in enumerate(lines):
                        if search_str in line:
                            matches.append({
                                'index': index,
                                'file': file_path,
                                'line_number': i + 1,
                                'line': line.rstrip('\n'),
                            })
                            index += 1
            except Exception as e:
                print(f"Could not read {file_path}: {e}")
    return matches

def display_matches(matches):
    for m in matches:
        print(f"{m['index']}: File: {m['file']} [Line {m['line_number']}] => {m['line']}")

def backup_file(path):
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = os.path.basename(path)
    backup_path = BACKUP_DIR / f"{filename}.{timestamp}.bak"
    shutil.copy2(path, backup_path)
    print(f"Backup created: {backup_path}")

def get_latest_backup(file_path):
    filename = Path(file_path).name
    backups = sorted(BACKUP_DIR.glob(f"{filename}.*.bak"), reverse=True)
    return backups[0] if backups else None

def restore_latest_backup(file_path):
    latest_backup = get_latest_backup(file_path)
    if not latest_backup:
        print("No backup found to restore.")
        return False

    shutil.copy2(latest_backup, file_path)
    print(f"Restored from backup: {latest_backup}")
    return True

def log_change(log_file, file_path, line_number, original, updated):
    log_file.write(f"[FILE]: {file_path}\n")
    log_file.write(f"[LINE]: {line_number}\n")
    log_file.write(f"[CHANGE]:\n!!**{original.strip()}**!! --> !!**{updated.strip()}**!!\n")
    log_file.write("-" * 60 + "\n")

def modify_line(match, action, log_file):
    file_path = match['file']
    line_number = match['line_number']
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()

    backup_file(file_path)
    original_line = lines[line_number - 1].rstrip('\n')
    updated_line = original_line

    if action == "1":
        old_val = input("Enter value to replace: ")
        new_val = input("Enter new value: ")
        updated_line = original_line.replace(old_val, new_val)
    elif action == "2":
        updated_line = ""
    elif action == "3":
        updated_line = input("Enter new line: ")
    elif action == "4":
        print("Rolling back from latest backup...")
        if restore_latest_backup(file_path):
            return
        else:
            print("No backup available.")
            return
    else:
        print("Invalid option. Skipping.")
        return

    lines[line_number - 1] = updated_line + '\n'
    with open(file_path, 'w', encoding='utf-8', errors='ignore') as f:
        f.writelines(lines)

    if action in ["1", "2", "3"]:
        log_change(log_file, file_path, line_number, original_line, updated_line)

    print(f"Updated: {file_path}")

def rollback_menu():
    print("\nRollback: Restore from latest backups in data_files/backups")
    backup_files = sorted(BACKUP_DIR.glob("*.bak"), reverse=True)
    if not backup_files:
        print("No backups available.")
        return

    file_map = {}
    print("\nAvailable backups:")
    for i, b in enumerate(backup_files, 1):
        original = ".".join(b.name.split(".")[:-2])
        print(f"{i}. Restore '{original}' from backup: {b.name}")
        file_map[i] = (original, b)

    choice = input("\nEnter number(s) to restore (comma-separated), or 'a' to restore all: ").strip()
    if choice.lower() == 'a':
        restored = set()
        for orig, b in file_map.values():
            if orig not in restored:
                shutil.copy2(b, DEFAULT_DATA_DIR / orig)
                print(f"Restored {orig} from {b.name}")
                restored.add(orig)
    else:
        indexes = [int(i.strip()) for i in choice.split(",") if i.strip().isdigit()]
        for idx in indexes:
            if idx in file_map:
                orig, b = file_map[idx]
                shutil.copy2(b, DEFAULT_DATA_DIR / orig)
                print(f"Restored {orig} from {b.name}")

def main():
    print("\nWhat would you like to do?")
    print("1. Edit files")
    print("2. Rollback files from backup")
    action = input("Select 1 or 2: ").strip()

    if action == '2':
        rollback_menu()
        return
    elif action != '1':
        print("Invalid selection. Exiting.")
        return

    root_dir = select_directory()
    search_str = input("Enter the string to search for: ").strip()
    matches = search_string_in_files(root_dir, search_str)

    if not matches:
        print("No matches found.")
        return

    display_matches(matches)

    selection = input("\nEnter number(s) of the lines to modify (comma-separated): ")
    selected_indexes = [int(i.strip()) for i in selection.split(',') if i.strip().isdigit()]

    username = get_last_editor(matches[0]['file'])
    log_file, log_path = create_log_file(username)

    print("\nOptions:\n1. Edit part of the string\n2. Delete the line\n3. Manually edit the whole line\n4. Roll back from latest backup")

    for sel in selected_indexes:
        match = next((m for m in matches if m['index'] == sel), None)
        if not match:
            print(f"Invalid selection: {sel}")
            continue

        print(f"\nSelected: {match['file']} [Line {match['line_number']}]")
        print(f"Line content: {match['line']}")
        sub_action = input("Choose an action [1-4]: ").strip()

        modify_line(match, sub_action, log_file)

    log_file.close()
    print(f"\nEdits completed. Log saved to: {log_path}")

if __name__ == "__main__":
    main()
