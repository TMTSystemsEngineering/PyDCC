# PyDCC

This is a set of Python tools for automating tasks on Docushare.

# Upgrading from previous GitHub repository
For users converting from using the previous GitHub projects, the following steps will 
be needed to use this new repository.

## Config Files
* Copy pyDCC/Config/Config_example.py to Config.py
* Edit Config.py per the instructions in the file
* If you are migrating to the PyDCC project you will have to copy over and edit your 
Config.py file for the location of: 
    - tracetreefilepath
    - dccfilepath
    - reportfilepath

## Secrets file
* Copy PyDCC/Secrets/secrets_example.py to secrets.py
* Edit secrets.py per the instructions in the file
* If you are migrating to the PyDCC project should be able to just copy over your existing 
secrets.py file (if you had one)


## PYTHONPATH
* Set the PYTHONPATH to point to the PyDCC/Config, PyDCC/Secrets, and PyDCC/Library directories