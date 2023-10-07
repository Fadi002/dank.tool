###################################################################################

#                            https://github.com/SirDank                            

###################################################################################

import os
import sys
import json
import time
import requests
from rich.panel import Panel
from win11toast import notify
from datetime import datetime
from rich.columns import Columns
from rich.console import Console
from translatepy import Translator
from dateutil.tz import tzlocal, tzutc
from concurrent.futures import ThreadPoolExecutor
from dankware import white, white_normal, green, red, red_normal, red_dim
from dankware import align, cls, clr, title, get_duration, multithread, err, rm_line

os.chdir(os.path.dirname(__file__))

# print randomly coloured and aligned banner

def print_banner():
    
    banner = '\n   ..                                       ..                  s                                  .. \n dF                                   < .z@8"`                 :8                            x .d88"  \n\'88bu.                     u.    u.    !@88E                  .88           u.          u.    5888R   \n\'*88888bu         u      x@88k u@88c.  \'888E   u             :888ooo  ...ue888b   ...ue888b   \'888R   \n  ^"*8888N     us888u.  ^"8888""8888"   888E u@8NL         -*8888888  888R  888r  888R  888r   888R   \n beWE "888L .@88 "8888"   8888  888R    888E`"88*"           8888     888R  888>  888R  888>   888R   \n 888E  888E 9888  9888    8888  888R    888E .dN.            8888     888R  888>  888R  888>   888R   \n 888E  888E 9888  9888    8888  888R    888E~8888            8888     888R  888>  888R  888>   888R   \n 888E  888F 9888  9888    8888  888R    888E \'888&     .    .8888Lu= u8888cJ888  u8888cJ888    888R   \n.888N..888  9888  9888   "*88*" 8888"   888E  9888.  .@8c   ^%888*    "*888*P"    "*888*P"    .888B . \n `"888*""   "888*""888"    ""   \'Y"   \'"888*" 4888" \'%888"    \'Y"       \'Y"         \'Y"       ^*888%  \n    ""       ^Y"   ^Y\'                   ""    ""     ^*                                        "%    \n'    
    cls(); print(align(clr(banner,4,colours=[white, white_normal, red, red, red, red, red_normal, red_dim]) + f"\n{white}s i r {red}. {white}d a n k {red}💕"))

# handle KeyboardInterrupt

def print_warning_symbol():
    
    warning_symbol = f'\n\n{red}                      ██                      \n{red}                    ██  ██                    \n{red}                  ██      ██                  \n{red}                ██          ██                \n{red}                ██          ██                \n{red}              ██              ██              \n{red}            ██      {white}██████{red}      ██            \n{red}            ██      {white}██████{red}      ██            \n{red}          ██        {white}██████{red}        ██          \n{red}          ██        {white}██████{red}        ██          \n{red}        ██          {white}██████{red}          ██        \n{red}      ██            {white}██████{red}            ██      \n{red}      ██            {white}██████{red}            ██      \n{red}    ██              {white}██████{red}              ██    \n{red}    ██                                  ██    \n{red}  ██                {white}██████{red}                ██  \n{red}  ██                {white}██████{red}                ██  \n{red}██                  {white}██████{red}                  ██\n{red}██                                          ██\n{red}  ██████████████████████████████████████████  \n'
    cls(); print(align(warning_symbol))

# get commit date & time

def updated_on(url, dankware_module = True):

    if dankware_module: url = f"https://api.github.com/repos/SirDank/dank.tool/commits?path=__modules__/{url}.py&page=1&per_page=1"
    try:

        response = requests.get(url, headers=headers, timeout=3).json()
        if response == []: return f"[ unreleased ]"
        else:
            date, time = response[0]["commit"]["author"]["date"].split("T")
            date = date.split("-")
            time = time.replace("Z","").split(":")
            date_time_data = datetime(int(date[0]), int(date[1]), int(date[2]), int(time[0]), int(time[1]), int(time[2]), tzinfo=tzutc())
        
        return f"[bright_green]{get_duration(date_time_data, datetime.now(tzlocal()), interval='dynamic-mini')}" # 🔄
    except: return "" # [bright_red]⚠️

