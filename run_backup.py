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
    sources = FileManager.get_backup_positions()

    # Get every source via SCP
    FileManager.get(source_path=sources, target_path=TARGET_DIR, recursive=True)