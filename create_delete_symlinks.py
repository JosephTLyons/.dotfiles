#!/usr/bin/env python3

import glob
import os
import pathlib


class SymlinkBase:
    def __init__(self):
        self.symlink_to_dotfile_dictionary = {}

        self.home_directory_path = pathlib.Path.home()
        self.dotfile_directory_path = pathlib.Path(os.getcwd() + "/files")
        self.add_all_items_in_directory_to_symlink_to_dotfile_dictionary(
            "Dotfiles", self.dotfile_directory_path, self.home_directory_path, "files"
        )

        self.atom_package_development_directory_path = self.home_directory_path / "github"
        self.atom_package_symlink_directory_path = self.home_directory_path / ".atom/packages"

        self.add_all_items_in_directory_to_symlink_to_dotfile_dictionary(
            "Atom Packages",
            self.atom_package_development_directory_path,
            self.atom_package_symlink_directory_path,
            "dirs",
        )

        self.add_custom_items_to_symlink_to_dotfile_dictionary()

    def run(self, action_function):
        for dictionary_name, dictionary in self.symlink_to_dotfile_dictionary.items():
            print(dictionary_name)

            if dictionary:
                action_function(dictionary)
            else:
                print("- No items in dictionary")

    def add_all_items_in_directory_to_symlink_to_dotfile_dictionary(
        self,
        new_dictionary_name,
        items_directory_path,
        desired_symlinks_directory_path,
        item_types_to_include,
    ):
        excluded_items = [".DS_Store"]
        excluded_items += glob.glob(".*~")

        inner_symlink_to_dotfile_dictionary = {}

        if items_directory_path.exists():
            for file in os.listdir(items_directory_path):
                path_to_item = os.path.join(items_directory_path, file)

                if item_types_to_include == "files":
                    is_correct_item_type = os.path.isfile(path_to_item)
                elif item_types_to_include == "dirs":
                    is_correct_item_type = os.path.isdir(path_to_item)
                else:
                    is_correct_item_type = True

                if is_correct_item_type and file not in excluded_items:
                    absolute_path_to_symlink = desired_symlinks_directory_path / file
                    absolute_path_to_dotfile = items_directory_path / file
                    inner_symlink_to_dotfile_dictionary[
                        absolute_path_to_symlink
                    ] = absolute_path_to_dotfile

            self.symlink_to_dotfile_dictionary[
                new_dictionary_name + " (Automatic)"
            ] = inner_symlink_to_dotfile_dictionary
        else:
            print(f"{items_directory_path} does not exist")

    def add_custom_items_to_symlink_to_dotfile_dictionary(self):
        inner_symlink_to_dotfile_dictionary = {
            self.home_directory_path / ".bashrc": self.dotfile_directory_path / ".zshrc",
            self.home_directory_path / ".profile": self.dotfile_directory_path / ".zprofile",
            self.home_directory_path / ".config/starship.toml": self.dotfile_directory_path / "starship.toml",
            pathlib.Path(
                "/usr/local/bin/subl"
            ): "/Applications/Sublime Text.app/Contents/SharedSupport/bin/subl",
        }

        self.symlink_to_dotfile_dictionary["Custom Items"] = inner_symlink_to_dotfile_dictionary


class CreateSymlinks(SymlinkBase):
    def __init__(self):
        super().__init__()

    def run(self):
        super().run(self.create_symlinks)

    @staticmethod
    def create_symlinks(dictionary):
        for i, (absolute_path_to_symlink, absolute_path_to_dotfile) in enumerate(
            dictionary.items()
        ):
            print(f"{i + 1}) ", end="")
            CreateSymlinks.create_symlink(absolute_path_to_dotfile, absolute_path_to_symlink)

    @staticmethod
    def create_symlink(path_to_file, path_to_symlink):
        try:
            os.symlink(path_to_file, path_to_symlink)
            action = "Created"
        except FileExistsError:
            action = "Already Exists"

        print(f"Symlink {action}: {path_to_symlink} -> {path_to_file}")


class DeleteSymlinks(SymlinkBase):
    def __init__(self):
        super().__init__()

    def run(self):
        super().run(self.delete_symlinks)

    @staticmethod
    def delete_symlinks(dictionary):
        for i, absolute_path_to_symlink in enumerate(dictionary.keys()):
            print(f"{i + 1}) ", end="")
            DeleteSymlinks.delete_symlink(absolute_path_to_symlink)

    @staticmethod
    def delete_symlink(absolute_path_to_symlink):
        try:
            os.remove(absolute_path_to_symlink)
            action = "Deleted"
        except FileNotFoundError:
            action = "Does Not Exist"

        print(f"Symlink {action}: {absolute_path_to_symlink}")


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
