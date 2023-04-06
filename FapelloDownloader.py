import ctypes
import fnmatch
import itertools
import multiprocessing
import os
import os.path
import platform
import shutil
import sys
import threading
import time
import tkinter as tk
import tkinter.font as tkFont
import urllib.request
import warnings
import webbrowser
from multiprocessing.pool import ThreadPool
from tkinter import PhotoImage, ttk

import cv2
import requests
import tkinterDnD
from bs4 import BeautifulSoup
from win32mica import MICAMODE, ApplyMica

import sv_ttk

warnings.filterwarnings("ignore")

global window_width
global window_height
global app_name

app_name = "Fapello.Downloader"
version  = "2.2"

# Fixed an issue for some Fapello models that did not allow downloading all files 
# Bugfixes and improvements
# Updated dependencies

default_font          = 'Segoe UI'
background_color      = "#181818"
window_width          = 600
window_height         = 650
text_color            = "#F0F0F0"
cpu_number            = 4
windows_subversion    = int(platform.version().split('.')[2])
 
githubme              = "https://github.com/Djdefrag/Fapello.Downloader"
itchme                = "https://jangystudio.itch.io/fapellodownloader"

ctypes.windll.shcore.SetProcessDpiAwareness(True)
scaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100
font_scale = round(1/scaleFactor, 1)


# ---------------------- Functions ----------------------

# ---------------------- Utils ----------------------


def openitch():
    webbrowser.open(itchme, new=1)

def opengithub():
    webbrowser.open(githubme, new=1)

def find_by_relative_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(
        os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

def write_in_log_file(text_to_insert):
    log_file_name = app_name + ".log"
    with open(log_file_name,'w') as log_file: 
        os.chmod(log_file_name, 0o777)
        log_file.write(text_to_insert) 
    log_file.close()

def read_log_file():
    log_file_name = app_name + ".log"
    with open(log_file_name,'r') as log_file: 
        os.chmod(log_file_name, 0o777)
        step = log_file.readline()
    log_file.close()
    return step

def create_temp_dir(name_dir):
    if os.path.exists(name_dir): shutil.rmtree(name_dir)
    if not os.path.exists(name_dir): os.makedirs(name_dir, mode=0o777)

def get_actual_path():
    path = find_by_relative_path("logo.png").replace("logo.png", "")
    return path

def prepare_filename(file_url, index, file_type):
    first_part_filename = str(file_url).split("/")[-3]

    if file_type == "image":
        extension = ".png"
    elif file_type == "video":
        extension = ".mp4"
    filename = first_part_filename + "_" + str(index) + extension

    return filename

def find_between(s, start, end):
    return (s.split(start))[1].split(end)[0]
    
def get_file_url(link):
    page = requests.get(link)
    soup = BeautifulSoup(page.content, "html.parser")
    file_url = str(soup.find("div", class_="flex justify-between items-center"))

    if 'type="video/mp4' in str(file_url): 
        # Video
        file_url  = str(file_url).split("src=")[1].split("type=")[0].replace('"', "")
        file_type = "video"
        print('> video: ' + file_url)
    else: 
        # Photo
        file_url  = file_url.split("src=")[1].split(".jpg")[0].replace('"', '') + '.jpg'
        file_type = "image"
        print('> image: ' + file_url)

    return file_url, file_type

def get_number_of_images(link):
    page = requests.get(link)
    soup = BeautifulSoup(page.content, "html.parser")
    print(soup)
    media_number = soup.find_all("div", class_="flex lg:flex-row flex-col")
    media_number = str(media_number).split(">")[1].split("<")[0]
    return media_number


# ---------------------- /Utils ----------------------

# ---------------------- Core ----------------------


def crop_border(input_img):
    image = cv2.imread(input_img)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 255, 255, cv2.THRESH_TRIANGLE)[1]

    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted(contours, key=cv2.contourArea, reverse=True)
    cnt = cnts[0]
    x,y,w,h = cv2.boundingRect(cnt)
    crop = image[y:y+h,x:x+w]

    cv2.imwrite(input_img, img = crop)

