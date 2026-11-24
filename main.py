import os
import json
import shutil
from pathlib import Path


# ==========================================
# 1. FILE ORGANIZER CORE LOGIC
# ==========================================
def load_config(config_filename="config.json"):
    """Loads configuration from a JSON file, or uses defaults if missing."""
    default_config = {
        "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"],
        "Documents": [".pdf", ".doc", ".docx", ".txt", ".xls", ".xlsx", ".ppt", ".pptx"],
        "Videos": [".mp4", ".mkv", ".mov", ".avi", ".wmv"],
        "Audio": [".mp3", ".wav", ".flac", ".aac", ".ogg"],
        "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
        "Code": [".py", ".js", ".ts", ".html", ".css", ".java", ".cpp", ".go", ".rs"]
    }

    config_path = Path(config_filename)
    if config_path.exists():
        try:
            with open(config_path, "r") as f:
                print(f"⚙️ Loaded custom rules from '{config_filename}'")
                return json.load(f)
        except json.JSONDecodeError:
            print(f"⚠️ Warning: '{config_filename}' is malformed JSON. Using default rules.")
    else:
        print(f"ℹ️ '{config_filename}' not found. Using default internal rules.")

    return default_config


def organize_folder(target_dir, dry_run=False):
    # Load the configuration dynamically from the JSON file
    config = load_config("config.json")

    target_path = Path(target_dir)
    if not target_path.exists():
        print(f"Error: Target directory '{target_dir}' does not exist.")
        return

    print(f"\n--- Starting File Sorter {'(DRY RUN)' if dry_run else ''} on: {target_path.resolve()} ---")

    # Initialize trackers for the final summary report
    summary = {category: 0 for category in config.keys()}
    summary["Others"] = 0

    # Scan the target folder (non-recursive)
    for item in target_path.iterdir():
        # Only process files, skip subfolders and hidden files
        if item.is_file() and not item.name.startswith('.'):
            ext = item.suffix.lower()
            matched_category = "Others"

            # Map extension to category case-insensitively
            for category, extensions in config.items():
                if ext in extensions:
                    matched_category = category
                    break

            dest_folder = target_path / matched_category

            if dry_run:
                print(f"[PREVIEW] Would move: {item.name} -> {matched_category}/")
            else:
                dest_folder.mkdir(exist_ok=True)
                shutil.move(str(item), str(dest_folder / item.name))
                print(f"[MOVED] {item.name} -> {matched_category}/")

            summary[matched_category] += 1

    # Print summary report
    print("\n--- Summary Report ---")
    for cat, count in summary.items():
        if count > 0:
            print(f"  {cat}: {count} file(s)")


# ==========================================
# 2. TEST AUTOMATION
# ==========================================
if __name__ == "__main__":
    example_folder = "my_messy_downloads"
    test_path = Path(example_folder)

    # Clean and recreate test folder
    if test_path.exists():
        shutil.rmtree(test_path)
    test_path.mkdir()

    # Generate test files
    test_files = [
        "photo.jpg", "vacation_shot.png",
        "resume.pdf", "notes.txt", "budget.xlsx",
        "song.mp3", "project_archive.zip", "script.py",
        "random_unsupported_file.xyz"
    ]

    for filename in test_files:
        (test_path / filename).touch()

    print(f"📁 Created example folder: '{example_folder}/'")

    # Run the sorter
    organize_folder(example_folder, dry_run=False)
