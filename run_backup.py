"""
@author:    Krzysztof Brzozowski
@file:      run_backup
@time:      05/03/2023
@desc:      
"""
from file_manager import *
import logger

logging.getLogger('main')

if __name__ == '__main__':
    # Connect via SSH
    FileManager.connect()

    # Get all backup sources
    backup_paths, skip_paths = FileManager.get_backup_positions()

    # Get source files/directories via SCP
    FileManager.get(source_path=backup_paths, skip_path=skip_paths)

