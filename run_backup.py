"""
@author:    Krzysztof Brzozowski
@file:      run_backup
@time:      05/03/2023
@desc:      
"""
import time

from file_manager import *
import logger

logging.getLogger('main')

if __name__ == '__main__':
    # Connect via SSH
    FileManager.connect()

    # Create postgres backup
    CommandManager.execute_command(command=[
        'export PGPASSWORD="XXXXXXXX"; pg_dump -h localhost -U my_user my_db > /some_path_to/db_dump.sql'
    ])
    # TODO Dynamic await for command execution not working yet
    time.sleep(10)

    # Get all backup sources
    backup_paths, skip_paths = FileManager.get_backup_positions()

    # Get source files/directories via SCP
    FileManager.get(source_path=backup_paths, skip_path=skip_paths)

