import os


def main():
    save_location = "testfolders"
    max_time = get_max(save_location)
    print(max_time)


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
