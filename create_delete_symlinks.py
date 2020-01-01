#!/usr/bin/env python3

import glob
import os
import pathlib


def create_symlink(action, path_to_file, path_to_symlink):
    os.symlink(path_to_file, path_to_symlink)
    print("Symlink", action + ":", path_to_symlink, "->", path_to_file)

def force_create_symlink(path_to_file, path_to_symlink):
    try:
        create_symlink("Created", path_to_file, path_to_symlink)
    except FileExistsError:
        os.remove(path_to_symlink)
        create_symlink("Overwritten", path_to_file, path_to_symlink)

def delete_symlink(absolute_path_to_symlink):
    try:
        os.remove(absolute_path_to_symlink)
        print("Symlink Deleted:", absolute_path_to_symlink)
    except FileNotFoundError:
        print("Symlink Does Not Exist:", absolute_path_to_symlink)

def create_symlink_to_dotfile_dictionary():
    excluded_items = [".DS_Store"]
    excluded_items += glob.glob(".*~")

    home_directory_path = pathlib.Path.home()
    dotfile_directory_path = pathlib.Path(os.getcwd() + "/files")

    symlink_to_dotfile_dictionary = {}

    for file in os.listdir(dotfile_directory_path):
        if os.path.isfile(os.path.join(dotfile_directory_path, file)) and file not in excluded_items:
            absolute_path_to_symlink = pathlib.Path(home_directory_path, file)
            absolute_path_to_dotfile = pathlib.Path(dotfile_directory_path, file)
            symlink_to_dotfile_dictionary[absolute_path_to_symlink] = absolute_path_to_dotfile

    # Additional symlinks added here
    symlink_to_dotfile_dictionary[pathlib.Path(home_directory_path, ".profile")] = pathlib.Path(dotfile_directory_path, ".zprofile")

    return symlink_to_dotfile_dictionary

def create_symlinks():
    for (absolute_path_to_symlink, absolute_path_to_dotfile) in create_symlink_to_dotfile_dictionary().items():
        force_create_symlink(absolute_path_to_dotfile, absolute_path_to_symlink)

def delete_symlinks():
    for absolute_path_to_symlink in create_symlink_to_dotfile_dictionary().keys():
        delete_symlink(absolute_path_to_symlink)

if __name__ == "__main__":
    print("1: Create Symlinks")
    print("2: Delete Symlinks")

    try:
        user_input = int(input())
    except ValueError:
        user_input = 0

    if user_input == 1:
        create_symlinks()
    elif user_input == 2:
        delete_symlinks()
    else:
        print("Invalid Input")

# Clean up long lines
# Be able to run the script from any path and it still work correctly (IE, being in the script's parent folder)
