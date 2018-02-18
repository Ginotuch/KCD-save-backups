# KCD-save-backups
This will automatically backup save games/profiles for the game Kingdom Come: Deliverance to avoid corruption.  
Keeps all backups, or overwrites older ones.

## Usage
* Change the amount of backups to keep in KCD-save-backups.py (line 5) if needed (default=20).  
* Setting it to 0 keeps infinite backups.  
* Then either run the file directly, or from the command line while playing KCD: `python KCD-save-backups.py`


## Notes
* If amount of backups is set to a high number, this **will** use a lot of diskspace. (After 5 hours of playing, and 20 backups, it used ~1.7GB on my system)  

* Backup location: [USER_DIRECTORY]\Save Games\backups  
e.g. C:\Users\John Doe\Save Games\backups

* Q: Why does this script exist?  
A: I saw on Reddit and Steam that save corruption is a common issue, and didn't want to take any risks.

#### Requirements
* Python 3+ (Tested with Python 3.6.4)