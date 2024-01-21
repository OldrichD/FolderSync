# Folder Sync Project

#### This is a program that performs one-way synchronization of two folders.
This script carries out a one-way synchronization of two folders to keep the replica folder updated with the contents of the source folder. The synchronization includes the following operations: file update, copy, and delete (with renaming being treated as separate delete and copy operations). Subfolders are also included in the synchronization, including empty ones. The synchronization progress (start, changes made, finish) and input parameters are recorded in a file and output to the console.

## Requirements

* Python 3.x
* Libraries: argparse, hashlib, os, sys, re, time, shutil, threading, keyboard
```
pip install -r requirements.txt
```

## How to Use

1. Ensure you have Python 3.x installed on your system.
2. Download or clone this repository to your local machine.
```
git clone https://github.com/OldrichD/FolderSync.git
```

## Usage

```
python main.py --source <SOURCE_FOLDER> --replica <REPLICA_FOLDER> --log_file <LOG_FILE> --time_interval <TIME_INTERVAL>
```
- To stop the synchronization press 'ESC' keyboard.

### Option

- `--source`: Path to the source folder to be synchronized (default: "Source").
- `--replica`: Path to the replica folder that will be updated to match the source folder (default: "Replica").
- `--log_file`: Path to the log file (default: "log.txt").
- `--time_interval`: Time interval for synchronization in seconds (default: 10).

### Additional Options:

- `-h, --help`: Show help message.



## Example

To synchronize a folder named "Source" to "Replica" with a time interval of 10 seconds and log the synchronization process to "log.txt", run the following command:

```
python main.py --source_folder Source --replica_folder Replica --log_file log.txt --time_interval 10
```

## Notes

- Initial file comparison uses metadata (size and date), followed by SHA256 hashing to optimize computational requirements.
- The script creates the replica folder if it doesn't exist.
- An error is raised if the source folder doesn't exist.
- Continuous monitoring and synchronization are based on the specified time interval.
- File copying utilizes the copy2 method from the shutil library, preserving metadata and permissions.
- For seamless integration into complex programs, synchronization is executed in a dedicated thread.
