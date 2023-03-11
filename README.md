# folder_sync
Implements a one way folder synchronization task.

Developed with Python 3.10.

## Usage
* Install **`requirements.txt`**

Example use:
Run synchronization of 'source_folder_name' and 'replica_folder_name' every 4 hours and log process to 'log_file_name'.
```bash
python3 sync.py -s 'source_folder_name' -r 'replica_folder_name' -log 'log_file_name' -h 4
```  
For help run:
```bash
python3 sync.py --help
```  
