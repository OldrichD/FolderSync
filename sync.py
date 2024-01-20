
import os
import sys
import time
import shutil
import threading
import keyboard


class SyncThread(threading.Thread):
    def __init__(self, source_folder, replica_folder, log_file, interval):
        super().__init__()
        self.source_folder = source_folder
        self.replica_folder = replica_folder
        self.log_file = log_file
        self.interval = interval
        self.stop_event = threading.Event()

    def run(self):
        self.sync_folders()
        while not self.stop_event.is_set() and self.interval > 0:
            time.sleep(1)
            self.interval -= 1

    def stop(self):
        self.stop_event.set()

    def sync_folders(self):
        # Log synchronization start
        self.log("Synchronization started.")

        # Synchronize folders
        for root, dirs, files in os.walk(self.source_folder):
            for file in files:
                source_path = os.path.join(root, file)
                relative_path = os.path.relpath(source_path, self.source_folder)
                replica_path = os.path.join(self.replica_folder, os.path.relpath(source_path, self.source_folder))

                # Check if the destination directory exists, create it if not
                replica_dir = os.path.dirname(replica_path)
                if not os.path.exists(replica_dir):
                    os.makedirs(replica_dir)

                if os.path.exists(replica_path):
                    # File exists in replica, check for modification
                    if os.path.getmtime(source_path) > os.path.getmtime(replica_path):
                        # Source file has been modified, copy to replica
                        shutil.copy2(source_path, replica_path)
                        self.log(f"Modified: {os.path.relpath(source_path, self.source_folder)}")
                else:
                    # File doesn't exist in replica, create it
                    shutil.copy2(source_path, replica_path)
                    self.log(f"Created: {os.path.relpath(source_path, self.source_folder)}")

        # Check for deleted files in replica
        for root, dirs, files in os.walk(self.replica_folder):
            for file in files:
                replica_path = os.path.join(root, file)
                source_path = os.path.join(self.source_folder, os.path.relpath(replica_path, self.replica_folder))

                if not os.path.exists(source_path):
                    # File doesn't exist in source, delete it in replica
                    os.remove(replica_path)
                    self.log(f"Deleted: {os.path.relpath(replica_path, self.replica_folder)}")

        # Log synchronization complete
        self.log("Synchronization complete.")

    def log(self, message):
        with open(self.log_file, 'a') as log:
            log.write(f"{time.ctime()} - {message}\n")
        print(message)


def is_positive_integer(value):
    try:
        value = int(value)
        return value > 0
    except ValueError:
        return False


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python sync.py <source_folder> <replica_folder> <log_file> <interval>")
        sys.exit(1)

    source_folder, replica_folder, log_file, interval = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]

    if not os.path.exists(source_folder) or not os.path.exists(replica_folder):
        print("Source or replica folder does not exist.")
        sys.exit(1)

    if not is_positive_integer(interval):
        print("Interval should be an integer greater than 0.")
        sys.exit(1)

    interval = int(interval)

    sync_thread = SyncThread(source_folder, replica_folder, log_file, interval)
    sync_thread.start()

    try:
        keyboard.wait('esc')
    except KeyboardInterrupt:
        pass
    finally:
        sync_thread.stop()
        sync_thread.join()