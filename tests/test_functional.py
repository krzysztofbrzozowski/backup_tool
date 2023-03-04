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
        assert True is False
