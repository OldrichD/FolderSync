import argparse
import os
import time
import shutil
import hashlib
import threading
import keyboard


def compare_files(file1, file2):
    """Compare content hashes of two files."""
    with open(file1, "rb") as f1, open(file2, "rb") as f2:
        hash1 = hashlib.sha256(f1.read()).hexdigest()
        hash2 = hashlib.sha256(f2.read()).hexdigest()

    return hash1 == hash2


def get_directory_content(directory):
    """Get the content (files and subdirectories) of a directory."""
    content = ""
    for root, dirs, files in os.walk(directory):
        for file in files:
            content += f"File: {os.path.relpath(os.path.join(root, file), directory)}\n"
        for sub_dir in dirs:
            content += f"Directory: {os.path.relpath(os.path.join(root, sub_dir), directory)}\n"
    return content


class SyncThread(threading.Thread):
    """Thread class for folder synchronization."""

    def __init__(self, source_folder, replica_folder, log_file, interval):
        """Initialize the synchronization thread."""
        super().__init__()
        self.source_folder = source_folder
        self.replica_folder = replica_folder
        self.log_file = log_file
        self.interval = interval
        self.stop_event = threading.Event()

    def run(self):
        """Run the synchronization thread."""
        # Log synchronization parameters at the start
        self.log(f"Synchronization parameters: "
                 f"--source_folder {self.source_folder} "
                 f"--replica_folder {self.replica_folder} "
                 f"--log_file {self.log_file} "
                 f"--time_interval {self.interval}")

        while not self.stop_event.is_set():
            self.sync_folders()
            remaining_time = self.interval

            # Sleep and decrement the remaining time until the next synchronization
            while not self.stop_event.is_set() and remaining_time > 0:
                time.sleep(1)
                remaining_time -= 1

    def stop(self):
        """Stop the synchronization thread."""
        # Set the stop event to terminate the synchronization thread
        self.stop_event.set()

    def sync_folders(self):
        """Synchronize files and directories."""
        # Log synchronization start
        self.log("Synchronization started.")

        # Perform file and directory synchronization
        self.sync_files()
        self.sync_directories()

        # Log synchronization complete
        self.log("Synchronization complete.")

    def sync_files(self):
        """Synchronize files in the source and replica folders."""
        for root, dirs, files in os.walk(self.source_folder):
            for file in files:
                source_path = os.path.join(root, file)
                replica_path = os.path.join(self.replica_folder, os.path.relpath(source_path, self.source_folder))

                replica_dir = os.path.dirname(replica_path)

                # Create replica directory if it doesn't exist
                if not os.path.exists(replica_dir):
                    os.makedirs(replica_dir)
                    self.log(f"Created directory: {replica_dir}")

                # Check if replica file exists and compare content hashes
                if os.path.exists(replica_path):
                    source_size = os.path.getsize(source_path)
                    source_mtime = os.path.getmtime(source_path)
                    replica_size = os.path.getsize(replica_path)
                    replica_mtime = os.path.getmtime(replica_path)

                    if (source_size, source_mtime) != (replica_size, replica_mtime):
                        shutil.copy2(source_path, replica_path)
                        self.log(f"Modified: {os.path.relpath(source_path, self.source_folder)}")
                    elif not compare_files(source_path, replica_path):
                        shutil.copy2(source_path, replica_path)
                        self.log(f"Modified: {os.path.relpath(source_path, self.source_folder)}")
                else:
                    shutil.copy2(source_path, replica_path)
                    self.log(f"Created: {os.path.relpath(source_path, self.source_folder)}")

    def sync_directories(self):
        """Synchronize directories in the source and replica folders."""
        # Create a set to store replica directories
        replica_directories = set()

        # Synchronize directories in the source folder
        for root, dirs, files in os.walk(self.source_folder):
            for dir_name in dirs:
                source_dir = os.path.join(root, dir_name)
                replica_dir = os.path.join(self.replica_folder, os.path.relpath(source_dir, self.source_folder))

                replica_directories.add(replica_dir)

                # Create empty directory in replica if it doesn't exist
                if not os.path.exists(replica_dir):
                    os.makedirs(replica_dir)
                    self.log(f"Created directory: {os.path.relpath(replica_dir, self.replica_folder)}")

        # Check for deleted directories in replica
        for root, dirs, files in os.walk(self.replica_folder):
            for dir_name in dirs:
                replica_dir = os.path.join(root, dir_name)
                source_dir = os.path.join(self.source_folder, os.path.relpath(replica_dir, self.replica_folder))

                # Delete replica directory if it doesn't exist in the source
                if not os.path.exists(source_dir):
                    # Log the content of the deleted directory
                    deleted_content = get_directory_content(replica_dir)

                    # Use shutil.rmtree to delete even non-empty directories
                    shutil.rmtree(replica_dir)
                    self.log(f"Deleted directory: {os.path.relpath(replica_dir, self.replica_folder)}\n"
                             f"Deleted content: {deleted_content}")

    def log(self, message):
        """Log the message with a timestamp to the specified log file and print it."""
        with open(self.log_file, 'a') as log:
            log.write(f"{time.ctime()} - {message}\n")
        print(message)


if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Folder synchronization program')
    parser.add_argument('--source_folder', type=str, default="Source", help='Source folder path.')
    parser.add_argument('--replica_folder', type=str, default="Replica", help='Replica folder path.')
    parser.add_argument('--log_file', type=str, default='log.txt', help='Log file path.')
    parser.add_argument('--time_interval', type=int, default=10,
                        help='Synchronization execution time interval in seconds.')
    args = parser.parse_args()

    # Create and start synchronization thread
    sync_thread = SyncThread(args.source_folder, args.replica_folder, args.log_file, args.time_interval)
    sync_thread.start()

    # Waiting for the pressed 'esc' key to finish the synchronization.
    try:
        keyboard.wait('esc')
    except KeyboardInterrupt:
        pass
    finally:
        sync_thread.stop()
        sync_thread.join()
