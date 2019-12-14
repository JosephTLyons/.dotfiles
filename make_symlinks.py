#!/usr/bin/env python3

import errno

from os import listdir, remove, symlink
from os.path import isfile, join
from pathlib import Path

def make_symlink(action, path_to_file, path_to_symlink):
    symlink(path_to_file, path_to_symlink)
    print("Symlink", action + ":", path_to_symlink, "->", path_to_file)

def force_make_symlink(path_to_file, path_to_symlink):
    try:
        make_symlink("created", path_to_symlink, path_to_file)
    except OSError as e:
        if e.errno == errno.EEXIST:
            remove(path_to_symlink)
            make_symlink("overwritten", path_to_symlink, path_to_file)

def make_all_symlinks():
    excluded_items = [
        ".DS_Store",
        ".git",
        ".gitignore",
        "make_symlinks.py"
    ]

    home_path = Path.home()
    dotfile_directory_path = Path(home_path, ".dotfiles")

    files = [file for file in listdir(dotfile_directory_path) if isfile(join(dotfile_directory_path, file)) and str(file) not in excluded_items]

    for file in files:
        absolute_path_to_dotfile = Path(dotfile_directory_path, file)
        absolute_path_to_symlink = Path(home_path, file)

        force_make_symlink(absolute_path_to_dotfile, absolute_path_to_symlink)

    # Additional symlinks generated here
    force_make_symlink(Path(dotfile_directory_path, ".zprofile"), Path(home_path, ".profile"))

if __name__ == "__main__":
    make_all_symlinks()
