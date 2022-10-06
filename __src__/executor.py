# [NOTE] executor.py is meant to be executed only as an executable, not as a python script!
# the below imports are not required by the executor.py but is required by dank.tool.py

from playsound import playsound
from mcstatus import JavaServer
from win10toast import ToastNotifier
from dankware import multithread, clr_banner, align, cls, clr, magenta, white, red, reset, chdir, title, github_downloads, github_file_selector, rm_line, random_ip
#from keyboard import press
#from pynput.keyboard import Key, Listener
#from pynput.mouse import Button, Controller
#from webbrowser import open_new_tab as web

# required imports for executor.py

import os
import sys
import time
import requests
from packaging.version import parse
session = requests.Session()

# change directory to exe's location

current_version = "1.0.1"
exec_mode = "exe"
title("dank.tool [ initializing ]"); exec(chdir(exec_mode))
print(clr(f"\n  > Version: {current_version}"))

# get latest version

while True:
    try:
        latest_version = session.get("https://raw.githubusercontent.com/SirDank/dank.tool/main/__src__/executor_version.txt").content.decode()
        if "Not Found" in latest_version: latest_version = "0"
        else: break
    except: wait = input(clr("\n  > Failed to check for an update! Make sure you are connected to the Internet! Press [ENTER] to try again... ",2))

# version checker / updater: overwrites the existing executable with the latest one using the help of a batch script called 'dankware-updater.cmd' which deletes itself upon completion!

def download_latest():

    print(clr("\n  > Downloading dank.tool-latest.exe..."))
    while True:
        try: data = session.get("https://github.com/SirDank/dank.tool/blob/main/dank.tool.exe?raw=true", allow_redirects=True).content; break
        except: wait = input(clr("\n  > Failed to download! Make sure you are connected to the Internet! Press [ENTER] to try again... ",2))
    open("dank.tool-latest.exe","wb+").write(data); data = None                                                                                                                                   # removed "start dank.tool.exe"
    open("dankware-updater.cmd","w+").write("@echo off\ntitle dankware-updater\ncolor 0a\ntimeout 3\ndel /F dank.tool.exe\nren dank.tool-latest.exe dank.tool.exe\ncls\necho.\necho =======================\necho.\necho    UPDATE COMPLETE\necho.\necho =======================\necho.\necho       Close This\necho.\necho    Run dank.tool.exe\necho.\necho =======================\necho.\necho  T E R M I N A T I N G\necho.\ntimeout 20\ndel \"%~f0\" >nul 2>&1\nexit")
    print(clr("\n  > Downloaded!\n\n  > Starting in 3s..."))
    time.sleep(3); os.system(f"start dankware-updater.cmd"); toast = ToastNotifier(); toast.show_toast("dank.tool", "Please restart dank.tool.exe", duration = 10, icon_path = f"{os.path.dirname(__file__)}\\dankware.ico", threaded = True)
    sys.exit()

if parse(latest_version) > parse(current_version):
    choice = input(clr(f"\n  > Update Found: {latest_version}\n\n  > Download latest version? [ y / n ]: ") + magenta).lower()
    if choice == "y": download_latest()
elif latest_version == current_version: print(clr(f"\n  > Latest Version!"))
else: print(clr("\n  > Development Version!"))

# get main src from github

while True:
    try: code = session.get("https://raw.githubusercontent.com/SirDank/dank.tool/main/__src__/dank.tool.py").content.decode(); break
    except: wait = input(clr("\n  > Failed to get src! Make sure you are connected to the Internet! Press [ENTER] to try again... ",2))

# execute, catch errors if any

time.sleep(3); title("dank.tool"); cls()

try: exec(code)
except Exception as exp:

    cls(); exc_type, exc_obj, exc_tb = sys.exc_info()
    print(clr(f"\n  > Error: {str(exp)} | {exc_type} | Line: {exc_tb.tb_lineno}",2))
    print(clr("\n  > Please take a screenshot of this and post it on https://github.com/SirDank/dank.tool/issues/new"))
    print(clr("\n  > Opening in 3s..."))
    time.sleep(3)
    if os.name == 'nt': os.system("start https://github.com/SirDank/dank.tool/issues/new")
    else: os.system("xdg-open https://github.com/SirDank/dank.tool/issues/new")

    if not latest_version == current_version:
        choice = input(clr("\n  > Download latest version? [ y / n ]: ") + magenta).lower()
        if choice == "y": download_latest()

    wait = input(clr("\n  > Press [ENTER] to continue: "))




