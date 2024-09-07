"""App class for the GUI of the application."""

from multiprocessing import Process
from multiprocessing import Queue as multiprocessing_Queue
from threading import Thread
from time import sleep
from tkinter import StringVar

from fapello_downloader.app.gui.base import GUI
from fapello_downloader.consts import DownloadStatus
from fapello_downloader.requests_handler import (download_orchestrator,
                                                 get_Fapello_files_number,
                                                 read_process_status,
                                                 write_process_status)
from fapello_downloader.utils import count_files_in_directory, stop_thread


class App:

    def __init__(self) -> None:
        # Initialize the GUI
        self.gui = GUI()

        # Define the components
        self.selected_url: StringVar = self.gui.selected_url
        self.info_message: StringVar = self.gui.info_message
        self.selected_cpu_number: StringVar = self.gui.selected_cpu_number

        # Configure the window
        self.gui.window.protocol("WM_DELETE_WINDOW", self.on_app_close)

        # Place the GUI elements
        self.gui.place_app_name()
        self.gui.place_qualityscaler_button()
        self.gui.place_github_button()
        self.gui.place_telegram_button()
        self.gui.place_link_textbox()
        self.gui.place_simultaneous_downloads_textbox()
        self.gui.place_tips()
        self.gui.place_message_label()
        self.gui.place_download_button(self.download_button_command)

        self.processing_queue: multiprocessing_Queue = multiprocessing_Queue(maxsize=1)

    def on_app_close(self) -> None:
        self.gui.window.grab_release()
        self.gui.window.destroy()
        self.stop_download_process()

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

            download_type = "fapello.com"

            if not selected_link.endswith("/"):
                selected_link = selected_link + "/"

            how_many_images = get_Fapello_files_number(selected_link)

            if how_many_images == 0:
                self.info_message.set("No files found for this link")
            else:
                self.process_download = Process(
                    target=download_orchestrator,
                    args=(self.processing_queue, selected_link, cpu_number),
                )
                self.process_download.start()

                thread_wait = Thread(
                    target=self.thread_check_steps_download,
                    args=(selected_link, how_many_images),
                )
                thread_wait.start()

                self.gui.place_stop_button(self.stop_button_command)

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
                    self.gui.show_error_message(error)
                    stop_thread()

                else:
                    self.info_message.set(actual_step)

                sleep(1)
        except:
            self.gui.place_download_button(self.download_button_command)