# multithread requests

def get_menu_request_responses(task_id, req_key):
    
    # get global runs
    
    if task_id in (0, 1):

        if task_id == 0: url = "https://dank-site.onrender.com/counter?id=dankware&hit=false"
        elif task_id == 1: url = "https://dank-site.onrender.com/counter?id=dank.tool&hit=false"
        try: menu_request_responses[req_key] = requests.get(url, headers=headers, timeout=3).content.decode().replace('<pre>','').replace('</pre>','')
        except: menu_request_responses[req_key] = f"{red}⚠️"
    
    # get motd
    
    elif task_id == 2:
        menu_request_responses[req_key] = clr(requests.get("https://raw.githubusercontent.com/SirDank/dank.tool/main/__src__/motd.txt", headers=headers, timeout=3).content.decode(), colour_one=green)

    # get chatroom user count

    elif task_id == 3:

        try:
            tmp = requests.get("https://dank-site.onrender.com/chatroom-users", headers=headers, timeout=3).content.decode()
            if tmp.isdigit() and tmp != "0": menu_request_responses[req_key] = tmp
            else: menu_request_responses[req_key] = "1"
            menu_request_responses[req_key] = f"[bright_green]{menu_request_responses[req_key]} online{' (you)' if menu_request_responses[req_key] == '1' else ''}"
        except: menu_request_responses[req_key] = "" # [bright_red]⚠️
        
    # get last update time for modules based on external repos
    
    elif task_id in (4, 5, 6):
        
        if task_id == 4: url = "https://api.github.com/repos/amd64fox/SpotX/commits?path=Install.ps1&page=1&per_page=1"
        elif task_id == 5: url = "https://api.github.com/repos/spicetify/spicetify-cli/commits?path=.&page=1&per_page=1"
        elif task_id == 6: url = "https://api.github.com/repos/massgravel/Microsoft-Activation-Scripts/commits?path=MAS/All-In-One-Version/MAS_AIO.cmd&page=1&per_page=1"
        menu_request_responses[req_key] = updated_on(url,False)
        
    # get last update time for modules
        
    elif task_id > 6:
        
        menu_request_responses[req_key] = updated_on(req_key)

# multithreaded script downloader

def download_offline_scripts(project):
    
    code = requests.get(f"https://raw.githubusercontent.com/SirDank/dank.tool/{branch}/__modules__/{project}.py", headers=headers, timeout=3).content.decode()
    open(f'__modules__/{project}.py', 'w', encoding='utf-8').write(code)

# print modules with index and get choice

def print_modules():
    
    print_banner(); print(clr(f"\n  - Modules:{stats}") + red + ('' if ONLINE_MODE else ' OFFLINE') + ('' if not OFFLINE_SRC else ' DEBUG') + ('' if not DEV_BRANCH else ' ONLINE DEBUG') + "\n")
    user_renderables = []
    console = Console()
    counter = 1
    
    for _title, module in modules.items():
        user_renderables.append(f"[b][bright_white]{counter} [bright_red]> [bright_white]{_title}[/b] {module['req_resp']}")
        counter += 1
        
    for _title in local_modules.keys():
        user_renderables.append(f"[b][bright_white]{counter} [bright_cyan]> [bright_white]{_title}[/b]")
        counter += 1

    console.print(Panel(title=f"[red1]> [bright_white][b]M O D U L E S[/b] [red1]<", title_align="center", renderable=Columns(user_renderables, expand=True), style="bright_red", expand=True))
    print()

# set globals

