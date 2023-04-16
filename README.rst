Current tests status
====

.. raw:: html

    <a><img src="https://github.com/krzysztofbrzozowski/backup_tool//actions/workflows/tests.yaml/badge.svg" alt="No message"/></a>

Tool for backup management
====

System requirements for for project:

* System downloads files form target source to selected local directory
* Allows recursively download
* Selected files to backup are written in JSON or YAML file
* When downloading files, progress and speed shall be displayed
* Zip or tar downloaded files
* Last backup time shall be stored and displayed when new backup is staring or displayed via selected command
* Possibility to use the tool via command line
* Tests shall be written to deliver quality and reliable DevOps tool

TESTING AFTER DOWNLOAD
====
Currently all of the tests are written to run on port 2222 in docker image.
After download repository you run all of your tests using docker image which is providing SSH/SCP server.
You can use any IDE for testing but here is example how to set up everything using PyCharm.

* Download and install Docker
* Create virtual env and install requirements.txt

.. code-block:: console

    virtualenv venv
    source source venv/bin/activate
    pip install -r requirements.txt

* Generate pair of SSH test keys

.. code-block:: console

    ssh-keygen -t ed25519 -C root
    # display your public key
    cat /place/to/store/sshkey/id_ed25519.pub
    # display your private key
    cat /place/to/store/sshkey/id_ed25519

* Put your public key into Dockerfile

.. raw:: html

    <a><img src="https://krzysztofbrzozowski.com/media/2023/04/16/backup_toop_pubkey.png" alt="No message"/></a>


Set up environment variable with path to your local copy of backup_tool.

.. code-block:: console

    # .zshrc
    export BACKUP_TOOL_DIR="absolute/path/to/backup_tool"

.. code-block:: console

    source ~/.zshrc





Generate SSH keys for test user and push it to your server. Set up key details in config_backup_tool.yaml.

.. code-block:: yaml

    # Test user for running tests
    TEST_USER:
      # Server details
      HOST:       your_remote_test_host
      USER:       your_remote_test_user

      # Private key details
      PKEY:       your_private_key_for_test
      PASSPHRASE: your_private_key_passphrase_for_test

Paths for tests are coded in config/config_backup_tool.yaml

.. code-block:: yaml

    # Backup target path
    BACKUP_DIR:     backup.nosync

    # Test paths for recursive download (absolute)
    TEST_DIR_SOURCE:              largefiles

    # Test paths for file download
    TEST_FILE_0:                  largefile_0
    TEST_FILE_1:                  largefile_1
    TEST_FILE_2:                  largefile_2

    TEST_FILE_TO_SKIP:            file_to_skip_0
    TEST_DIR_TO_SKIP:
    - folder_to_skip
    - largefiles_upload

    DOWNLOAD_TEST_LOCATION_SCP:   test_artifacts/scp_call
    DOWNLOAD_TEST_LOCATION_API:   test_artifacts/api_call

    # temporary folder
    TMP_DIR:                      tmp

    # Test path for recursive upload
    TEST_DIR_UPLOAD_SOURCE:       largefiles_upload

    # Test paths for file upload
    TEST_FILE_UPLOAD_0:           largefile_upload_0
    TEST_FILE_UPLOAD_1:           largefile_upload_1
    TEST_FILE_UPLOAD_2:           largefile_upload_2

Run the tests

Prepare Dockerfile to mock your test server

.. code-block:: console

    pytest -v tests/test_functional.py

Current test output:

.. code-block:: console

    tests/test_functional.py::TestFunctionalBackupTool::test_connection_raises_exception_if_key_not_correct FAILED                                                          [ 12%]
    tests/test_functional.py::TestFunctionalBackupTool::test_login_via_ssh_possible PASSED                                                                                  [ 25%]
    tests/test_functional.py::TestFunctionalBackupTool::test_remote_commands_execution_working PASSED                                                                       [ 37%]
    tests/test_functional.py::TestFunctionalBackupTool::test_downloaded_file_size_is_correct PASSED                                                                         [ 50%]
    tests/test_functional.py::TestFunctionalBackupTool::test_downloaded_directory_size_is_correct PASSED                                                                    [ 62%]
    tests/test_functional.py::TestFunctionalBackupTool::test_download_speed_is_correct FAILED                                                                               [ 75%]
    tests/test_functional.py::TestFunctionalBackupTool::test_skip_path_is_working_for_directory PASSED                                                                      [ 87%]
    tests/test_functional.py::TestFunctionalBackupTool::test_skip_path_is_working_for_file PASSED                                                                           [100%]

Known issues:

.. code-block:: console

    tests/test_functional.py::TestFunctionalBackupTool::test_connection_raises_exception_if_key_not_correct FAILED
    tests/test_functional.py::TestFunctionalBackupTool::test_download_speed_is_correct FAILED

HOW TO USE TOOL
====
Generate SSH keys for regular user and push it to your server. Set up key details in config/config_backup_tool.yaml.

.. code-block:: yaml

    your_pc_name:
      # Server details
      HOST:       your_remote_host
      USER:       your_remote_user

      # Private key details
      PKEY:       your_private_key
      PASSPHRASE: your_private_key_passphrase

      # Backup/backup compressed target path (absolute)
      BACKUP_DIR:             your_backup_dir
      BACKUP_DIR_COMPRESSED:  your_backup_dir_compressed


Put paths you want to backup and which one you want to skip in config/backup_source.yaml

.. code-block:: yaml

    # Source to download
    backup_source:
      - /home/xyz/some_folder_0
      - /home/xyz/some_folder_1

    # Skip selected files or folders
    backup_source_skip:
      - /home/xyz/some_folder_0/some_folder_to_skip
      - /home/xyz/some_folder_1/some_folder_to_skip

Replace backup_source_private.yaml to backup_source.yaml (with your settings)

.. code-block:: python

    with open(os.path.join(os.getenv('BACKUP_TOOL_DIR', None), 'config', 'backup_source_private.yaml'), 'r') as file:

In Python you can use

.. code-block:: python

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

        # Compress backup
        FileManager.tar_backup()


TODO
----
* [X] Import directories to backup form YAML
* [] Pack files into one one to speed up backup process
* [X] Run tests in Docker Container instead of regular server
* [X] Create tar or zip after download
* [] Test creating tar or zip after download
* [X] Put all the settings in YAML config
* [X] Use different logger in tests than in regular call -> switched off logging as tem solution
* [X] Create put method
* [X] Test put method
* [] Add skip path for put method
* [X] Create method to remotely execute commands
* [X] Test remote cmd execution method
* [X] Prepare tar from sql db
* [] Add logging to important methods/steps