##!/usr/bin/env python

import logging
import shutil
import os
import time

from datetime import datetime


username = "zosma"
target_directory = "D:\\Valheim\\ValheimBackups"
logs_directory = "{base_dir}\\logs".format(base_dir=target_directory)
retention = 2

source_directory = "C:\\Users\\{username}\\AppData\\LocalLow\\IronGate\\Valheim".format(username=username)
log_file = \
    '{log_directory}\\backup_log_{date}.log'\
    .format(log_directory=logs_directory, date=datetime.now().strftime('%Y%m%d'))


def create_dirs_open_log(target_location, logs_location):
    if not os.path.exists(target_location):
        os.makedirs(target_location)
    if not os.path.exists(logs_location):
        os.makedirs(logs_location)


def configure_logging():
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format=' %(asctime)s - %(levelname)s - %(message)s'
    )


def backup_source_directory(source_location, target_location):
    target_filename = \
        target_location + "\\valheimBackup.{date}"\
        .format(date=datetime.now().strftime('%Y%m%d_%H%M%S'))
    logging.info("Creating backup " + shutil.make_archive(target_filename, 'zip', source_location))


def delete_old_backups(target_location, retention_days):
    current_date = time.time()
    for file in os.listdir(target_location):
        file_full_path = os.path.join(target_location, file)
        if os.path.isfile(file_full_path):
            if 'valheimBackup.' in file:
                if os.stat(file_full_path).st_mtime < current_date - retention_days * 86400:
                    logging.info("Deleting old backup {filename}".format(filename=file))
                    os.unlink(file_full_path)


create_dirs_open_log(target_location=target_directory, logs_location=logs_directory)
configure_logging()
backup_source_directory(source_location=source_directory, target_location=target_directory)
delete_old_backups(target_location=target_directory, retention_days=retention)

