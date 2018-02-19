import os
import pathlib
import re
import shutil
import traceback
from time import sleep, ctime

# 0 for infinite, otherwise maximum backups allowed. Number should always be integer 0 or greater
# Warning: backups can be large in file size, infinite backups can use up a lot of disk space
backup_size = 20

# Set custom locations of where the game save is, and where to back them up
save_location = os.path.join(str(pathlib.Path.home()), "Saved Games", "kingdomcome")  # Default save file location
backup_location = os.path.join(str(pathlib.Path.home()), "Saved Games", "KCD_backups")  # Default backup directory

# Refresh interval in seconds (raise if script hurts system performance)
r_time = 10


def main():
    if not os.path.exists(save_location):
        print("kingdomcome SAVE FOLDER NOT FOUND AT", save_location)
        print("Please launch the game and create a save before running this script")
        print("If you think this message was shown in error, please make an issue at https://github.com/Ginotuch/KCD-save-backups/issues")
        input()
        exit()
    max_time = get_max()
    if not os.path.exists(backup_location):
        os.mkdir(backup_location)
    rename_existing_backups()
    print("Backup process started. Please keep this window open while playing the game.\n")
    while True:
        if get_max() > max_time:
            max_time = get_max()
            make_backup()
        sleep(r_time)  # Refresh time of checking for new save


def rename_existing_backups():
    old_backups = get_old_backups()
    if len(old_backups) > 0:
        try:
            a = [int(x[6:]) for x in old_backups]
            if a[-1] * (a[-1] + a[0]) / 2 - sum(a) != 0:  # Taken from https://stackoverflow.com/a/20718334
                for num in range(1, len(old_backups) + 1):
                    os.rename(os.path.join(backup_location, old_backups[num - 1]),
                              os.path.join(backup_location, "backup{}".format(str(num))))
        except ValueError:
            print("UNEXPECTED FOLDER/FILE IN BACKUPS LOCATION, PLEASE REMOVE EVERYTHING EXCEPT BACKUP FOLDERS AND LOGS")
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
    return [tryint(c) for c in re.split('([0-9]+)', s)]


def get_old_backups():
    old_backups = [d for d in os.listdir(backup_location) if
                   os.path.isdir(os.path.join(backup_location, d)) and d[:6] == "backup"]
    old_backups.sort(key=alphanum_key)
    return old_backups


def make_backup():
    old_backups = get_old_backups()
    if backup_size == 0:
        new_name = str(max([int(x[6:]) for x in old_backups]) + 1)
        destination = os.path.join(backup_location, "backup{}".format(new_name))
        shutil.copytree(save_location, destination)
        print_message()

    else:
        while len(old_backups) > backup_size:
            shutil.rmtree(os.path.join(backup_location, old_backups[0]))
            old_backups.pop(0)
            rename_existing_backups()
            old_backups = get_old_backups()

        if len(old_backups) < backup_size:
            new_name = "1" if len(old_backups) == 0 else str(max([int(x[6:]) for x in old_backups]) + 1)
            destination = os.path.join(backup_location, "backup{}".format(new_name))
            shutil.copytree(save_location, destination)
            print_message()
        elif len(old_backups) == backup_size:
            shutil.rmtree(os.path.join(backup_location, old_backups[0]))
            old_backups.pop(0)
            for backup in old_backups:
                os.rename(os.path.join(backup_location, backup),
                          os.path.join(backup_location, backup[:6] + str(int(backup[6:]) - 1)))
            old_backups = get_old_backups()
            new_name = "1" if len(old_backups) == 0 else str(max([int(x[6:]) for x in old_backups]) + 1)
            destination = os.path.join(backup_location, "backup{}".format(new_name))
            shutil.copytree(save_location, destination)
            print_message()


def get_max():
    max_time = 0
    for folder_path, folder_names, file_names in os.walk(save_location):
        for item in folder_names, file_names:
            for a in item:
                if os.path.getctime(os.path.join(folder_path, a)) > max_time:
                    max_time = os.path.getctime(os.path.join(folder_path, a))
    return max_time


def log_error(text):
    error_logs_loc = os.path.join(backup_location, "error_logs")
    if not os.path.exists(error_logs_loc):
        try:
            os.mkdir(error_logs_loc)
        except PermissionError:
            print("UNABLE TO CREATE ERROR LOG FOLDER, INSUFFICIENT PERMISSIONS")
            input()
            exit()
    errors = [f for f in os.listdir(error_logs_loc) if os.path.isfile(os.path.join(error_logs_loc, f))]
    if len(errors) == 0:
        log_file = os.path.join(error_logs_loc, "error1.log")
        with open(log_file, 'w') as output:
            output.write(text)
    else:
        log_file = os.path.join(error_logs_loc, "error{}.log".format(str(max([int(x[5:-4]) for x in errors]) + 1)))
        with open(log_file, 'w') as output:
            output.write(text)
    return log_file


if __name__ == "__main__":
    try:
        main()
    except:
        loc = log_error(str(traceback.format_exc()))
        print("UNRECOVERABLE ERROR OCCURED")
        print("ERROR LOG WRITTEN: {}".format(loc))
        print("PLEASE SUBMIT ISSUE WITH RELATED LOGS TO: https://github.com/Ginotuch/KCD-save-backups/issues")
        input()
        exit()
