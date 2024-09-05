"""Main module of the Fapello Downloader application."""

from multiprocessing import freeze_support as multiprocessing_freeze_support
from warnings import filterwarnings

from customtkinter import (set_appearance_mode,  # type: ignore
                           set_default_color_theme)

from fapello_downloader.app.core import App


def main() -> None:
    filterwarnings("ignore")
    multiprocessing_freeze_support()

    set_appearance_mode("Dark")
    set_default_color_theme("dark-blue")

    app = App()
    app.window.update()
    app.window.mainloop()


if __name__ == "__main__":
    main()
