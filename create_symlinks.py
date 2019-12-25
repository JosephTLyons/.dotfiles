#!/usr/bin/env python3

import errno
import glob
import os
import pathlib


def create_symlink(action, path_to_file, path_to_symlink):
    os.symlink(path_to_file, path_to_symlink)
    print("Symlink", action + ":", path_to_symlink, "->", path_to_file)

def force_create_symlink(path_to_file, path_to_symlink):
    try:
        create_symlink("created", path_to_file, path_to_symlink)
    except OSError as error:
        if error.errno == errno.EEXIST:
            os.remove(path_to_symlink)
            create_symlink("overwritten", path_to_file, path_to_symlink)

def create_symlinks():
    excluded_items = [
        ".DS_Store"
    ]

    excluded_items += glob.glob(".*~")

    home_directory_path = pathlib.Path.home()
    dotfile_directory_path = pathlib.Path(os.getcwd() + "/files")

    for file in os.listdir(dotfile_directory_path):
        if os.path.isfile(os.path.join(dotfile_directory_path, file)) and file not in excluded_items:
            absolute_path_to_dotfile = pathlib.Path(dotfile_directory_path, file)
            absolute_path_to_symlink = pathlib.Path(home_directory_path, file)

            force_create_symlink(absolute_path_to_dotfile, absolute_path_to_symlink)

    # Additional symlinks generated here
    force_create_symlink(
        pathlib.Path(dotfile_directory_path, ".zprofile"),
        pathlib.Path(home_directory_path, ".profile")
    )

if __name__ == "__main__":
    create_symlinks()




# Have main run a while loop asking if user wants to create or delete symlinks