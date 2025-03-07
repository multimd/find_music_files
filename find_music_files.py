import os
import sys
import argparse
from pathlib import Path
from collections import defaultdict
import time

# Music file extensions to search for
MUSIC_EXTENSIONS = {
    # Common formats
    ".mp3", ".aac", ".wav", ".flac", ".m4a",
    # High-quality/lossless formats
    ".oga", ".ape", ".dsf", ".dff", ".aiff", ".aif", 
    # Additional formats
    ".ogg"
}

def count_music_files(root_path):
    """
    Count music files in the selected folder and its subfolders.
    Returns:
    - dictionary with counts for each top-level subfolder
    - total count of files
    - dictionary with counts by file extension
    """
    music_files_count = defaultdict(int)
    extension_counts = defaultdict(int)
    
    # Initialize counts for all supported extensions with zeros
    for ext in MUSIC_EXTENSIONS:
        extension_counts[ext] = 0
        
    total_count = 0
    cumulative_count = 0
    
    # Get top-level subdirectories
    try:
        top_subdirs = [d for d in os.scandir(root_path) if d.is_dir()]
        if not top_subdirs:
            # If no subdirectories, count files in the root directory
            count = 0
            for f in os.scandir(root_path):
                if f.is_file():
                    file_ext = Path(f.path).suffix.lower()
                    if file_ext in MUSIC_EXTENSIONS:
                        count += 1
                        extension_counts[file_ext] += 1
            
            music_files_count[os.path.basename(root_path)] = count
            total_count = count
            print(f"Found {count} music files in {os.path.basename(root_path)}")
            return music_files_count, total_count, extension_counts
    except PermissionError:
        print(f"Permission denied: cannot access {root_path}")
        return music_files_count, total_count, extension_counts
    
    print(f"Scanning {len(top_subdirs)} top-level subdirectories in {root_path}...")
    print(f"{'Subfolder':<50} | {'Files':<8} | {'Cumulative':<10} | {'Speed (files/sec)':<15}")
    print("-" * 90)
    
    # Process each top-level subdirectory
    for subdir in top_subdirs:
        subdir_count = 0
        print(f"Scanning {subdir.name}...", end="", flush=True)
        start_time = time.time()
        
        # Recursively walk through the subdirectory
        for root, _, files in os.walk(subdir.path):
            for file in files:
                file_ext = Path(file).suffix.lower()
                if file_ext in MUSIC_EXTENSIONS:
                    subdir_count += 1
                    total_count += 1
                    extension_counts[file_ext] += 1
                    
                    # Show progress for large directories
                    if subdir_count % 100 == 0:
                        elapsed = time.time() - start_time
                        print(f"\rScanning {subdir.name}... Found {subdir_count} music files ({subdir_count/elapsed:.1f} files/sec)", 
                              end="", flush=True)
        
        elapsed = time.time() - start_time
        files_per_sec = subdir_count/elapsed if elapsed else 0
        cumulative_count += subdir_count
        
        # Display progress with cumulative count
        print(f"\r{subdir.name:<50} | {subdir_count:<8,d} | {cumulative_count:<10,d} | {files_per_sec:<15.1f}")
        
        music_files_count[subdir.name] = subdir_count
    
    return music_files_count, total_count, extension_counts

def main():
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(description='Count music files in a folder and its subfolders.')
    parser.add_argument('--path', '-p', required=True, help='Path to the folder to scan.')
    args = parser.parse_args()
    
    # Get the folder path
    folder_path = args.path
    # Check if the path exists and is a directory
    if not os.path.isdir(folder_path):
        print(f"Error: '{folder_path}' is not a valid directory. Exiting.")
        sys.exit(1)
    
    print(f"Selected folder: {folder_path}")
    print(f"Scanning for files with extensions: {', '.join(sorted(MUSIC_EXTENSIONS))}")
    print("-" * 70)
    
    # Count music files
    start_time = time.time()
    folder_counts, total_count, extension_counts = count_music_files(folder_path)
    elapsed = time.time() - start_time
    
    # Display results
    print("\nMusic Files Count by Top Subfolder:")
    print("-" * 70)
    
    # Calculate the longest folder name for alignment
    max_folder_length = max(len(folder) for folder in folder_counts.keys()) if folder_counts else 0
    
    # Print results in a formatted table
    print(f"{'Subfolder':<{max_folder_length+2}} | {'Music Files':>12} | {'% of Total':>10}")
    print("-" * (max_folder_length+2) + "+" + "-" * 14 + "+" + "-" * 12)
    
    for folder, count in sorted(folder_counts.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / total_count) * 100 if total_count > 0 else 0
        print(f"{folder:<{max_folder_length+2}} | {count:>12,d} | {percentage:>9.2f}%")
    
    # Display extension statistics
    print("\nMusic Files Count by Extension:")
    print("-" * 70)
    
    # Calculate the longest extension for alignment
    max_ext_length = max(len(ext) for ext in extension_counts.keys()) if extension_counts else 0
    max_ext_length = max(max_ext_length, 10)  # Ensure minimum width
    
    # Print extension results in a formatted table
    print(f"{'Extension':<{max_ext_length+2}} | {'Music Files':>12} | {'% of Total':>10}")
    print("-" * (max_ext_length+2) + "+" + "-" * 14 + "+" + "-" * 12)
    
    # First display extensions with counts
    non_zero_exts = {ext: count for ext, count in extension_counts.items() if count > 0}
    zero_exts = {ext: count for ext, count in extension_counts.items() if count == 0}
    
    # Display extensions with files first
    for ext, count in sorted(non_zero_exts.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / total_count) * 100 if total_count > 0 else 0
        print(f"{ext:<{max_ext_length+2}} | {count:>12,d} | {percentage:>9.2f}%")
    
    # Then display extensions with zero files
    for ext in sorted(zero_exts.keys()):
        print(f"{ext:<{max_ext_length+2}} | {0:>12,d} | {0:>9.2f}%")
    
    print("-" * 70)
    print(f"Total music files: {total_count:,d}")
    print(f"Scan completed in {elapsed:.2f} seconds")

if __name__ == "__main__":
    main() 