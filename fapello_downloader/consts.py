"""Constants for Fapello Downloader."""

from enum import Enum

try:
    from importlib import metadata
except ImportError:  # for Python < 3.8
    import importlib_metadata as metadata  # type: ignore

__version__: str = metadata.version(__package__ or __name__)
__desc__: str = metadata.metadata(__package__ or __name__)["Summary"]
GITHUB: str = metadata.metadata(__package__ or __name__)["Home-page"]
PACKAGE: str | None = __package__

text_color = "#F0F0F0"
app_name_color = "#ffbf00"

telegramme = "https://linktr.ee/j3ngystudio"
qs_link = "https://github.com/Djdefrag/QualityScaler"

headers_for_request = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.3"
}


class DownloadStatus(Enum):
    COMPLETED = "Completed"
    DOWNLOADING = "Downloading"
    ERROR = "Error"
    STOP = "Stop"
