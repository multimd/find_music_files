# Music Files Counter

A Python script to count music files in a selected folder and its subfolders.

## Features

- Counts music files with extensions: .mp3, .aac, .wav, .flac, .m4a, .oga, .ape, .dsf, .dff, .aiff, .aif, .ogg
- Shows counts for each top-level subfolder
- Displays a total sum of all music files
- Shows real-time progress as it scans
- Works with or without a graphical interface

## Requirements

- Python 3.11 or newer
- No additional packages required (uses only Python standard library)

## Usage

### Option 1: Using the Graphical Interface (requires tkinter)

```bash
python find_music_files.py
```

A folder selection dialog will appear for you to choose the directory to scan.

### Option 2: Using Command Line Arguments

```bash
python find_music_files.py --path /path/to/music/folder
```

or the short form:

```bash
python find_music_files.py -p /path/to/music/folder
```

## Expected Output

The script will display:
- Progress information as it scans each subfolder
- A summary of music files found in each subfolder
- The total count of music files found
- The time taken for the scan

## Troubleshooting

If you encounter an error about missing tkinter or tcl-tk:

1. Either use the command-line option with `--path` flag, or
2. Install the required libraries:
   - On macOS with Homebrew: `brew install tcl-tk`
   - On Ubuntu/Debian: `sudo apt-get install python3-tk`
   - On Windows: tkinter is included with standard Python installations 