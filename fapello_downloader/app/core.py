"""App class for the GUI of the application."""

from multiprocessing import Process
from multiprocessing import Queue as multiprocessing_Queue
from os import sep as os_separator
from threading import Thread
from time import sleep
from tkinter import CENTER, StringVar
from typing import Callable

from customtkinter import (CTk, CTkButton, CTkEntry, CTkFont,  # type: ignore
                           CTkLabel)

from fapello_downloader.app.actions import (open_info_simultaneous_downloads,
                                            open_info_tips, show_error_message)
from fapello_downloader.app.consts import (create_fonts, download_icon,
                                           info_icon, logo_git, logo_qs,
                                           logo_telegram, stop_icon)
from fapello_downloader.consts import (DownloadStatus, app_name,
                                       app_name_color, version)
from fapello_downloader.requests_handler import (download_orchestrator,
                                                 get_Fapello_files_number,
                                                 read_process_status,
                                                 write_process_status)
from fapello_downloader.utils import (count_files_in_directory,
                                      find_by_relative_path, opengithub,
                                      openqualityscaler, opentelegram,
                                      stop_thread)


class App:

    def __init__(self) -> None:
        window = CTk()

        self.selected_url        = StringVar()
        self.info_message        = StringVar()
        self.selected_cpu_number = StringVar()

        self.selected_url.set("Paste link here https://fapello.com/emily-rat---/")
        self.selected_cpu_number.set("6")
        self.info_message.set("Hi :)")

        # Windows properties
        window.title('')
        width        = 500
        height       = 500
        window.geometry("500x500")
        window.minsize(width, height)
        window.resizable(False, False)
        window.iconbitmap(find_by_relative_path("../Assets" + os_separator + "logo.ico"))

        window.protocol("WM_DELETE_WINDOW", self.on_app_close)

        self.processing_queue: multiprocessing_Queue = multiprocessing_Queue(maxsize=1)
        self.window: CTk = window

        self.fonts: dict[str, CTkFont] = create_fonts()

        self.place_app_name()
        self.place_qualityscaler_button()
        self.place_github_button()
        self.place_telegram_button()
        self.place_link_textbox()
        self.place_simultaneous_downloads_textbox()
        self.place_tips()
        self.place_message_label()
        self.place_download_button()

    def on_app_close(self) -> None:
        self.window.grab_release()
        self.window.destroy()
        self.stop_download_process()

    def place_app_name(self) -> None:
        app_name_label = CTkLabel(master     = self.window,
                                text       = app_name + " " + version,
                                text_color = app_name_color,
                                font       = self.fonts.get("bold20"),
                                anchor     = "w")

        app_name_label.place(relx = 0.5,
                            rely = 0.1,
                            anchor = CENTER)

    def place_link_textbox(self) -> None:
        link_textbox = self.create_text_box(self.selected_url, 150, 32)
        link_textbox.place(relx = 0.5, rely = 0.3, relwidth = 0.85, anchor = CENTER)

    def place_simultaneous_downloads_textbox(self) -> None:
        cpu_button = self.create_info_button(open_info_simultaneous_downloads, "Simultaneous downloads")
        cpu_textbox = self.create_text_box(self.selected_cpu_number, 110, 32)

        cpu_button.place(relx = 0.42, rely = 0.42, anchor = CENTER)
        cpu_textbox.place(relx = 0.75, rely = 0.42, anchor = CENTER)

    def place_tips(self) -> None:
        dns_tips_button = self.create_info_button(open_info_tips, "Tips", width = 110)
        dns_tips_button.place(relx = 0.8, rely = 0.9, anchor = CENTER)

    def place_message_label(self) -> None:
        message_label = CTkLabel(
            master  = self.window,
            textvariable = self.info_message,
            height       = 25,
            font         = self.fonts.get("bold11"),
            fg_color     = "#ffbf00",
            text_color   = "#000000",
            anchor       = "center",
            corner_radius = 25
        )
        message_label.place(relx = 0.5, rely = 0.78, anchor = CENTER)

    def place_download_button(self) -> None:
        download_button = CTkButton(
            master     = self.window,
            command    = self.download_button_command,
            text       = "DOWNLOAD",
            image      = download_icon,
            width      = 140,
            height     = 30,
            font       = self.fonts.get("bold11"),
            border_width = 1,
            fg_color     = "#282828",
            text_color   = "#E0E0E0",
            border_color = "#0096FF"
        )
        download_button.place(relx = 0.5, rely = 0.9, anchor = CENTER)

    def place_stop_button(self) -> None:
        stop_button = CTkButton(
            master     = self.window,
            command    = self.stop_button_command,
            text       = "STOP",
            image      = stop_icon,
            width      = 140,
            height     = 30,
            font       = self.fonts.get("bold11"),
            border_width = 1,
            fg_color     = "#282828",
            text_color   = "#E0E0E0",
            border_color = "#0096FF"
        )
        stop_button.place(relx = 0.5, rely = 0.9, anchor = CENTER)

    def place_qualityscaler_button(self) -> None:
        qualityscaler_button = CTkButton(
            master = self.window,
            image  = logo_qs,
            command = openqualityscaler,
            width         = 30,
            height        = 30,
            border_width  = 1,
            fg_color      = "transparent",
            text_color    = "#C0C0C0",
            border_color  = "#404040",
            anchor        = "center",
            text          = "",
            font          = self.fonts.get("bold11")
        )
        qualityscaler_button.place(relx = 0.055, rely = 0.8, anchor = CENTER)

    def download_button_command(self) -> None:
        self.info_message.set("Starting download")
        write_process_status(self.processing_queue, "Starting download")

        try:
            cpu_number = int(float(str(self.selected_cpu_number.get())))
        except:
            self.info_message.set("Cpu number must be a numeric value")
            return

        selected_link = str(self.selected_url.get()).strip()

        if selected_link == "Paste link here https://fapello.com/emily-rat---/":
            self.info_message.set("Insert a valid Fapello.com link")

        elif selected_link == "":
            self.info_message.set("Insert a valid Fapello.com link")

        elif "https://fapello.com" in selected_link:

            download_type = 'fapello.com'

            if not selected_link.endswith("/"): selected_link = selected_link + '/'

            how_many_images = get_Fapello_files_number(selected_link)

            if how_many_images == 0:
                self.info_message.set("No files found for this link")
            else:
                self.process_download = Process(
                    target = download_orchestrator,
                    args = (
                        self.processing_queue,
                        selected_link,
                        cpu_number
                        )
                    )
                self.process_download.start()

                thread_wait = Thread(
                    target = self.thread_check_steps_download,
                    args = (
                        selected_link,
                        how_many_images
                        )
                    )
                thread_wait.start()

                self.place_stop_button()

        else:
            self.info_message.set("Insert a valid Fapello.com link")

    def stop_download_process(self) -> None:
        try:
            self.process_download
        except:
            pass
        else:
            self.process_download.kill()

    def stop_button_command(self) -> None:
        self.stop_download_process()
        write_process_status(self.processing_queue, f"{DownloadStatus.STOP.value}")

    def create_info_button(
        self, command: Callable, text: str, width: int = 150
    ) -> CTkButton:
        return CTkButton(
            master  = self.window,
            command = command,
            text          = text,
            fg_color      = "transparent",
            hover_color   = "#181818",
            text_color    = "#C0C0C0",
            anchor        = "w",
            height        = 22,
            width         = width,
            corner_radius = 10,
            font          = self.fonts.get("bold12"),
            image         = info_icon
        )

    def create_text_box(self, textvariable, width, heigth) -> CTkEntry:
        return CTkEntry(
            master        = self.window,
            textvariable  = textvariable,
            border_width  = 1,
            width         = width,
            height        = heigth,
            font          = self.fonts.get("bold11"),
            justify       = "center",
            fg_color      = "#000000",
            border_color  = "#404040"
        )

    def place_github_button(self) -> None:
        git_button = CTkButton(
            master      = self.window,
            command    = opengithub,
            image      = logo_git,
            width         = 30,
            height        = 30,
            border_width  = 1,
            fg_color      = "transparent",
            text_color    = "#C0C0C0",
            border_color  = "#404040",
            anchor        = "center",
            text          = "",
            font          = self.fonts.get("bold11")
        )

        git_button.place(relx = 0.055, rely = 0.875, anchor = CENTER)

    def place_telegram_button(self) -> None:
        telegram_button = CTkButton(
            master     = self.window,
            image      = logo_telegram,
            command    = opentelegram,
            width         = 30,
            height        = 30,
            border_width  = 1,
            fg_color      = "transparent",
            text_color    = "#C0C0C0",
            border_color  = "#404040",
            anchor        = "center",
            text          = "",
            font          = self.fonts.get("bold11")
        )
        telegram_button.place(relx = 0.055, rely = 0.95, anchor = CENTER)

    def thread_check_steps_download(self, link: str, how_many_files: int) -> None:
        sleep(1)
        target_dir = link.split("/")[3]

        try:
            while True:
                actual_step = read_process_status(self.processing_queue)

                if actual_step == DownloadStatus.COMPLETED.value:
                    self.info_message.set(f"Download completed! :)")
                    stop_thread()

                elif actual_step == DownloadStatus.DOWNLOADING.value:
                    file_count = count_files_in_directory(target_dir)
                    self.info_message.set(
                        f"Downloading {str(file_count)} / {str(how_many_files)}"
                    )

                elif actual_step == DownloadStatus.STOP.value:
                    self.info_message.set(f"Download stopped")
                    stop_thread()

                elif DownloadStatus.ERROR.value in actual_step:
                    error_message = f"Error while downloading :("
                    self.info_message.set(error_message)

                    error = actual_step.replace(DownloadStatus.ERROR.value, "")
                    show_error_message(self, error)
                    stop_thread()

                else:
                    self.info_message.set(actual_step)

                sleep(1)
        except:
            self.place_download_button()
