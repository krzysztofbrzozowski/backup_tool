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
from pathlib import Path
from shutil import rmtree

# Private imports
from file_manager import FileManager
from command_manager import CommandManager
from config_manager import ConfigManager as Config

BASE_DIR = Path(__file__).parent.parent


def get_file_via_scp(source: str = None, target: str = None, recursive: bool = False):
    """Call downloading file via SCP using subprocess

    :return:
        expected target size (extracted form debug log)
        expected download speed (extracted form debug log)
    """
    import subprocess
    import re

    CommandManager.connect(use_pkey=True)

    # Create parent folder if not exist yet
    try:
        if not os.path.exists(Path(target).parent):
            os.makedirs(Path(target).parent, exist_ok=True)
    except OSError as e:
        logging.error(e)

    # Manual call of scp and getting file size and speed
    # Call 'scp -v -i <pkey> <user>@<host>:<source_file> <target_file>'
    call_args = f"scp -o StrictHostKeyChecking=no -v {'-r' if recursive else ''} -P 2222 -i {Config.get_config_value('PKEY')} " \
                f"{Config.get_config_value('USER')}@{Config.get_config_value('HOST')}:{source} {target} "

    logging.info(f'running command -> {call_args}')

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
    # return expected_target_size


class TestFunctionalBackupTool:
    @pytest.fixture(autouse=True)
    def setup_method(self):
        logging.disable(logging.CRITICAL)
        Config.test_mode = True

        # Clear all downloaded data
        for c_path in Config.get_config_values(
                ['DOWNLOAD_TEST_LOCATION_SCP', 'DOWNLOAD_TEST_LOCATION_API']):
            c_path = os.path.join(BASE_DIR, Config.get_config_value('BACKUP_DIR'), c_path)
            for path in Path(c_path).glob("**/*"):
                if path.is_file(): path.unlink()
                elif path.is_dir(): rmtree(path)

    # TODO if this test is second one Fails, why?
    # def test_connection_raises_exception_if_key_not_correct(self):
    #     """Verifying raising exception if unable to SSH connect"""
    #     with pytest.raises(BaseException):
    #         CommandManager.connect(use_pkey=False)

    def test_login_via_ssh_possible(self):
        """Verifying possibility of SSH connection"""
        assert CommandManager.connect(use_pkey=True) is None

    def test_remote_commands_execution_working(self):
        """Comparing size of remotely created file with random size after download to local disc"""
        import random
        # Create random size of file which is also expected one after download
        # Multiply 1024 * 1024 to get size in bytes
        expected_random_size = random.randint(5, 10) * 1024 * 1024

        # Create source path
        source_path = os.path.join(
            Config.get_config_value('TEST_DIR_SOURCE'),
            'test_remote_executing_command',
            f'{expected_random_size}B_largefile'
        )

        # Create download path using SCP
        target_path_scp = os.path.join(
            BASE_DIR,
            Config.get_config_value('BACKUP_DIR'),
            Config.get_config_value('DOWNLOAD_TEST_LOCATION_SCP'),
            source_path
        )

        CommandManager.connect(use_pkey=True)
        # Tested method
        CommandManager.execute_command(command=[
            fr'mkdir -p /{Path(source_path).parent}',
            fr'rm /{source_path} ; truncate -s {expected_random_size} /{source_path}'
        ])

        # Download file via SCP
        get_file_via_scp(source=fr'/{source_path}', target=target_path_scp, recursive=False)

        random_size = os.stat(target_path_scp).st_size

        assert random_size == expected_random_size

        # If working to the cleanup
        CommandManager.execute_command(command=[
            fr'rm -r /{Path(source_path).parent}'
        ])

    # def test_remote_commands_execution_awaiting_for_done(self):
    #     """Verify script awaits remote executing command done"""
    #     # TODO write the test for awaiting execution done
    #     assert True is False

    def test_downloaded_file_size_is_correct(self):
        """Verifying downloaded file have correct size"""
        # Create source path
        source_path = os.path.join(
            Config.get_config_value('TEST_DIR_SOURCE'),
            Config.get_config_value('TEST_FILE_0')
        )
        # Create download path using SCP
        target_path_scp = os.path.join(
            BASE_DIR,
            Config.get_config_value('BACKUP_DIR'),
            Config.get_config_value('DOWNLOAD_TEST_LOCATION_SCP'),
            source_path
        )
        # Create download path using API
        target_path_api = os.path.join(
            BASE_DIR,
            Config.get_config_value('BACKUP_DIR'),
            Config.get_config_value('DOWNLOAD_TEST_LOCATION_API'),
            source_path
        )

        # Not needed return values since comparison works on folder/file level base
        get_file_via_scp(source=fr'/{source_path}', target=target_path_scp, recursive=True)

        # test_target_file = Path(target_path_scp)
        expected_target_size = os.stat(Path(target_path_scp)).st_size

        # Tested method
        target_size, _ = FileManager.get(source_path=fr'/{source_path}', target_path=target_path_api)

        assert target_size == expected_target_size

    def test_downloaded_directory_size_is_correct(self):
        """Verifying downloaded files (recursive) have correct size"""
        # Create source path
        source_path = Config.get_config_value('TEST_DIR_SOURCE')

        # Create download path using SCP
        target_path_scp = os.path.join(
            BASE_DIR,
            Config.get_config_value('BACKUP_DIR'),
            Config.get_config_value('DOWNLOAD_TEST_LOCATION_SCP'),
            source_path
        )
        # Create download path using API
        target_path_api = os.path.join(
            BASE_DIR,
            Config.get_config_value('BACKUP_DIR'),
            Config.get_config_value('DOWNLOAD_TEST_LOCATION_API'),
            source_path
        )

        # Verify size of whole folder
        # Not needed return values since comparison works on folder/file level base
        get_file_via_scp(source=fr'/{source_path}', target=target_path_scp, recursive=True)

        directory = Path(target_path_scp)
        expected_target_size = sum(f.stat().st_size for f in directory.glob('**/*') if f.is_file())

        # Tested method
        target_size, _ = FileManager.get(source_path=fr'/{source_path}', target_path=target_path_api)

        assert target_size == expected_target_size

    # def test_download_speed_is_correct(self):
    #     """Comparing downloading speed using SCPClient and raw SCP call from console"""
    #     source = Config.get_config_value('TEST_FILE_0')
    #     # Manual call of scp and getting file size and speed
    #     _, expected_download_speed = get_file_via_scp(source=source, target=Config.get_config_value('TEST_FILE_TARGET_SCP'))
    #
    #     # Tested method
    #     _, download_speed = FileManager.get(source_path=source, target_path=Config.get_config_value('TEST_FILE_TARGET_API'))
    #
    #     assert download_speed == expected_download_speed

    def test_skip_path_is_working_for_file_and_directory(self):
        """Verify if in downloaded folder skip path is omitted during downloading"""
        # Create source path
        source_path = Config.get_config_value('TEST_DIR_SOURCE')

        # Create download path using API
        target_path_api = os.path.join(
            BASE_DIR,
            Config.get_config_value('BACKUP_DIR'),
            Config.get_config_value('DOWNLOAD_TEST_LOCATION_API'),
            source_path
        )

        skip_paths = list()
        skip_paths.extend([os.path.join(
            '/',
            source_path,
            Config.get_config_value('TEST_FILE_TO_SKIP'))]
        )

        # Extend skip path list with multiple paths provided in YAML file
        skip_paths.extend([os.path.join('/', source_path, yaml_skip_path)
                          for yaml_skip_path
                          in Config.get_config_value('TEST_DIR_TO_SKIP')])


        # Tested method with skipping paths
        target_size, _ = FileManager.get(source_path=fr'/{source_path}',
                                         target_path=target_path_api,
                                         skip_path=skip_paths)

        # In test folder there are only 3 files, each 10MB, size in bytes
        expected_file_size = 30 * 1024 * 1024

        assert target_size == expected_file_size

        # Tested method without skipping paths (negative scenario to confirm)
        target_size, _ = FileManager.get(source_path=fr'/{source_path}',
                                         target_path=target_path_api)

        # In test folder there are only 5 files, each 10MB, size in bytes
        expected_file_size = 50 * 1024 * 1024

        assert target_size == expected_file_size

    # def test_compressing_downloaded_backup_working(self):
    #     """Verify size before compressing and after decompression has the same size"""
    #     # TODO write the test for compressing downloaded backup
    #     assert True is False
    #

    def test_uploaded_file_size_is_correct(self):
        """Test is uploading created random file size, download it via SCP
        and verifies downloaded file size equals uploaded"""
        # Create source path for a file to upload
        source_path = os.path.join(
            BASE_DIR,
            Config.get_config_value('TMP_DIR'),
            Config.get_config_value('TEST_DIR_UPLOAD_SOURCE'),
            Config.get_config_value('TEST_FILE_UPLOAD_1')
        )
        # Create upload path using tested method (file will be stored here on a server)
        target_path_api = os.path.join(
            Config.get_config_value('TEST_DIR_SOURCE'),
        )
        # Create target (file to download) path using SCP
        source_path_scp = os.path.join(
            Config.get_config_value('TEST_DIR_SOURCE'),
            Config.get_config_value('TEST_FILE_UPLOAD_1')
        )
        # Create download path using SCP
        target_path_scp = os.path.join(
            BASE_DIR,
            Config.get_config_value('BACKUP_DIR'),
            Config.get_config_value('DOWNLOAD_TEST_LOCATION_SCP'),
            Config.get_config_value('TEST_FILE_UPLOAD_1')
        )

        # Create source path directory if not exists
        if not os.path.exists(Path(source_path).parent):
            os.makedirs(Path(source_path).parent, exist_ok=True)

        # Create random size of file which is also expected one after download
        # Multiply 1024 * 1024 to get size in bytes
        import random
        expected_random_size = random.randint(5, 10) * 1024 * 1024

        # Create local file to upload
        with open(source_path, 'wb') as file:
            file.write(os.urandom(expected_random_size))

        # Tested method
        FileManager.put(source_path=source_path, target_path=fr'/{target_path_api}')

        # Not needed return values since comparison works on folder/file level base
        get_file_via_scp(source=fr'/{source_path_scp}', target=target_path_scp, recursive=False)
        target_upload_size = os.stat(Path(target_path_scp)).st_size

        assert target_upload_size == expected_random_size

    def test_uploaded_directory_size_is_correct(self):
        """Test is uploading created random file size, download it via SCP
        and verifies downloaded file size equals uploaded"""
        # Create source path for a directory to upload
        source_path = os.path.join(
            BASE_DIR,
            Config.get_config_value('TMP_DIR'),
            Config.get_config_value('TEST_DIR_UPLOAD_SOURCE'),
        )
        # Create upload path using tested method (directory will be stored here on a server)
        target_path_api = os.path.join(
            Config.get_config_value('TEST_DIR_SOURCE'),
        )
        # Create target (directory to download) path using SCP
        source_path_scp = os.path.join(
            Config.get_config_value('TEST_DIR_SOURCE'),
            Config.get_config_value('TEST_DIR_UPLOAD_SOURCE')
        )
        # Create download path using SCP
        target_path_scp = os.path.join(
            BASE_DIR,
            Config.get_config_value('BACKUP_DIR'),
            Config.get_config_value('DOWNLOAD_TEST_LOCATION_SCP'),
        )

        # Create source path directory if not exists
        if not os.path.exists(Path(source_path).parent):
            os.makedirs(Path(source_path).parent, exist_ok=True)

        # Create random size of file which is also expected one after download
        # Multiply 1024 * 1024 to get size in bytes
        import random
        expected_random_size = random.randint(5, 10) * 1024 * 1024

        # Create local files to upload inside directory to upload
        for file_to_upload in Config.get_config_values(['TEST_FILE_UPLOAD_0', 'TEST_FILE_UPLOAD_1', 'TEST_FILE_UPLOAD_2']):
            with open(os.path.join(source_path, file_to_upload), 'wb') as file:
                file.write(os.urandom(expected_random_size))

        # Tested method
        FileManager.put(source_path=source_path, target_path=fr'/{target_path_api}')

        # Not needed return values since comparison works on folder/file level base
        get_file_via_scp(source=fr'/{source_path_scp}', target=target_path_scp, recursive=True)
        directory = Path(target_path_scp)
        target_upload_size = sum(f.stat().st_size for f in directory.glob('**/*') if f.is_file())

        # Expected random size x3 because 3 files created
        assert target_upload_size == 3 * expected_random_size