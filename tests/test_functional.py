"""
@author:    Krzysztof Brzozowski
@file:      test_functional
@time:      04/03/2023
@desc:      
"""
import os
import time

import pytest

from file_manager import FileManager
from private_file import *


class TestFunctionalBackupTool:
    # @pytest.fixture(autouse=True)
    # def setup_method(self, test_method):
    #     pass

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
        assert True is False

    def test_download_speed_is_correct(self):
        """Test is comparing download result using SCPClient and raw SCP call from console"""
        import subprocess
        import re

        FileManager.connect()

        # Manual call of scp and getting file size and speed
        call_args = f'scp -v -i {PKEY} {USER}@{HOST}:{SOURCE} {TARGET}'
        proc = subprocess.Popen(call_args, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for line in proc.stdout:
            if line != bytes():
                try:
                    line = line.decode().strip()
                    if re.search(r'Transferred:.*', line):
                        sent, transferred, time_transfer = re.findall(r'[\d+^.]+|\d+[.]\d+', line)
                        print(sent, transferred, time_transfer)
                except Exception as e:
                    # print(e)
                    pass
        proc.wait()

        expected_target_size = (int(transferred) - int(sent)) / (1024 * 1024)
        expected_download_speed = expected_target_size / float(time_transfer)
        print(f'{expected_download_speed:.2f} MB/s')

        # Tested method
        target_size, download_speed = FileManager.get(source_path=SOURCE, target_path=TARGET)

        assert expected_download_speed == download_speed
        assert expected_target_size == target_size





