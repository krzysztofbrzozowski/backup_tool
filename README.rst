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
    sources = FileManager.get_backup_positions()

    # Get every file via SCP
    # TODO Write it better (add it to one fucntion)
    for source in sources:
        FileManager.get(source_path=source, target_path=TARGET_DIR, recursive=True)