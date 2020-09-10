#!/usr/bin/env python3

import glob
import os
import pathlib


class SymlinkBase:
    def __init__(self):
        self.symlink_to_dotfile_dictionary = {}
        self.home_directory_path = pathlib.Path.home()
        self.dotfile_directory_path = pathlib.Path(os.getcwd() + "/files")

        self.add_default_items_to_symlink_to_dotfile_dictionary()
        self.add_custom_items_to_symlink_to_dotfile_dictionary()

    def run(self):
        raise NotImplementedError

    def add_default_items_to_symlink_to_dotfile_dictionary(self):
        excluded_items = [".DS_Store"]
        excluded_items += glob.glob(".*~")

        for file in os.listdir(self.dotfile_directory_path):
            if os.path.isfile(os.path.join(self.dotfile_directory_path, file)) and file not in excluded_items:
                absolute_path_to_symlink = pathlib.Path(
                    self.home_directory_path, file)
                absolute_path_to_dotfile = pathlib.Path(
                    self.dotfile_directory_path, file)
                self.symlink_to_dotfile_dictionary[absolute_path_to_symlink] = absolute_path_to_dotfile

    def add_custom_items_to_symlink_to_dotfile_dictionary(self):
        self.symlink_to_dotfile_dictionary[pathlib.Path(
            self.home_directory_path, ".bashrc")] = pathlib.Path(self.dotfile_directory_path, ".zshrc")
        self.symlink_to_dotfile_dictionary[pathlib.Path(
            self.home_directory_path, ".profile")] = pathlib.Path(self.dotfile_directory_path, ".zprofile")
        self.symlink_to_dotfile_dictionary[pathlib.Path(
            "/usr/local/bin/subl")] = pathlib.Path(self.dotfile_directory_path, "/Applications/Sublime Text.app/Contents/SharedSupport/bin/subl")


class CreateSymlinks(SymlinkBase):
    def __init__(self):
        super().__init__()

    def run(self):
        self.create_symlinks()

    def create_symlinks(self):
        for i, (absolute_path_to_symlink, absolute_path_to_dotfile) in enumerate(self.symlink_to_dotfile_dictionary.items()):
            print(f"{i + 1}) ", end="")
            self.create_symlink(absolute_path_to_dotfile,
                                absolute_path_to_symlink)

    def create_symlink(self, path_to_file, path_to_symlink):
        try:
            os.symlink(path_to_file, path_to_symlink)
            action = "Created"
        except FileExistsError:
            action = "Already Exists"

        print("Symlink", action + ":", path_to_symlink, "->", path_to_file)


class DeleteSymlinks(SymlinkBase):
    def __init__(self):
        super().__init__()

    def run(self):
        self.delete_symlinks()

    def delete_symlinks(self):
        for i, absolute_path_to_symlink in enumerate(self.symlink_to_dotfile_dictionary.keys()):
            print(f"{i + 1}) ", end="")
            self.delete_symlink(absolute_path_to_symlink)

    def delete_symlink(self, absolute_path_to_symlink):
        try:
            os.remove(absolute_path_to_symlink)
            action = "Deleted"
        except FileNotFoundError:
            action = "Does Not Exist"

        print("Symlink", action + ":", absolute_path_to_symlink)


if __name__ == "__main__":
    print("1) Create Symlinks")
    print("2) Delete Symlinks")

    try:
        user_input = int(input())
    except ValueError:
        user_input = 0

    print()

    if user_input == 1:
        create_symlinks = CreateSymlinks()
        create_symlinks.run()
    elif user_input == 2:
        delete_symlinks = DeleteSymlinks()
        delete_symlinks.run()
    else:
        print("Invalid Input")
