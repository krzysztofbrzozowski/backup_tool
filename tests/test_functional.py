"""
@author:    Krzysztof Brzozowski
@file:      test_functional
@time:      04/03/2023
@desc:      
"""
import logging
import os
import time

import pytest

from file_manager import FileManager
# from private_file import *
from config_manager import ConfigManager as Config


def get_file_via_scp(source: str = None, target: str = None, recursive: bool = False):
    """Call downloading file via SCP using subprocess

    :return:
        expected target size (extracted form debug log)
        expected download speed (extracted form debug log)
    """
    import subprocess
    import re

    FileManager.connect()

    # Manual call of scp and getting file size and speed
    # Call 'scp -v -i <pkey> <user>@<host>:<source_file> <target_file>'
    call_args = f"scp -v {'-r' if recursive else ''} -i {Config.get_config_value('PKEY')} " \
                f"{Config.get_config_value('USER')}@{Config.get_config_value('HOST')}:{source} {target}"

    proc = subprocess.Popen(call_args, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in proc.stdout:
        if line != bytes():
            try:
                line = line.decode().strip()
                if re.search(r'Transferred:.*', line):
                    # Line looks similar: Transferred: sent 17504, received 10506872 bytes, in 13.8 seconds
                    # Looking for data
                    sent, transferred, time_transfer = re.findall(r'[\d+^.]+|\d+[.]\d+', line)
            except Exception as e:
                logging.error(f'test output | {e}')
    proc.wait()

    # Get estimated target size from debug log
    expected_target_size = (int(transferred) - int(sent)) / (1024 * 1024)
    expected_download_speed = expected_target_size / float(time_transfer)
    logging.info(f'test output | {expected_download_speed:.2f} MB/s')

    return expected_target_size, expected_download_speed


class TestFunctionalBackupTool:
    @pytest.fixture(autouse=True)
    def setup_method(self):
        # TODO set up logging to info only
        # TODO clean up whole folder before test!
        Config.test_mode = True

    # @pytest.fixture(autouse=True)
    # def teardown_method(self):
    #     FileManager.close()

    # TODO if this test is second one Fails, why?
    def test_connection_raises_exception_if_key_not_correct(self):
        with pytest.raises(BaseException):
            FileManager.connect(use_pkey=False)

    def test_login_via_ssh_possible(self):
        assert FileManager.connect(use_pkey=True) is None

    def test_downloaded_file_is_correct(self):
        from pathlib import Path
        source = Config.get_config_value('TEST_FILE_SOURCE')
        # Verify size of whole folder
        # Not needed return values since comparison works on folder/file level base
        get_file_via_scp(source=source, target=Config.get_config_value('TEST_FILE_TARGET_SCP'), recursive=False)

        directory = Path(Config.get_config_value('TEST_FILE_TARGET_SCP'))
        expected_target_size = sum(f.stat().st_size for f in directory.glob('**/*') if f.is_file())
        # Tested method
        target_size, _ = FileManager.get(source_path=source, target_path=Config.get_config_value('TEST_FILE_TARGET_API'), recursive=False)

        assert expected_target_size == target_size

    def test_downloaded_directory_is_correct(self):
        from pathlib import Path
        source = Config.get_config_value('TEST_DIR_SOURCE')
        # Verify size of whole folder
        # Not needed return values since comparison works on folder/file level base
        get_file_via_scp(source=source, target=Config.get_config_value('TEST_DIR_TARGET_SCP'), recursive=True)

        directory = Path(Config.get_config_value('TEST_DIR_TARGET_SCP'))
        expected_target_size = sum(f.stat().st_size for f in directory.glob('**/*') if f.is_file())
        # Tested method
        target_size, _ = FileManager.get(source_path=source, target_path=Config.get_config_value('TEST_DIR_TARGET_API'), recursive=True)

        assert expected_target_size == target_size

    def test_download_speed_is_correct(self):
        """Test is comparing download result using SCPClient and raw SCP call from console"""
        # Manual call of scp and getting file size and speed
        source = Config.get_config_value('TEST_FILE_SOURCE')

        _, expected_download_speed = get_file_via_scp(source=source, target=Config.get_config_value('TEST_FILE_TARGET_SCP'))

        # Tested method
        _, download_speed = FileManager.get(source_path=source, target_path=Config.get_config_value('TEST_FILE_TARGET_API'))
        assert expected_download_speed == download_speed





