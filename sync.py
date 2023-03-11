"""Synchronizes two folders: source and replica.
Program maintains a full, identical copy of source folder at replica folder.

Author: Sara Derakhshani
Date: 11.03.2023
"""


import click
import filecmp
import logging
import os 
import shutil
import sys
import time


@click.command()
@click.option('-s',
              '--source_dir',
              help='Path to source folder.',
              required=True
              )
@click.option('-r',
              '--replica_dir',
              help='Path to replica folder.',
              required=True
              )
@click.option('-log',
              '--log_file',
              help='Path to log file.',
              required=True
              )
@click.option('-h',
              '--hours',
              default=1,
              show_default=True,
              type=click.FLOAT,
              help="Synchronization interval in hours.",
              )
def main(source_dir, replica_dir, log_file, hours=None):
    # Set file and console logging
    logformat = '%(asctime)s [%(levelname)s] %(message)s'
    logging.basicConfig(filename=log_file, 
                        level=logging.INFO,
                        format=logformat) 
    console = logging.StreamHandler(sys.stdout)                                               
    console.setLevel(logging.INFO)                                                  
    console.setFormatter(logging.Formatter(fmt=logformat))                                                
    logging.getLogger().addHandler(console)
    # Run synchronization until it's stopped manually
    while True:
        # Stop program execution if source directory doesn't exist
        if not os.path.exists(source_dir):
            logging.error("Source folder not found. Synchronization not executed.")
            exit()
        # Check if replica directory has to be created
        if not os.path.exists(replica_dir):
            logging.warning("Replica folder not found.")
            os.mkdir(replica_dir) 
            logging.info("Replica folder created.")
        logging.info("Start synchronization.")
        for filename in os.listdir(source_dir):
            # Compare files with the same name in source and replica folder
            # If they don't match delete old copy in replica folder and create new one
            source_file_path = os.path.join(source_dir, filename)
            replica_file_path = os.path.join(replica_dir, filename)
            if os.path.isfile(replica_file_path):
                # Current comparison is by os.stat() signatures
                # Set shallow to False to compare file by content
                if not filecmp.cmp(source_file_path, replica_file_path, shallow=True):
                    os.remove(replica_file_path)
                    logging.info(f"Removed {replica_file_path}. \
                                 Content does not match source file {source_file_path}")
                    shutil.copy2(source_file_path, replica_dir)
                    logging.info(f"Copied {source_file_path} to {replica_file_path}.")
            # Create copy of source file, if no matching replica file name exists
            else:
                shutil.copy2(source_file_path, replica_dir)
                logging.info(f"Copied {source_file_path} to {replica_file_path}.")
        # Delete replica files that don't have matching source files
        for filename in os.listdir(replica_dir):
            replica_file_path = os.path.join(replica_dir, filename)
            source_file_path = os.path.join(source_dir, filename)
            if not os.path.isfile(source_file_path):
                os.remove(replica_file_path)
                logging.info(f"Removed {replica_file_path}. \
                             No matching source file found in {source_dir}.")
        logging.info("Finished synchronization.")
        # Pause script until next synchronization cycle starts
        hours_in_secs = hours * 3600
        time.sleep(hours_in_secs)


if '__main__' == __name__:
    main()
