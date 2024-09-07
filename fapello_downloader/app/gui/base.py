"""Graphical User Interface module for the downloader."""

from os import sep as os_separator
from tkinter import CENTER, StringVar
from typing import Callable

from customtkinter import (CTk, CTkButton, CTkEntry, CTkFont,  # type: ignore
                           CTkLabel)

from fapello_downloader.app.gui.consts import (ASSETS_PATH, create_fonts,
                                               download_icon, info_icon,
                                               logo_git, logo_qs,
                                               logo_telegram, stop_icon)
from fapello_downloader.app.gui.message_box import CTkMessageBox
from fapello_downloader.consts import PACKAGE
from fapello_downloader.consts import __version__ as VERSION
from fapello_downloader.consts import app_name_color
from fapello_downloader.utils import (find_by_relative_path, opengithub,
                                      openqualityscaler, opentelegram)


class GUI:

    def __init__(self) -> None:
        """Initialize the GUI."""
        # Create the main window
        self.window: CTk = CTk()

        # Define the components
        self.selected_url = StringVar()
        self.info_message = StringVar()
        self.selected_cpu_number = StringVar()

        # Set the default values
        self.selected_url.set("Paste link here https://fapello.com/emily-rat---/")
        self.selected_cpu_number.set("6")
        self.info_message.set("Hi :)")

        # Windows properties
        self.window.title("")
        self.width = 500
        self.height = 500
        self.window.geometry("500x500")
        self.window.minsize(self.width, self.height)
        self.window.resizable(False, False)
        self.window.iconbitmap(
            find_by_relative_path(f"{ASSETS_PATH}{os_separator}logo.ico")
        )

        # Load the fonts
        self.fonts: dict[str, CTkFont] = create_fonts()

    def place_app_name(self) -> None:
        if PACKAGE:
            app_name: str = PACKAGE.replace("-", " ").replace("_", " ").title()
        else:
            app_name = "Fapello Downloader"

        app_name_label = CTkLabel(
            master=self.window,
            text=f"{PACKAGE} {VERSION}",
            text_color=app_name_color,
            font=self.fonts.get("bold20"),
            anchor="w",
        )

        app_name_label.place(relx=0.5, rely=0.1, anchor=CENTER)

    def place_link_textbox(self) -> None:
        link_textbox = self.create_text_box(self.selected_url, 150, 32)
        link_textbox.place(relx=0.5, rely=0.3, relwidth=0.85, anchor=CENTER)

    def place_simultaneous_downloads_textbox(self) -> None:
        cpu_button = self.create_info_button(
            self.open_info_simultaneous_downloads, "Simultaneous downloads"
        )
        cpu_textbox = self.create_text_box(self.selected_cpu_number, 110, 32)

        cpu_button.place(relx=0.42, rely=0.42, anchor=CENTER)
        cpu_textbox.place(relx=0.75, rely=0.42, anchor=CENTER)

    def place_tips(self) -> None:
        dns_tips_button = self.create_info_button(
            self.open_info_tips, "Tips", width=110
        )
        dns_tips_button.place(relx=0.8, rely=0.9, anchor=CENTER)

    def place_message_label(self) -> None:
        message_label = CTkLabel(
            master=self.window,
            textvariable=self.info_message,
            height=25,
            font=self.fonts.get("bold11"),
            fg_color="#ffbf00",
            text_color="#000000",
            anchor="center",
            corner_radius=25,
        )
        message_label.place(relx=0.5, rely=0.78, anchor=CENTER)

    def place_download_button(self, command: Callable) -> None:
        download_button = CTkButton(
            master=self.window,
            command=command,
            text="DOWNLOAD",
            image=download_icon,
            width=140,
            height=30,
            font=self.fonts.get("bold11"),
            border_width=1,
            fg_color="#282828",
            text_color="#E0E0E0",
            border_color="#0096FF",
        )
        download_button.place(relx=0.5, rely=0.9, anchor=CENTER)

    def place_stop_button(self, command: Callable) -> None:
        stop_button = CTkButton(
            master=self.window,
            command=command,
            text="STOP",
            image=stop_icon,
            width=140,
            height=30,
            font=self.fonts.get("bold11"),
            border_width=1,
            fg_color="#282828",
            text_color="#E0E0E0",
            border_color="#0096FF",
        )
        stop_button.place(relx=0.5, rely=0.9, anchor=CENTER)

    def place_qualityscaler_button(self) -> None:
        qualityscaler_button = CTkButton(
            master=self.window,
            image=logo_qs,
            command=openqualityscaler,
            width=30,
            height=30,
            border_width=1,
            fg_color="transparent",
            text_color="#C0C0C0",
            border_color="#404040",
            anchor="center",
            text="",
            font=self.fonts.get("bold11"),
        )
        qualityscaler_button.place(relx=0.055, rely=0.8, anchor=CENTER)

    def place_github_button(self) -> None:
        git_button = CTkButton(
            master=self.window,
            command=opengithub,
            image=logo_git,
            width=30,
            height=30,
            border_width=1,
            fg_color="transparent",
            text_color="#C0C0C0",
            border_color="#404040",
            anchor="center",
            text="",
            font=self.fonts.get("bold11"),
        )

        git_button.place(relx=0.055, rely=0.875, anchor=CENTER)

    def place_telegram_button(self) -> None:
        telegram_button = CTkButton(
            master=self.window,
            image=logo_telegram,
            command=opentelegram,
            width=30,
            height=30,
            border_width=1,
            fg_color="transparent",
            text_color="#C0C0C0",
            border_color="#404040",
            anchor="center",
            text="",
            font=self.fonts.get("bold11"),
        )
        telegram_button.place(relx=0.055, rely=0.95, anchor=CENTER)

    def create_info_button(
        self, command: Callable, text: str, width: int = 150
    ) -> CTkButton:
        return CTkButton(
            master=self.window,
            command=command,
            text=text,
            fg_color="transparent",
            hover_color="#181818",
            text_color="#C0C0C0",
            anchor="w",
            height=22,
            width=width,
            corner_radius=10,
            font=self.fonts.get("bold12"),
            image=info_icon,
        )

    def create_text_box(self, textvariable, width, heigth) -> CTkEntry:
        return CTkEntry(
            master=self.window,
            textvariable=textvariable,
            border_width=1,
            width=width,
            height=heigth,
            font=self.fonts.get("bold11"),
            justify="center",
            fg_color="#000000",
            border_color="#404040",
        )

    def show_error_message(self, exception: str) -> None:
        messageBox_title = "Download error"
        messageBox_subtitle = "Please report the error on Github or Telegram"
        messageBox_text = f" {str(exception)} "

        CTkMessageBox(
            fonts=self.fonts,
            messageType="error",
            title=messageBox_title,
            subtitle=messageBox_subtitle,
            default_value="",
            option_list=[messageBox_text],
        )

    def open_info_simultaneous_downloads(self) -> None:
        CTkMessageBox(
            fonts=self.fonts,
            messageType="info",
            title="Simultaneous downloads",
            subtitle="This widget allows to choose how many files are downloaded simultaneously",
            default_value="6",
            option_list=[],
        )

    def open_info_tips(self) -> None:
        CTkMessageBox(
            fonts=self.fonts,
            messageType="info",
            title="Tips",
            subtitle="In case of problems with reaching the website, follow these tips",
            default_value="",
            option_list=[
                " Many internet providers block access to websites such as fapello.com",
                " In this case you can use custom DNS to solve the problem, by setting them in Windows",
                " The most popular DNS are Cloudflare 1.1.1.1 or Google 8.8.8.8",
                "\n To facilitate there is a free program called DNSJumper\n"
                + "    • it can find the best custom DNS for your internet line and set them directly\n"
                + "    • it can quickly revert to the default DNS in case of problems \n"
                + "    • has also a useful function called DNS Flush that solves problems connecting to the Fapello.com \n",
            ],
        )
