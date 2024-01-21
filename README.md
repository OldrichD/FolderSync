# Folder Sync Project

#### This is a program that performs one-way synchronization of two folders.
This program facilitates one-way synchronization of two folders, aiming to keep a replica folder updated with the content of a source folder. The synchronization includes various operations such as file updates, copying, and deletions (where renaming is treated as separate delete and copy operations). The progress of synchronization, including input parameters, start, performed changes, and completion, is logged to both the console and a specified log file.

## Requirements

* Python 3.x
* Libraries: argparse, hashlib, os, time, shutil, threading, keyboard
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

To synchronize a folder named "source_folder" to "replica_folder" with a time interval of 120 seconds and log the synchronization process to "sync_log.txt", run the following command:

```
python main.py --source source_folder --replica replica_folder --log-file sync_log.txt --time-interval 120
```

## Notes

- Initial file comparison uses metadata (size and date), followed by SHA256 hashing to optimize computational requirements.
- The script creates the replica folder if it doesn't exist.
- An error is raised if the source folder doesn't exist.
- Continuous monitoring and synchronization are based on the specified time interval.
- File copying utilizes the copy2 method from the shutil library, preserving metadata and permissions.
- For seamless integration into complex programs, synchronization is executed in a dedicated thread.
