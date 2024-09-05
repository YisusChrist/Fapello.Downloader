"""Utility functions for the program."""

import sys
from fnmatch import filter as fnmatch_filter
from os import listdir as os_listdir
from os import makedirs as os_makedirs
from os.path import abspath as os_path_abspath
from os.path import dirname as os_path_dirname
from os.path import exists as os_path_exists
from os.path import join as os_path_join
from shutil import rmtree
from webbrowser import open as open_browser

from fapello_downloader.consts import githubme, qs_link, telegramme


def opengithub() -> None:
    open_browser(githubme, new=1)


def opentelegram() -> None:
    open_browser(telegramme, new=1)


def openqualityscaler() -> None:
    open_browser(qs_link, new=1)


def find_by_relative_path(relative_path: str) -> str:
    base_path = getattr(sys, '_MEIPASS', os_path_dirname(os_path_abspath(__file__)))
    return os_path_join(base_path, relative_path)


def create_temp_dir(name_dir: str) -> None:
    if os_path_exists(name_dir):
        rmtree(name_dir)
    if not os_path_exists(name_dir):
        os_makedirs(name_dir, mode=0o777)


def stop_thread():
    stop = 1 + "x"


def prepare_filename(file_url, index, file_type):
    first_part_filename = str(file_url).split("/")[-3]

    if file_type == "image":
        extension = ".jpg"
    elif file_type == "video":
        extension = ".mp4"

    filename = first_part_filename + "_" + str(index) + extension

    return filename


def count_files_in_directory(target_dir: str) -> int:
    return len(fnmatch_filter(os_listdir(target_dir), "*.*"))