def set_globals_one():
    
    global ONLINE_MODE, OFFLINE_SRC, DEV_BRANCH, DANK_TOOL_VERSION, DANK_TOOL_LANG, TRANSLATOR_ENABLED, branch, headers

    OFFLINE_SRC = int(os.environ['DANK_TOOL_OFFLINE_SRC'])
    DEV_BRANCH = int(os.environ['DANK_TOOL_DEV_BRANCH'])
    DANK_TOOL_VERSION = os.environ['DANK_TOOL_VERSION']
    ONLINE_MODE = int(os.environ['DANK_TOOL_ONLINE'])
    DANK_TOOL_LANG = os.environ['DANK_TOOL_LANG']
    branch = ("main" if not DEV_BRANCH else "dev")
    headers = {"User-Agent": "dank.tool"}
    TRANSLATOR_ENABLED = (False if DANK_TOOL_LANG == "en" else True)

def set_globals_two():
    
    global offline_modules, offline_scripts, request_keys
    
    offline_modules = {

        'Fusion-Fall Modding Tool': {
            'req_resp': '',
            'title': "𝚍𝚊𝚗𝚔.𝚏𝚞𝚜𝚒𝚘𝚗-𝚏𝚊𝚕𝚕",
            'project': "dank.fusion-fall",
            'rpc': "modding fusion-fall"
        },
        
        'Browser Backup': {
            'req_resp': '',
            'title': "𝚍𝚊𝚗𝚔.𝚋𝚛𝚘𝚠𝚜𝚎𝚛-𝚋𝚊𝚌𝚔𝚞𝚙",
            'project': "dank.browser-backup",
            'rpc': "backing up a browser"
        },
        
        'Settings': {
            'req_resp': '',
            'title': "𝚍𝚊𝚗𝚔.𝚝𝚘𝚘𝚕 𝚜𝚎𝚝𝚝𝚒𝚗𝚐𝚜",
            'project': "dank.tool settings",
            'rpc': "changing dank.tool settings"
        }
    }

    offline_scripts = tuple(("dank.fusion-fall", "dank.browser-backup"))
    
    # KEEP request_keys IN ORDER!
    
    request_keys = tuple(
        (
            "dankware_runs",
            "danktool_runs",
            "motd",
            "chatroom_user_count",
            "SpotX-Win",
            "Spicetify",
            "dank.win-activate",
            "dank.minecraft-server-builder",
            "dank.minecraft-server-scanner",
            "dank.auto-clicker",
            "dank.browser-backup",
            "dank.fusion-fall"
        )
    )

