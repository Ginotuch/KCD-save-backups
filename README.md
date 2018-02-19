# KCD-save-backups
This will automatically backup save games/profiles for the game Kingdom Come: Deliverance to avoid corruption.  
Keeps all backups, or overwrites older ones.

## Usage
* Download KCD-save-backups.py and place it anywhere.
* If needed change the amount of backups to keep in KCD-save-backups.py (line 10, default=20).  
* Setting it to 0 keeps infinite backups.  
* Then either run the file directly, or from the command line while playing KCD: `python KCD-save-backups.py`


## Notes
* If amount of backups is set to a high number, this **will** use a lot of diskspace. (After 5 hours of playing, and 20 backups, it used ~1.7GB on my system)  

* Default backup location: `[USER_DIRECTORY]\Save Games\backups`  
e.g. C:\Users\John Doe\Save Games\backups

* Q: Why does this script exist?  
A: I saw on Reddit and Steam that save corruption is a common issue, and didn't want to take any risks.

## Feature list
* Custom amount of backups to keep
* 10 second default refresh on new save data (uses almost no system resources, although customizable)
* Automatically renames backups if some were deleted
* Custom save location specification
* Custom backup directory location

#### Requirements
* Python 3+ (Tested with Python 3.6.4)
* Windows (Custom save/backup location required to be set on Linux)