import os
import json
import shutil
from pathlib import Path
from tkinter import *
# Import the tools needed for picking folders and showing alerts
from tkinter import filedialog, messagebox


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
        "Code": [".py", ".js", ".ts", ".html", ".css", ".java", ".cpp", ".go", ".rs"],
        "Others": []
    }

    config_path = Path(config_filename)
    if config_path.exists():
        try:
            with open(config_path, "r") as f:
                print(f"Loaded custom rules from '{config_filename}'")
                return json.load(f)
        except json.JSONDecodeError:
            print(f"Warning: '{config_filename}' is malformed JSON. Using default rules.")
    else:
        print(f"'{config_filename}' not found. Using default internal rules.")

    return default_config


def organize_folder(target_dir, dry_run=False):
    config = load_config("config.json")
    target_path = Path(target_dir)

    if not target_path.exists():
        messagebox.showerror("Error", f"Target directory does not exist.")
        return

    print(f"\n--- Starting File Sorter {'(DRY RUN)' if dry_run else ''} on: {target_path.resolve()} ---")

    summary = {category: 0 for category in config.keys()}
    summary["Others"] = 0

    for item in target_path.iterdir():
        if item.is_file() and not item.name.startswith('.'):
            ext = item.suffix.lower()
            matched_category = "Others"

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

    # Format the summary for a popup box
    report_message = "Folder Organized Successfully!\n\nSummary:\n"
    for cat, count in summary.items():
        if count > 0:
            report_message += f"• {cat}: {count} file(s)\n"

    # Show user success message alert
    messagebox.showinfo("Success", report_message)


# ==========================================
# 2. GUI ACTION FUNCTIONS
# ==========================================
def select_folder():
    """Opens a native directory chooser dialog and stores the selection."""
    chosen_path = filedialog.askdirectory(title="Select Folder to Organize")
    if chosen_path:  # Ensure user didn't hit cancel
        selected_folder_var.set(chosen_path)
        # Update our screen label to show the path chosen
        path_label.config(text=f"Selected:\n{Path(chosen_path).name}", fg="green")


def run_organizer():
    """Validates choice and fires off core logic script."""
    folder_to_sort = selected_folder_var.get()
    if not folder_to_sort:
        messagebox.showwarning("Warning", "Please select a folder first!")
        return

    organize_folder(folder_to_sort)


# ==========================================
# 3. WINDOW & UI DESIGN Layout
# ==========================================
windows = Tk()
windows.title("Automatic File Organizer")
windows.geometry("320x250")  # Reduced window height to fit content beautifully
windows.resizable(False, False)

# This Tkinter variable type remembers text strings across functions
selected_folder_var = StringVar()

# Header Information Title
title_label = Label(windows, text="Automatic File Sorter", font=("Arial", 16, "bold"))
title_label.pack(pady=15)

# Displays what folder is targeted currently
path_label = Label(windows, text="No folder selected yet", font=("Arial", 10, "italic"), fg="gray", wraplength=280)
path_label.pack(pady=10)

# Button 1: Browse/Choose folder
choose_btn = Button(windows, text="1. Choose Folder", font=("Arial", 11), width=18, command=select_folder)
choose_btn.pack(pady=5)

# Button 2: Run the program sorting logic
run_btn = Button(windows, text="2. Run Organizer", font=("Arial", 11, "bold"), bg="#4CAF50", fg="white", width=18,
                 command=run_organizer)
run_btn.pack(pady=10)

# ==========================================
# 4. INITIALIZATION
# ==========================================
if __name__ == "__main__":
    # Optional: Keep your automated example folder generation if you want to test it locally.
    example_folder = "my_messy_downloads"
    test_path = Path(example_folder)
    if test_path.exists():
        shutil.rmtree(test_path)
    test_path.mkdir()

    test_files = ["photo.jpg", "vacation_shot.png", "resume.pdf", "notes.txt", "budget.xlsx", "song.mp3",
                  "project_archive.zip", "script.py"]
    for filename in test_files:
        (test_path / filename).touch()

    print(f"Created standalone example folder: '{example_folder}/' for testing.")

    # Kickoff the Tkinter event loop window rendering
    windows.mainloop()
