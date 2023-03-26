#!/usr/bin/env python
"""
@author:    Krzysztof Brzozowski
@file:      run
@time:      26/03/2023
@desc:  
"""
import logging
import sys
from pathlib import Path
from argparse import ArgumentParser, Action
from shutil import rmtree
from subprocess import Popen, PIPE, TimeoutExpired


sys.tracebacklimit = 8
logging.basicConfig(level='INFO', format='%(message)s')
log = logging.getLogger(__name__)

BASE_DIR = Path(__file__).parent


def run(cmd, timeout=None):
    process = Popen(cmd, stdout=PIPE, shell=True)
    while process.poll() is None:
        try:
            stdout, stderr = process.communicate(timeout=timeout)
        except TimeoutExpired:
            process.kill()
            raise TimeoutError from None
        if stdout:
            print(stdout.decode())
    return process.returncode

class Install(Action):
    def __call__(self, parser, namespace, folder, *args, **kwargs):
        if folder is None:
            folder = '.'
        run('clear && printf "\e[3J"')  # noqa
        run(f'pip install -r {folder}/requirements.txt')
        log.info('Requirements installed')


class UnitTests(Action):
    def __call__(self, parser, namespace, paths, *args, **kwargs):
        run('clear && printf "\e[3J"')  # noqa
        all_tests = 0
        files = sorted(self.get_files(paths))
        for file in files:
            if self.is_ignored(file): continue
            if self.is_venv(file): continue
            if self.is_skipped(file): continue
            if count := self.count_unittests(file):
                self.run_doctest(file)
                all_tests += count
            else:
                log.error(f'NOTESTS\t{file}')
        logging.warning(f'\nAll tests {all_tests}')

    @staticmethod
    def is_ignored(file: Path):
        doctestignore = Path(file.parts[0]) / '.doctestignore'
        if doctestignore.exists():
            log.warning(f'IGNORED\t{file}')
            return True
        else:
            return False

    @staticmethod
    def is_skipped(file: Path):
        if '# doctest: +SKIP_FILE' in file.read_text():
            log.warning(f'SKIPPED\t{file}')
            return True
        else:
            return False

    @staticmethod
    def is_venv(file: Path):
        log.debug(f'VENV\t{file}')
        return str(file).startswith('.venv-py')

    @staticmethod
    def count_unittests(file: Path):
        return file.read_text().count('test_')

    @staticmethod
    def get_files(paths: str):
        for path in map(Path, paths):
            if path == Path(''):
                continue
            elif not path.exists():
                continue
            elif path.suffix in ('.rst', '.py'):
                yield path
            else:
                yield from Path(path).rglob('*.rst')
                yield from Path(path).rglob('*.py')

    @staticmethod
    def run_doctest(file: Path):
        log.debug(f'RUN\t {file}')
        try:
            exitcode = run(f'python -m unittest -v {file}', timeout=20)
        except TimeoutError:
            log.error(f'TIMEOUT\t{file}')
            exit(1)
        if exitcode == 0:
            log.info(f'PASSED\t{file}')
        else:
            log.critical(f'FAILED\t{file}')
            exit(1)


class PyTests(Action):
    def __call__(self, parser, namespace, paths, *args, **kwargs):
        run('clear && printf "\e[3J"')  # noqa
        all_tests = 0
        files = sorted(self.get_files(paths))
        for file in files:
            if self.is_ignored(file): continue
            if self.is_venv(file): continue
            if self.is_skipped(file): continue
            if count := self.count_unittests(file):
                self.run_doctest(file)
                all_tests += count
            else:
                log.error(f'NOTESTS\t{file}')
        logging.warning(f'\nAll tests {all_tests}')

    @staticmethod
    def is_ignored(file: Path):
        doctestignore = Path(file.parts[0]) / '.doctestignore'
        if doctestignore.exists():
            log.warning(f'IGNORED\t{file}')
            return True
        else:
            return False

    @staticmethod
    def is_skipped(file: Path):
        if '# doctest: +SKIP_FILE' in file.read_text():
            log.warning(f'SKIPPED\t{file}')
            return True
        else:
            return False

    @staticmethod
    def is_venv(file: Path):
        log.debug(f'VENV\t{file}')
        return str(file).startswith('.venv-py')

    @staticmethod
    def count_unittests(file: Path):
        return file.read_text().count('test_')

    @staticmethod
    def get_files(paths: str):
        for path in map(Path, paths):
            if path == Path(''):
                continue
            elif not path.exists():
                continue
            elif path.suffix in ('.rst', '.py'):
                yield path
            else:
                yield from Path(path).rglob('*.rst')
                yield from Path(path).rglob('*.py')

    @staticmethod
    def run_doctest(file: Path):
        log.debug(f'RUN\t {file}')
        try:
            exitcode = run(f'python -m pytest -v {file}', timeout=20)
        except TimeoutError:
            log.error(f'TIMEOUT\t{file}')
            exit(1)
        if exitcode == 0:
            log.info(f'PASSED\t{file}')
        else:
            log.critical(f'FAILED\t{file}')
            exit(1)


if __name__ == '__main__':
    parser = ArgumentParser()

    parser.add_argument('--unittest',
                        nargs='+', metavar='UNITTEST_FILE', action=UnitTests,
                        help='--unittest *.py files')

    parser.add_argument('--pytest',
                        nargs='+', metavar='UNITTEST_FILE', action=PyTests,
                        help='--unittest *.py files')

    parser.add_argument('--install',
                        nargs='?', metavar='INSTALL_FILE', action=Install,
                        help='install requirements')

    parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        exit(1)