def process_start_download( link, cpu_number):
    actual_dir    = get_actual_path()
    dir_name      = link.split("/")[3]
    target_dir    = actual_dir + os.sep + dir_name

    write_in_log_file('Preparing...')
    
    try:
        create_temp_dir(target_dir)

        how_many_images = int(get_number_of_images(link))  
        how_many_images = round(how_many_images * 5)

        list_of_index = []
        for index in range(how_many_images): list_of_index.append(index)

        write_in_log_file("Downloading...")

        with ThreadPool(cpu_number) as pool:
            pool.starmap(thread_download_file, 
                         zip(itertools.repeat(link),
                         list_of_index,
                         itertools.repeat(target_dir)))
            
        write_in_log_file("Completed")
        import tkinter as tk
        tk.messagebox.showinfo(title   = 'Completed', 
                               message = 'Files saved in: \n' + 
                                         target_dir + '\n')

    except Exception as e:
        write_in_log_file('Error while downloading' + '\n\n' + str(e)) 
        import tkinter as tk
        tk.messagebox.showerror(title   = 'Error', 
                                message = 'Download failed caused by:\n\n' +
                                           str(e) + '\n\n' +
                                          'Please report the error on Github.com or Itch.io.' +
                                          '\n\nThank you :)')

def thread_download_file(link, index, target_dir):
    link = link + str(index)       
    model_name = link.split('/')[3]
    try:
        file_url, file_type = get_file_url(link)
        
        if model_name in file_url:
            file_name = prepare_filename(file_url, index, file_type)

            if file_type == "image":
                download_image(file_url, file_name, target_dir)
                x = 1 + "x"
            elif file_type == "video":
                download_video(file_url, file_name, target_dir)
                x = 1 + "x"
    except:
        pass




def download_image(file_url, file_name, target_dir):
    if file_url != '' and target_dir.split(str(os.sep))[-1] in file_url:
        opener = urllib.request.build_opener()
        opener.addheaders = [
                                (
                                "User-Agent",
                                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
                                )
                            ]                   
        urllib.request.install_opener(opener)

        urllib.request.urlretrieve(file_url, target_dir + os.sep + file_name)

def download_video(file_url, file_name, target_dir):
    if file_url != '' and target_dir.split(str(os.sep))[-1] in file_url:
        opener = urllib.request.build_opener()
        opener.addheaders = [
                                (
                                "User-Agent",
                                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
                                )
                            ]                   
        urllib.request.install_opener(opener)

        urllib.request.urlretrieve(file_url, target_dir + os.sep + file_name)

def thread_check_steps_download( link, how_many_files ):
    time.sleep(2)

    actual_dir    = get_actual_path()
    dir_name      = link.split("/")[3]
    target_dir    = actual_dir + os.sep + dir_name

    try:
        while True:
            step = read_log_file()
            if "Completed" in step or "Error" in step or "Stopped" in step:
                info_string.set(step)
                stop = 1 + "x"
            elif "Downloading" in step:
                count = len(fnmatch.filter(os.listdir(target_dir), '*.*'))
                info_string.set("Downloading " + str(count) + "/" + str(how_many_files))
            else:
                info_string.set(step)

            time.sleep(2)
    except:
        place_download_button()


# ---------------------- /Core ----------------------

# ---------------------- GUI related ----------------------


def download_button_command():
    global process_download
    global cpu_number

    info_string.set("Checking link")

    try:
        cpu_number = int(float(str(selected_cpu_number.get()))) * 2
    except:
        info_string.set("Cpu number must be a numeric value")
        return

    selected_link = str(selected_url.get())
    if selected_link == "paste link ( https://fapello.com/emily-rat---/ )":
        info_string.set("Please, insert a valid Fapello link")
    elif selected_link == "":
        info_string.set("Please, insert a valid Fapello link")
    else:
        info_string.set("Starting download")

        how_much_images = int(get_number_of_images(selected_link))  
        how_much_images = round(how_much_images)

        place_stop_button()
        
        process_download = multiprocessing.Process(target = process_start_download,
                                                   args   = (selected_link, cpu_number))
        process_download.start()

        thread_wait = threading.Thread( target = thread_check_steps_download,
                                        args   = (selected_link, how_much_images), 
                                        daemon = True)
        thread_wait.start()