def set_globals_three():
    
    global stats
    
    if ONLINE_MODE:
        
        global online_modules
        
        # global runs
            
        stats = f" [ dankware runs: {green}{menu_request_responses['dankware_runs']} | dank.tool runs: {green}{menu_request_responses['danktool_runs']} | motd: {menu_request_responses['motd']} ]"
        
        online_modules = {

            _translate('Minecraft Server Builder'): {
                'req_resp': menu_request_responses["dank.minecraft-server-builder"],
                'title': "𝚍𝚊𝚗𝚔.𝚖𝚒𝚗𝚎𝚌𝚛𝚊𝚏𝚝-𝚜𝚎𝚛𝚟𝚎𝚛-𝚋𝚞𝚒𝚕𝚍𝚎𝚛",
                'project': "dank.minecraft-server-builder",
                'rpc': "building a minecraft server"
            },

            _translate('Minecraft Server Scanner'): {
                'req_resp': menu_request_responses["dank.minecraft-server-scanner"],
                'title': "𝚍𝚊𝚗𝚔.𝚖𝚒𝚗𝚎𝚌𝚛𝚊𝚏𝚝-𝚜𝚎𝚛𝚟𝚎𝚛-𝚜𝚌𝚊𝚗𝚗𝚎𝚛",
                'project': "dank.minecraft-server-scanner",
                'rpc': "scanning for minecraft servers"
            },

            _translate('Fusion-Fall Modding Tool'): {
                'req_resp': menu_request_responses["dank.fusion-fall"],
                'title': "𝚍𝚊𝚗𝚔.𝚏𝚞𝚜𝚒𝚘𝚗-𝚏𝚊𝚕𝚕",
                'project': "dank.fusion-fall",
                'rpc': "modding fusion-fall"
            },

            _translate('SpotX + Spicetify Installer'): {
                'req_resp': (f'{menu_request_responses["Spicetify"]}, {menu_request_responses["SpotX-Win"]}' if menu_request_responses["Spicetify"] and menu_request_responses["SpotX-Win"] else ""),
                'title': "𝚍𝚊𝚗𝚔.𝚜𝚙𝚘𝚝𝚒𝚏𝚢",
                'project': "dank.spotify",
                'rpc': "installing spotx and spicetify"
            },

            _translate('Browser Backup'): {
                'req_resp': menu_request_responses["dank.browser-backup"],
                'title': "𝚍𝚊𝚗𝚔.𝚋𝚛𝚘𝚠𝚜𝚎𝚛-𝚋𝚊𝚌𝚔𝚞𝚙",
                'project': "dank.browser-backup",
                'rpc': "backing up a browser"
            },

            _translate('Windows / Office Activator'): {
                'req_resp': menu_request_responses["dank.win-activate"],
                'title': "𝚍𝚊𝚗𝚔.𝚠𝚒𝚗-𝚊𝚌𝚝𝚒𝚟𝚊𝚝𝚎",
                'project': "dank.win-activate",
                'rpc': "activating windows / office"
            },

            #'Auto Clicker [bright_red][[red1]WIP[bright_red]]': {
            #    'req_resp': menu_request_responses["dank.auto-clicker"],
            #    'title': "𝚍𝚊𝚗𝚔.𝚊𝚞𝚝𝚘-𝚌𝚕𝚒𝚌𝚔𝚎𝚛",
            #    'project': "dank.auto-clicker",
            #    'rpc': "running auto-clicker"
            #},

            'Chatroom': {
                'req_resp': menu_request_responses["chatroom_user_count"],
                'title': "𝚍𝚊𝚗𝚔.𝚌𝚑𝚊𝚝𝚛𝚘𝚘𝚖",
                'project': "dank.chatroom",
                'rpc': "chatting in the chatroom"
            },

            'Discord Server': {
                'req_resp': '[bright_green]Join Now!',
                'project': "Dankware Inc. Discord Server",
            },
            
            'Settings': {
                'req_resp': '',
                'title': "𝚍𝚊𝚗𝚔.𝚝𝚘𝚘𝚕 𝚜𝚎𝚝𝚝𝚒𝚗𝚐𝚜",
                'project': "dank.tool settings",
                'rpc': "changing dank.tool settings"
            }
        }
    
    else:

        stats = ""

# translator

def _translate(text):

    if TRANSLATOR_ENABLED and ONLINE_MODE:
        try:
            text = translator.translate(text, source_language='en', destination_language=DANK_TOOL_LANG)
        except:
            pass

    return text

