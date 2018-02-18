# KCD-save-backups
This will automatically backup save games/profiles for the game Kingdom Come: Deliverance to avoid corruption.  
Keeps all backups, or overwrites older ones.

### Usage
Change the amount of backups to keep in main.py (line 5) if needed. Setting it to 0 keeps infinite backups.  
Then either run the file, or from the command line: `python KCD-save-backups.py`

#### Requirements
* Python 3+ (Tested with Python 3.6.4)
* Packages: Toml, Requests