def place_cpu_number_spinbox():
    cpu_number_container = ttk.Notebook(root)
    cpu_number_container.place(x = window_width - 285 - 30, 
                    y = 220, 
                    width  = 285,
                    height = 65)

    global spinbox_cpu_number
    spinbox_cpu_number = ttk.Spinbox(root,  
                                        from_     = 1, 
                                        to        = 100, 
                                        increment = 1,
                                        textvariable = selected_cpu_number, 
                                        justify      = 'center',
                                        foreground   = text_color,
                                        takefocus    = False,
                                        font         = bold12)
    spinbox_cpu_number.place( x = window_width - 130 - 43, 
                                y = 232, 
                                width  = 130, 
                                height = 38 )
    spinbox_cpu_number.insert(0, cpu_number)

    cpu_selection_title = ttk.Label(root, background = "", 
                                    font = bold11, 
                                     foreground = text_color, 
                                     justify = 'right', 
                                     relief = 'flat', text = " Cpu number ")
    cpu_selection_title.place(x = window_width - 127 - 173,
                                y = 232,
                                width  = 127,
                                height = 40)



def place_itch_button():
    global logo_itch
    horizontal_center = window_width/2

    logo_itch = PhotoImage(file = find_by_relative_path( "Assets" + os.sep + "itch_logo.png"))

    version_button = ttk.Button(root,
                               image = logo_itch,
                               padding = '0 0 0 0',
                               text    = " " + version,
                               compound = 'left',
                               style    = 'Bold.TButton')
    version_button.place(x = horizontal_center - 125/2,
                        y = 90,
                        width  = 125,
                        height = 35)
    version_button["command"] = lambda: openitch()

def stop_button_command():
    global process_download
    process_download.terminate()
    process_download.kill()
    
    write_in_log_file("Stopped") 

def place_github_button():
    global logo_git
    horizontal_center = window_width/2
    logo_git = PhotoImage(file = find_by_relative_path("Assets" 
                                                        + os.sep 
                                                        + "github_logo.png"))

    github_button = ttk.Button(root,
                               image = logo_git,
                               padding = '0 0 0 0',
                               text    = ' Github',
                               compound = 'left',
                               style    = 'Bold.TButton')
    github_button.place(x = horizontal_center + 10,
                        y = 90,
                        width  = 110,
                        height = 35)
    github_button["command"] = lambda: opengithub()

def place_app_title():
    horizontal_center = window_width/2

    Title = ttk.Label(root, 
                      font = (default_font, round(17 * font_scale), "bold"),
                      foreground = "#ffbf00",
                      background = background_color, 
                      anchor     = 'center', 
                      text       = app_name)
    Title.place(x = horizontal_center - 270/2,
                y = 22,
                width  = 270,
                height = 55)

def place_background():
    global Background
    Background = ttk.Label(root, background = background_color, relief = 'flat')
    Background.place(x = 0, 
                     y = 0, 
                     width  = window_width,
                     height = window_height)

def place_entrybox_widget():
    global Entry_box_url
    Entry_box_url = ttk.Entry(root, 
                            textvariable = selected_url, 
                            justify      = 'center',
                            foreground   = text_color,
                            takefocus    = False,
                            font         = normal13)
    Entry_box_url.place(x = window_width/2 - (window_width * 0.83)/2, 
                        y = 150, 
                        width  = window_width * 0.83, 
                        height = 45)
    Entry_box_url.insert(0, 'paste link ( https://fapello.com/emily-rat---/ )')

def place_message_box():
    info_string.set("...")
    Message = ttk.Label(root,
                        font = (default_font, round(11 * font_scale), "bold"),
                        textvar    = info_string,
                        relief     = "flat",
                        justify    = "center",
                        foreground = "#ffbf00",
                        anchor     = "center",
                        background = background_color)
    Message.place(x = window_width/2 - (window_width * 0.9)/2,
                        y = window_height - 145,
                        width  = window_width * 0.9,
                        height = 30)

def place_download_button(): 
    global download_icon

    download_icon = tk.PhotoImage(file = find_by_relative_path("Assets" 
                                                            + os.sep 
                                                            + "download_icon.png"))

    Download_button = ttk.Button(root, 
                                image = download_icon,
                                text  = '  DOWNLOAD ',
                                compound = tk.LEFT,
                                style    = 'Bold.TButton')

    Download_button.place(x     = window_width/2 - (window_width * 0.45)/2 ,  
                         y      = window_height - 100,
                         width  = window_width * 0.45,
                         height = 45)
    Download_button["command"] = lambda: download_button_command()

