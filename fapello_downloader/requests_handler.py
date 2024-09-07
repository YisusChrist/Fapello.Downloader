"""Requests handler module for Fapello Downloader."""

from itertools import repeat as itertools_repeat
from multiprocessing import Queue as multiprocessing_Queue
from multiprocessing.pool import ThreadPool
from os.path import join as os_path_join
from re import compile as re_compile
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup  # type: ignore
from requests import get as requests_get

from fapello_downloader.consts import DownloadStatus, headers_for_request
from fapello_downloader.utils import create_temp_dir, prepare_filename


def get_Fapello_file_url(link: str) -> tuple:
    headers = headers_for_request
    page = requests_get(link, headers=headers)

    soup = BeautifulSoup(page.content, "html.parser")
    file_element = soup.find("div", class_="flex justify-between items-center")
    try:
        if 'type="video/mp4' in str(file_element):
            file_url = file_element.find("source").get("src")
            file_type = "video"
            print(f" > Video: {file_url}")
        else:
            file_url = file_element.find("img").get("src")
            file_type = "image"
            print(f" > Image: {file_url}")

        return file_url, file_type
    except:
        return None, None


def get_Fapello_files_number(url: str) -> int:
    headers = headers_for_request
    page = requests_get(url, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")

    all_href_links = soup.find_all("a", href=re_compile(url))

    for link in all_href_links:
        link_href = link.get("href")
        link_href_stripped = link_href.rstrip("/")
        link_href_numeric = link_href_stripped.split("/")[-1]
        if link_href_numeric.isnumeric():
            print(f"> Found {link_href_numeric} files")
            return int(link_href_numeric) + 1

    return 0


def thread_download_file(link: str, target_dir: str, index: int) -> None:
    headers = headers_for_request
    link = link + str(index)
    model_name = link.split("/")[3]

    file_url, file_type = get_Fapello_file_url(link)

    if file_url != None and model_name in file_url:
        try:
            file_name = prepare_filename(file_url, index, file_type)

            request = Request(file_url, headers=headers)
            response = urlopen(request)

            file_path = os_path_join(target_dir, file_name)
            with open(file_path, "wb") as output_file:
                output_file.write(response.read())

        except:
            pass


def download_orchestrator(
    processing_queue: multiprocessing_Queue, selected_link: str, cpu_number: int
) -> None:
    target_dir = selected_link.split("/")[3]
    list_of_index = []

    write_process_status(processing_queue, DownloadStatus.DOWNLOADING.value)

    try:
        create_temp_dir(target_dir)
        how_many_files = get_Fapello_files_number(selected_link)
        list_of_index = [index for index in range(how_many_files)]

        with ThreadPool(cpu_number) as pool:
            pool.starmap(
                thread_download_file,
                zip(
                    itertools_repeat(selected_link),
                    itertools_repeat(target_dir),
                    list_of_index,
                ),
            )

        write_process_status(processing_queue, DownloadStatus.COMPLETED.value)

    except Exception as error:
        print(error)
        pass


def write_process_status(processing_queue: multiprocessing_Queue, step: str) -> None:
    while not processing_queue.empty():
        processing_queue.get()
    processing_queue.put(f"{step}")


def read_process_status(processing_queue: multiprocessing_Queue) -> str:
    actual_step = processing_queue.get()

    if actual_step == DownloadStatus.DOWNLOADING:
        write_process_status(processing_queue, DownloadStatus.DOWNLOADING.value)

    return actual_step
