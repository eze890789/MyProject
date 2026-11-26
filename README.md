Automatic File Organizer

A simple, efficient tool that scans a messy folder and automatically sorts files into subfolders based on their extensions.

📋 Overview

Ever downloaded too many files into your Downloads folder or Desktop? File Sorter helps you declutter by automatically organizing files into categorized subfolders based on their file extensions (e.g., images, documents, videos, audio, archives, and more).

✨ Features

· 🗂️ Automatic sorting – Groups files into folders by extension category
· 📁 Smart categorization – Maps extensions to meaningful folder names (e.g., .jpg → Images, .pdf → Documents)
· 🔍 Dry-run mode – Preview changes before moving anything
· 🧩 Custom rules – Add or modify extension-to-folder mappings via a config file
· 🛡️ Safe by default – Skips unknown extensions or routes them to an Others folder
· 📊 Summary report – Shows how many files were moved and where

🚀 Getting Started

Prerequisites

· Python 3.8+ (or your language/runtime of choice)
· No external dependencies required (uses standard library only)

Installation

```bash
git clone https://github.com/eze890789/file-sorter.git
cd file-sorter
```

Usage

Basic usage — sort a folder:

```bash
python file_sorter.py /path/to/messy/folder
```

Preview changes without moving files (dry run):

```bash
python file_sorter.py /path/to/messy/folder --dry-run
```

Use a custom rules file:

```bash
python file_sorter.py /path/to/messy/folder --config custom_rules.json
```

⚙️ Configuration

The default extension mappings live in config.json:

```json
{
  "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"],
  "Documents": [".pdf", ".doc", ".docx", ".txt", ".xls", ".xlsx", ".ppt", ".pptx"],
  "Videos": [".mp4", ".mkv", ".mov", ".avi", ".wmv"],
  "Audio": [".mp3", ".wav", ".flac", ".aac", ".ogg"],
  "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
  "Code": [".py", ".js", ".ts", ".html", ".css", ".java", ".cpp", ".go", ".rs"],
  "Others": []
}
```

· Files with extensions not listed in any category go to Others.
· Extensions are matched case-insensitively.

🧠 How It Works

1. Scans the target folder (non-recursive by default).
2. For each file, looks up its extension in the rules config.
3. Creates the destination subfolder if it doesn't exist.
4. Moves the file into the correct subfolder.
5. Optionally prints a summary of actions taken.

📂 Example

Before:

```
Downloads/
├── photo.jpg
├── resume.pdf
├── song.mp3
├── archive.zip
└── notes.txt
```

After:

```
Downloads/
├── Images/
│   └── photo.jpg
├── Documents/
│   ├── resume.pdf
│   └── notes.txt
├── Audio/
│   └── song.mp3
└── Archives/
    └── archive.zip
```

🛠️ Roadmap

☐ Recursive scanning of nested folders
☐ Undo / restore last operation
☐ GUI version
☐ Duplicate file detection
☐ Rule-based sorting by date or size

🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request.

1. Fork the repo
2. Create a feature branch (git checkout -b feature/my-feature)
3. Commit your changes (git commit -m "Add my feature")
4. Push and open a PR

📄 License

This project is licensed under the MIT License — see the LICENSE file for details.

🙏 Acknowledgements

Inspired by the universal problem of messy download folders.

---

Made with ❤️ to keep your folders tidy.

