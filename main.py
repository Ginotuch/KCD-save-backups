import os
from time import sleep
import shutil

backup_size = 0  # 0 for infinite, otherwise maximum backups


def main():
    save_location = "testfolders"
    make_backup(save_location)
    max_time = get_max(save_location)
    if not os.path.exists(os.path.join(save_location, "backups")):
        os.mkdir(os.path.join(save_location, "backups"))
    while True:
        if get_max(save_location)[1] > max_time[1]:
            max_time = get_max(save_location)
            make_backup(save_location)
        sleep(1)


def make_backup(save_location):
    backups_loc = os.path.join(save_location, "backups")
    old_backups = [d for d in os.listdir(backups_loc) if os.path.isdir(os.path.join(backups_loc, d))]
    if backup_size == 0:
        new_name = str(max([int(x[6:]) for x in old_backups]) + 1)
        source = os.path.join(save_location, "kingdomcome")
        destination = os.path.join(save_location, "backups", "backup{}".format(new_name))
        shutil.copytree(source, destination)



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
