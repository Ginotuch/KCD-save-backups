import os
from time import sleep, ctime
import shutil
import pathlib

backup_size = 1  # 0 for infinite, otherwise maximum backups allowed. Number should always be integer 0 or greater
# Warning: backups can be large in file size, infinite backups can use up a lot of disk space


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
    print("Backup process started\n")
    while True:
        if get_max(save_location)[1] > max_time[1]:
            max_time = get_max(save_location)
            make_backup(save_location)
        sleep(20)  # Refresh time of checking for new save


def print_message():
    print("Backup made:", ctime())


def make_backup(save_location):
    backups_loc = os.path.join(save_location, "backups")
    old_backups = [d for d in os.listdir(backups_loc) if os.path.isdir(os.path.join(backups_loc, d))]
    if backup_size == 0:
        new_name = str(max([int(x[6:]) for x in old_backups]) + 1)
        source = os.path.join(save_location, "kingdomcome")
        destination = os.path.join(save_location, "backups", "backup{}".format(new_name))
        shutil.copytree(source, destination)
        print_message()

    else:
        while len(old_backups) > backup_size:
            old_backups.sort()
            shutil.rmtree(os.path.join(backups_loc, old_backups[0]))
            old_backups.pop(0)
            for backup in old_backups:
                os.rename(os.path.join(backups_loc, backup),
                          os.path.join(backups_loc, backup[:6] + str(int(backup[6:]) - 1)))
            old_backups = [d for d in os.listdir(backups_loc) if os.path.isdir(os.path.join(backups_loc, d))]

        if len(old_backups) < backup_size:
            new_name = "1" if len(old_backups) == 0 else str(max([int(x[6:]) for x in old_backups]) + 1)
            source = os.path.join(save_location, "kingdomcome")
            destination = os.path.join(save_location, "backups", "backup{}".format(new_name))
            shutil.copytree(source, destination)
            print_message()
        elif len(old_backups) == backup_size:
            old_backups.sort()
            shutil.rmtree(os.path.join(backups_loc, old_backups[0]))
            old_backups.pop(0)
            for backup in old_backups:
                os.rename(os.path.join(backups_loc, backup), os.path.join(backups_loc, backup[:6] + str(int(backup[6:]) - 1)))
            old_backups = [d for d in os.listdir(backups_loc) if os.path.isdir(os.path.join(backups_loc, d))]
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
