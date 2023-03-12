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

Project description
====
.. code-block:: python

    if __name__ == '__main__':
        # Connect via SSH
        FileManager.connect()

        # Get all backup sources
        backup_paths, skip_paths = FileManager.get_backup_positions()

        # Get source files/directories via SCP
        FileManager.get(source_path=backup_paths, target_path=TARGET_DIR, skip_path=skip_paths)


How to use tool
====
Generate SSH keys and push it to your server.
Set up key details in config_backup_tool.yaml

.. code-block:: yaml

    # Test user for running tests
    TEST_USER:
      # Server details
      HOST:       your_remote_test_host
      USER:       your_remote_test_user

      # Private key details
      PKEY:       your_private_key_for_test
      PASSPHRASE: your_private_key_passphrase_for_test


Set up the config_backup_tool.yaml for running tests


TODO
----
* [X] Import directories to backup form YAML
* Create tar or zip after download
* [X] Put all the settings in YAML config
* [X] Use different logger in tests than in regular call -> switched off logging as tem solution
* Create put method
* Test put method
* [X] Create method to remotely execute commands
* [X] Test remote cmd execution method
* [] Prepare tar from sql db