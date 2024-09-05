"""Actions module for the app package."""

from typing import Any
from fapello_downloader.app.gui import CTkMessageBox


def show_error_message(app_instance: Any, exception: str) -> None:
    messageBox_title = "Download error"
    messageBox_subtitle = "Please report the error on Github or Telegram"
    messageBox_text = f" {str(exception)} "

    CTkMessageBox(
        app_instance=app_instance,
        messageType="error",
        title=messageBox_title,
        subtitle=messageBox_subtitle,
        default_value="",
        option_list=[messageBox_text],
    )


def open_info_simultaneous_downloads(app_instance: Any) -> None:
    CTkMessageBox(
        app_instance=app_instance,
        messageType = 'info',
        title = "Simultaneous downloads",
        subtitle = "This widget allows to choose how many files are downloaded simultaneously",
        default_value = "6",
        option_list = []
    )


def open_info_tips(app_instance: Any) -> None:
    CTkMessageBox(
        app_instance=app_instance,
        messageType   = 'info',
        title         = "Tips",
        subtitle      = "In case of problems with reaching the website, follow these tips",
        default_value = "",
        option_list   = [
            " Many internet providers block access to websites such as fapello.com",
            " In this case you can use custom DNS to solve the problem, by setting them in Windows",
            " The most popular DNS are Cloudflare 1.1.1.1 or Google 8.8.8.8",

            "\n To facilitate there is a free program called DNSJumper\n" +
            "    • it can find the best custom DNS for your internet line and set them directly\n" +
            "    • it can quickly revert to the default DNS in case of problems \n" +
            "    • has also a useful function called DNS Flush that solves problems connecting to the Fapello.com \n"
        ]
    )