def place_stop_button(): 
    global stop_icon
    stop_icon = tk.PhotoImage(file = find_by_relative_path("Assets" 
                                                            + os.sep 
                                                            + "stop_icon.png"))

    Stop_button = ttk.Button(root, 
                            image = stop_icon,
                            text  = '  STOP DOWNLOAD ',
                            compound = tk.LEFT,
                            style    = 'Bold.TButton')

    Stop_button.place(x     = window_width/2 - (window_width * 0.45)/2 ,  
                         y      = window_height - 100,
                         width  = window_width * 0.45,
                         height = 45)
    Stop_button["command"] = lambda: stop_button_command()


# ---------------------- /GUI related ----------------------

# ---------------------- /Functions ----------------------


def apply_windows_dark_bar(window_root):
    window_root.update()
    DWMWA_USE_IMMERSIVE_DARK_MODE = 20
    set_window_attribute          = ctypes.windll.dwmapi.DwmSetWindowAttribute
    get_parent                    = ctypes.windll.user32.GetParent
    hwnd                          = get_parent(window_root.winfo_id())
    rendering_policy              = DWMWA_USE_IMMERSIVE_DARK_MODE
    value                         = 2
    value                         = ctypes.c_int(value)
    set_window_attribute(hwnd, rendering_policy, ctypes.byref(value), ctypes.sizeof(value))    

    #Changes the window size
    window_root.geometry(str(window_root.winfo_width()+1) + "x" + str(window_root.winfo_height()+1))
    #Returns to original size
    window_root.geometry(str(window_root.winfo_width()-1) + "x" + str(window_root.winfo_height()-1))

def apply_windows_transparency_effect(window_root):
    window_root.wm_attributes("-transparent", background_color)
    hwnd = ctypes.windll.user32.GetParent(window_root.winfo_id())
    ApplyMica(hwnd, MICAMODE.DARK)

class App:
    def __init__(self, root):
        sv_ttk.use_dark_theme()

        Upsc_Butt_Style = ttk.Style()
        Upsc_Butt_Style.configure("Bold.TButton", font = bold11)

        root.title('')
        width        = window_width
        height       = window_height
        screenwidth  = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr     = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        root.iconphoto(False, PhotoImage(file = find_by_relative_path("Assets" 
                                                                    + os.sep 
                                                                    + "logo.png")))

        if windows_subversion >= 22000: # Windows 11
            apply_windows_transparency_effect(root)
        apply_windows_dark_bar(root)

        place_background()
        place_app_title()
        place_itch_button()

        place_entrybox_widget()
        place_cpu_number_spinbox()
        place_message_box()             
        place_download_button()

if __name__ == "__main__":
    multiprocessing.freeze_support()
    
    root = tkinterDnD.Tk()
    selected_url        = tk.StringVar()
    info_string         = tk.StringVar()
    selected_cpu_number = tk.StringVar()

    normal12 = tkFont.Font(family = default_font, size   = round(12 * font_scale), weight = 'normal')
    normal13 = tkFont.Font(family = default_font, size   = round(13 * font_scale), weight = 'normal')

    bold10 = tkFont.Font(family = default_font, size   = round(10 * font_scale), weight = 'bold')
    bold11 = tkFont.Font(family = default_font, size   = round(11 * font_scale), weight = 'bold')
    bold12 = tkFont.Font(family = default_font, size   = round(12 * font_scale), weight = 'bold')
    bold13 = tkFont.Font(family = default_font, size   = round(13 * font_scale), weight = 'bold')
    bold14 = tkFont.Font(family = default_font, size   = round(14 * font_scale), weight = 'bold')
    bold15 = tkFont.Font(family = default_font, size   = round(15 * font_scale), weight = 'bold')
    bold20 = tkFont.Font(family = default_font, size   = round(20 * font_scale), weight = 'bold')
    bold21 = tkFont.Font(family = default_font, size   = round(21 * font_scale), weight = 'bold')

    app = App(root)
    root.update()
    root.mainloop()
    

