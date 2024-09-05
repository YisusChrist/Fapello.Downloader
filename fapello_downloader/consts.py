"""Constants for Fapello Downloader."""

from enum import Enum

app_name = "Fapello.Downloader"
version = "3.5"

text_color = "#F0F0F0"
app_name_color = "#ffbf00"

githubme = "https://github.com/Djdefrag/Fapello.Downloader"
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