if __name__ == "__main__":

    set_globals_one()
    set_globals_two()
    translator = Translator()

    # multithread requests & download offline scripts

    if ONLINE_MODE:

        if not os.path.isdir("__modules__"): os.mkdir("__modules__")
        
        print(clr(f"\n  > {_translate('Downloading scripts')}..."))

        while True:
            try:
                multithread(download_offline_scripts, 50, offline_scripts, progress_bar=False)
                break
            except:
                input(clr(f"\n  > {_translate('Failed to download scripts! Make sure you are connected to the internet! Press [ENTER] to try again')}... ",2))

        print(clr(f"\n  > {_translate('Getting request responses')}..."))
        
        global menu_request_responses
        menu_request_responses = {}

        while True:
            try:
                multithread(get_menu_request_responses, 1, tuple(_ for _ in range(len(request_keys))), request_keys, progress_bar=False)
                break
            except:
                input(clr(f"\n  > {_translate('Failed to get request responses! Make sure you are connected to the internet! Press [ENTER] to try again')}... ",2))
    
    else:
        
        del updated_on
        del download_offline_scripts
        del get_menu_request_responses

    # main

    executor = ThreadPoolExecutor(10)
    executor.submit(notify, '[ SirDank ]',
        _translate('Thank you for using my tool ❤️\nShare it with your friends!'),
        icon = {'src': f'{os.path.dirname(__file__)}\\dankware.ico', 'placement': 'appLogoOverride'} if os.path.exists(f'{os.path.dirname(__file__)}\\dankware.ico') else None,
        image = f'{os.path.dirname(__file__)}\\red.png' if os.path.exists('red.png') else None
    )

    while True:
        
        set_globals_one()
        set_globals_two()
        set_globals_three()

        title(f"𝚍𝚊𝚗𝚔.𝚝𝚘𝚘𝚕 {DANK_TOOL_VERSION}" + ("" if ONLINE_MODE else " | 𝙾𝙵𝙵𝙻𝙸𝙽𝙴")) # version defined in executor.py
        os.environ['DISCORD_RPC'] = "on the main menu"
        os.chdir(os.path.dirname(__file__))
            
        # available modules
        
        modules = (offline_modules if not ONLINE_MODE else online_modules)
        
        local_modules = {}
        
        if not os.path.isdir('__local_modules__'):
            os.mkdir('__local_modules__')

        for module in os.listdir("__local_modules__"):
            if os.path.isfile(f"__local_modules__/{module}") and module.endswith(".py"):
                name = module.replace('.py','')
                local_modules[name] = {
                    'title': name,
                    'project': name,
                    'rpc': f'running "{module}"'}

        print_modules()
        
        while True:
            
            choice = input(clr("  - Choice: ") + red)
            if choice.isdigit() and int(choice) >= 1 and int(choice) <= int(len(modules) + len(local_modules)):
                if int(choice) <= len(modules):
                    choice = modules[list(modules.keys())[int(choice) - 1]]
                    LOCAL_MODULE = False
                else:
                    choice = local_modules[list(local_modules.keys())[int(choice) - len(modules) - 1]]
                    LOCAL_MODULE = True
                break

            elif choice == 'refresh': # re-align ui
                print_modules()
            
            elif choice == 'debug': # debug menu
                cls()
                while True:
                    # this variable is long to prevent it from being changed!
                    cmd_to_be_executed = input(clr("\n  > ") + white)
                    if cmd_to_be_executed == 'exit': print_modules(); break
                    elif cmd_to_be_executed == 'env':
                        print()
                        for key, val in os.environ.items(): print(clr(key, colour_one=green, colour_two=green) + f"{white}:{green} " + clr(val, colour_one=green, colour_two=green))
                        continue
                    try: exec(cmd_to_be_executed)
                    except: print(clr("\n" + err(sys.exc_info()), 2))
            
            elif choice == 'exit':
                os.system("taskkill /f /im dank.tool.exe")
            
            else: rm_line()

        try:
            
            if "Discord" in choice['project']:
                os.system(f'start https://allmylinks.com/link/out?id=kdib4s-nu8b-1e19god'); continue

            else:
                title(choice['title'])
                project = choice['project']
                os.environ['DISCORD_RPC'] = choice['rpc']
                
            if "dank.tool settings" in choice['project']:
                
                while True:
                    
                    cls(); print(clr(f"\n  - Settings: [ {_translate('restart for changes to take effect')} ]\n"))
                    
                    settings = json.loads(open("settings.json", "r", encoding="utf-8").read())
                    update_settings = False
                    
                    if os.path.isfile("force-audio"):
                        if not int(settings["force-audio"]):
                            settings["force-audio"] = "1"
                            update_settings = True
                    else:
                        if int(settings["force-audio"]):
                            settings["force-audio"] = "0"
                            update_settings = True
                    if os.path.isfile("disable-audio"):
                        if not int(settings["disable-audio"]):
                            settings["disable-audio"] = "1"
                            update_settings = True
                    else:
                        if int(settings["disable-audio"]):
                            settings["disable-audio"] = "0"
                            update_settings = True
                    
                    if update_settings:
                        open("settings.json", "w", encoding="utf-8").write(json.dumps(settings, indent=4))
                    
                    counter = 1
                    for name, value in settings.items():
                        print(clr(f"  - [{counter}] {name}: {'True' if int(value) else 'False'}"))
                        counter += 1
                    
                    choice = input(clr("\n  - Choice [num/exit]: ") + red).lower() 
                    
                    if choice.isdigit() and int(choice) >= 1 and int(choice) <= int(len(settings)):
                        settings = list(settings.items())
                        settings[int(choice) - 1] = (settings[int(choice) - 1][0], str(int(not int(settings[int(choice) - 1][1]))))
                        settings = dict(settings)
                        
                        if int(settings["force-audio"]):
                            if not os.path.isfile("force-audio"):
                                open("force-audio", "w", encoding="utf-8").write("")
                        else:
                            if os.path.isfile("force-audio"):
                                os.remove("force-audio")
                        if int(settings["disable-audio"]):
                            if not os.path.isfile("disable-audio"):
                                open("disable-audio", "w", encoding="utf-8").write("")
                        else:
                            if os.path.isfile("disable-audio"):
                                os.remove("disable-audio")
                        
                        open("settings.json", "w", encoding="utf-8").write(json.dumps(settings, indent=4))
                    
                    elif choice == 'exit': break

                continue       
                
            if LOCAL_MODULE:
                
                # get src from local_module
                
                while True:
                    try: code = open(f'__local_modules__/{project}.py', 'r', encoding='utf-8').read(); break
                    except:
                        output = _translate(f"Failed to get code! Unable to read '__local_modules__/{project}.py'! Press [ENTER] to try again")
                        input(clr(f"\n  > {output}... ",2))
                    rm_line(); rm_line()
                
            else:

                # get src from github if not debug mode else get src locally

                if not OFFLINE_SRC and ( ONLINE_MODE or not os.path.exists(f'__modules__/{project}.py') ): # OFFLINE_DEV / ONLINE_MODE defined in executor.py
                    while True:
                        try: code = requests.get(f"https://raw.githubusercontent.com/SirDank/dank.tool/{branch}/__modules__/{project}.py", headers=headers).content.decode(); break
                        except: input(clr(f"\n  > {_translate(f'Failed to get code for {project}! Make sure you are connected to the internet! Press [ENTER] to try again')}... ",2))
                        rm_line(); rm_line()
                else:
                    while True:
                        try: code = open(f'__modules__/{project}.py', 'r', encoding='utf-8').read(); break
                        except:
                            output = _translate(f"Failed to get code! Unable to read '__modules__/{project}.py'! Press [ENTER] to try again")
                            input(clr(f"\n  > {output}... ",2))
                        rm_line(); rm_line()

            # execute src
            
            if code == "404: Not Found":
                print(clr(f"\n  > {_translate(f'{project} has not been released yet! Returning to menu in 5 seconds')}...",2)); time.sleep(5)
            else:
                cls(); exec(code)
                cls(); print(clr(f"\n  > {_translate(f'{project} executed successfully! Returning to menu in 5 seconds')}...")); time.sleep(5)

        except:

            err_message = err(sys.exc_info())
            print(clr(err_message, 2))
        
            if "Error Type: KeyboardInterrupt" in err_message:
                
                print_warning_symbol()
                print(clr(f"\n  > {_translate('Please select text first and then use [ CTRL + C ]')}!"))
                
            elif ONLINE_MODE and not LOCAL_MODULE:
                while True:
                    try: requests.post("https://dank-site.onrender.com/dank-tool-errors", headers=headers, data={"text": f"```<--- 🚨 ---> Module: {choice['title']}\n\n{err_message}```"}); break
                    except:
                        input(clr(f"\n  > {_translate('Failed to post error report! Make sure you are connected to the internet! Press [ENTER] to try again')}... ",2))
                        rm_line(); rm_line()
                print(clr(f"\n  > {_translate('Error Reported! If it is an OS error, Please run as admin and try again!')}\n\n  > {_translate('If it is a logic error, it will be fixed soon!')}"))
            
            input(clr("\n  > Press [ENTER] to return to the menu... "))
            #os.system("taskkill /f /im dank.tool.exe")
