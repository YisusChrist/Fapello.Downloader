"""Constants for the application."""

from os import sep as os_separator

from customtkinter import CTkFont, CTkImage  # type: ignore
from PIL.Image import open as pillow_image_open

from fapello_downloader.utils import find_by_relative_path

ASSETS_PATH: str = find_by_relative_path("assets")


# Fonts
def create_fonts() -> dict[str, CTkFont]:
    # Initialize the fonts after the root window is created
    font = "Segoe UI"
    return {
        "bold8": CTkFont(family=font, size=8, weight="bold"),
        "bold9": CTkFont(family=font, size=9, weight="bold"),
        "bold10": CTkFont(family=font, size=10, weight="bold"),
        "bold11": CTkFont(family=font, size=11, weight="bold"),
        "bold12": CTkFont(family=font, size=12, weight="bold"),
        "bold13": CTkFont(family=font, size=13, weight="bold"),
        "bold14": CTkFont(family=font, size=14, weight="bold"),
        "bold16": CTkFont(family=font, size=16, weight="bold"),
        "bold17": CTkFont(family=font, size=17, weight="bold"),
        "bold18": CTkFont(family=font, size=18, weight="bold"),
        "bold19": CTkFont(family=font, size=19, weight="bold"),
        "bold20": CTkFont(family=font, size=20, weight="bold"),
        "bold21": CTkFont(family=font, size=21, weight="bold"),
        "bold22": CTkFont(family=font, size=22, weight="bold"),
        "bold23": CTkFont(family=font, size=23, weight="bold"),
        "bold24": CTkFont(family=font, size=24, weight="bold"),
    }


# Images
logo_git = CTkImage(
    pillow_image_open(
        find_by_relative_path(f"{ASSETS_PATH}{os_separator}github_logo.png")
    ),
    size=(15, 15),
)
logo_telegram = CTkImage(
    pillow_image_open(
        find_by_relative_path(f"{ASSETS_PATH}{os_separator}telegram_logo.png")
    ),
    size=(15, 15),
)
stop_icon = CTkImage(
    pillow_image_open(
        find_by_relative_path(f"{ASSETS_PATH}{os_separator}stop_icon.png")
    ),
    size=(15, 15),
)
info_icon = CTkImage(
    pillow_image_open(
        find_by_relative_path(f"{ASSETS_PATH}{os_separator}info_icon.png")
    ),
    size=(14, 14),
)
download_icon = CTkImage(
    pillow_image_open(
        find_by_relative_path(f"{ASSETS_PATH}{os_separator}download_icon.png")
    ),
    size=(15, 15),
)
logo_qs = CTkImage(
    pillow_image_open(find_by_relative_path(f"{ASSETS_PATH}{os_separator}qs_logo.png")),
    size=(15, 15),
)
