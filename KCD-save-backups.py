import os
import pathlib
import re
import shutil
from time import sleep, ctime


# 0 for infinite, otherwise maximum backups allowed. Number should always be integer 0 or greater
# Warning: backups can be large in file size, infinite backups can use up a lot of disk space
backup_size = 20


def main():
    save_location = os.path.join(str(pathlib.Path.home()), "Saved Games")
    if not "kingdomcome" in os.listdir(save_location):
        print("kingdomcome SAVE FOLDER NOT FOUND IN", save_location)
        print("Please launch the game and create a save before running this script")
        print("If you think this message was shown in error, please make an issue at https://github.com/Ginotuch/KCD-save-backups")
        input()
        exit()
    max_time = get_max(save_location)
    if not os.path.exists(os.path.join(save_location, "backups")):
        os.mkdir(os.path.join(save_location, "backups"))
    rename_existing_backups(save_location)
    print("Backup process started\n")
    while True:
        if get_max(save_location)[1] > max_time[1]:
            max_time = get_max(save_location)
            make_backup(save_location)
        sleep(20)  # Refresh time of checking for new save


def rename_existing_backups(save_location):
    old_backups = get_old_backups(save_location)
    if len(old_backups) > 0:
        try:
            a = [int(x[6:]) for x in old_backups]
            if a[-1] * (a[-1] + a[0]) / 2 - sum(a) != 0:
                for num in range(1, len(old_backups) + 1):
                    os.rename(os.path.join(save_location, "backups", old_backups[num - 1]),
                              os.path.join(save_location, "backups", "backup{}".format(str(num))))
        except ValueError:
            print("UNEXPECTED FOLDER/FILE IN BACKUPS LOCATION, PLEASE REMOVE EVERYTHING EXCEPT BACKUP FOLDERS")
            input()
            exit()


def print_message():
    print("Backup made:", ctime())


"""
the two functions below were taken from Daniel DiPaolo's Stackoverflow answer: https://stackoverflow.com/a/4623518
"""


def tryint(s):
    try:
        return int(s)
    except:
        return s


def alphanum_key(s):
    """ Turn a string into a list of string and number chunks.
        "z23a" -> ["z", 23, "a"]
    """
    return [ tryint(c) for c in re.split('([0-9]+)', s) ]


def get_old_backups(save_location):
    backups_loc = os.path.join(save_location, "backups")
    old_backups = [d for d in os.listdir(backups_loc) if os.path.isdir(os.path.join(backups_loc, d))]
    old_backups.sort(key=alphanum_key)
    return old_backups


def make_backup(save_location):
    backups_loc = os.path.join(save_location, "backups")
    old_backups = get_old_backups(save_location)
    if backup_size == 0:
        new_name = str(max([int(x[6:]) for x in old_backups]) + 1)
        source = os.path.join(save_location, "kingdomcome")
        destination = os.path.join(save_location, "backups", "backup{}".format(new_name))
        shutil.copytree(source, destination)
        print_message()

    else:
        while len(old_backups) > backup_size:
            shutil.rmtree(os.path.join(backups_loc, old_backups[0]))
            old_backups.pop(0)
            for backup in old_backups:
                os.rename(os.path.join(backups_loc, backup),
                          os.path.join(backups_loc, backup[:6] + str(int(backup[6:]) - 1)))
            old_backups = get_old_backups(save_location)

        if len(old_backups) < backup_size:
            new_name = "1" if len(old_backups) == 0 else str(max([int(x[6:]) for x in old_backups]) + 1)
            source = os.path.join(save_location, "kingdomcome")
            destination = os.path.join(save_location, "backups", "backup{}".format(new_name))
            shutil.copytree(source, destination)
            print_message()
        elif len(old_backups) == backup_size:
            shutil.rmtree(os.path.join(backups_loc, old_backups[0]))
            old_backups.pop(0)
            for backup in old_backups:
                os.rename(os.path.join(backups_loc, backup),
                          os.path.join(backups_loc, backup[:6] + str(int(backup[6:]) - 1)))
            old_backups = get_old_backups(save_location)
            new_name = "1" if len(old_backups) == 0 else str(max([int(x[6:]) for x in old_backups]) + 1)
            source = os.path.join(save_location, "kingdomcome")
            destination = os.path.join(save_location, "backups", "backup{}".format(new_name))
            shutil.copytree(source, destination)
            print_message()


def get_max(save_location):
    max_time = (0, 0)
    save_location += "\\kingdomcome"
    for folder_path, folder_names, file_names in os.walk(save_location):
        for item in folder_names, file_names:
            for a in item:
                if os.path.getctime(os.path.join(folder_path, a)) > max_time[1]:
                    max_time = (os.path.join(folder_path, a), os.path.getctime(os.path.join(folder_path, a)))
    return max_time


if __name__ == "__main__":
    main()
