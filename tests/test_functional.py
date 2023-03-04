"""
@author:    Krzysztof Brzozowski
@file:      test_functional
@time:      04/03/2023
@desc:      
"""
import os
import pytest


class TestFunctionalBackupTool:
    @pytest.fixture(autouse=True)
    def setup_startup(self):
        pass

    def test_login_via_ssh_possible(self):
        assert True is False

    def test_downloaded_file_is_correct(self):
        assert True is False

    def test_download_speed_is_correct(self):
        assert True is False
