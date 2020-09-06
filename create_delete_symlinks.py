#!/usr/bin/env python3

import glob
import os
import pathlib


def create_symlink(path_to_file, path_to_symlink):
    try:
        os.symlink(path_to_file, path_to_symlink)
        action = "Created"
    except FileExistsError:
        action = "Already Exists"

    print("Symlink", action + ":", path_to_symlink, "->", path_to_file)


def delete_symlink(absolute_path_to_symlink):
    try:
        os.remove(absolute_path_to_symlink)
        action = "Deleted"
    except FileNotFoundError:
        action = "Does Not Exist"

    print("Symlink", action + ":", absolute_path_to_symlink)


def add_default_items_to_symlink_to_dotfile_dictionary(
    symlink_to_dotfile_dictionary,
    home_directory_path,
    dotfile_directory_path
):
    excluded_items = [".DS_Store"]
    excluded_items += glob.glob(".*~")

    for file in os.listdir(dotfile_directory_path):
        if os.path.isfile(os.path.join(dotfile_directory_path, file)) and file not in excluded_items:
            absolute_path_to_symlink = pathlib.Path(home_directory_path, file)
            absolute_path_to_dotfile = pathlib.Path(
                dotfile_directory_path, file)
            symlink_to_dotfile_dictionary[absolute_path_to_symlink] = absolute_path_to_dotfile


def add_custom_items_to_symlink_to_dotfile_dictionary(
    symlink_to_dotfile_dictionary,
    home_directory_path,
    dotfile_directory_path
):
    symlink_to_dotfile_dictionary[pathlib.Path(
        home_directory_path, ".bashrc")] = pathlib.Path(dotfile_directory_path, ".zshrc")
    symlink_to_dotfile_dictionary[pathlib.Path(
        home_directory_path, ".profile")] = pathlib.Path(dotfile_directory_path, ".zprofile")


def create_symlink_to_dotfile_dictionary():
    home_directory_path = pathlib.Path.home()
    dotfile_directory_path = pathlib.Path(os.getcwd() + "/files")

    symlink_to_dotfile_dictionary = {}

    add_default_items_to_symlink_to_dotfile_dictionary(
        symlink_to_dotfile_dictionary,
        home_directory_path,
        dotfile_directory_path
    )
    add_custom_items_to_symlink_to_dotfile_dictionary(
        symlink_to_dotfile_dictionary,
        home_directory_path,
        dotfile_directory_path
    )

    return symlink_to_dotfile_dictionary


def create_symlinks():
    for i, (absolute_path_to_symlink, absolute_path_to_dotfile) in enumerate(create_symlink_to_dotfile_dictionary().items()):
        print(f"{i + 1}) ", end="")
        create_symlink(absolute_path_to_dotfile, absolute_path_to_symlink)


def delete_symlinks():
    for i, absolute_path_to_symlink in enumerate(create_symlink_to_dotfile_dictionary().keys()):
        print(f"{i + 1}) ", end="")
        delete_symlink(absolute_path_to_symlink)


if __name__ == "__main__":
    print("1) Create Symlinks")
    print("2) Delete Symlinks")

    try:
        user_input = int(input())
    except ValueError:
        user_input = 0

    print()

    if user_input == 1:
        create_symlinks()
    elif user_input == 2:
        delete_symlinks()
    else:
        print("Invalid Input")
