import os
import time
import socket
import requests
from random import randint
from numpy.random import choice
from translatepy import Translator
from concurrent.futures import ThreadPoolExecutor
from mcstatus import JavaServer, BedrockServer
from dankware import red, red_dim
from dankware import multithread, clr, cls, align, rm_line, random_ip, get_path

'''

for the future of this script

Goals: masscan port scans

https://github.com/MyKings/python-masscan
https://github.com/Arryboom/MasscanForWindows
https://github.com/rezonmain/mc-server-scanner/blob/main/src/iprange.py
https://github.com/ObscenityIB/creeper/blob/main/creeper.sh
https://raw.githubusercontent.com/robertdavidgraham/masscan/master/data/exclude.conf
https://github.com/Footsiefat/Minecraft-Server-Scanner

'''

def translate(text):
    if DANK_TOOL_LANG:
        try: text = translator.translate(text, DANK_TOOL_LANG, 'en').result
        except: pass
    return text

# checks if ip has a server running on the specified port

def check_java(ip):
    if socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect_ex((ip,port)) == 0:
        server = JavaServer(ip,port)
        check(ip, server)

def check_bedrock(ip):
    try:
        socket.socket(socket.AF_INET, socket.SOCK_DGRAM).sendto(b'\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\x00\xfe\xfe\xfe\xfe\xfd\xfd\xfd\xfd\x124Vx\x00\x00\x00\x00\x00\x00\x00\x00', (ip, port))
        server = BedrockServer(ip,port)
        check(ip, server)
    except: pass

def save():
    tmp = []
    while running: # pylint: disable=used-before-assignment
        while to_save: # pylint: disable=used-before-assignment
            tmp.append(to_save.pop())
        if tmp:
            with open('servers.txt','a',encoding='utf-8') as _:
                _.write('\n'.join(tmp)+'\n')
            tmp.clear()
        time.sleep(5)

def check(ip, server):

    try:
        status = server.status()
        saved[ip] = None
        #try: query_response = f"{server.query().software}"
        #except: query_response = ""

        try:
            response = requests.get(f"http://ipwho.is/{ip}", timeout=3).json()
            if response['success']:
                server_info = f"{response['city']} | {response['connection']['org']} | {response['connection']['domain']}"
            else:
                server_info = "ratelimited on ipwho.is" # 50mil monthly limit
        except: server_info = "ipwho.is is unreachable"

        # for https://dashboard.render.com/minecraft-java-servers
        # for https://dashboard.render.com/minecraft-bedrock-servers
        try:
            json = {'server_ip': ip, 'city': '', 'org': '', 'domain': ''}
            if response['success']:
                json['city'] = response['city']
                json['org'] = response['connection']['org']
                json['domain'] = response['connection']['domain']
            executor.submit(requests.post, f"https://dank-site.onrender.com/minecraft-{server_type}-servers", headers={"User-Agent": "dank.tool"}, json=json) # pylint: disable=used-before-assignment
        except: pass

        if server_type == "java":
            to_print = f"{ip} | java | {status.version.name} | {status.players.online}/{status.players.max} online | {int(status.latency)}ms | {server_info} | {status.description}".replace('\n',' ').replace('ü','u')
        else:
            to_print = f"{ip} | bedrock | {status.version.name} | {status.gamemode} | Map: {status.map_name} | {status.players.online}/{status.players.max} online | {int(status.latency)}ms | {server_info} | {status.motd.raw}".replace('\n',' ')

        for _ in ('§0', '§1', '§2', '§3', '§4', '§5', '§6', '§7', '§8', '§9', '§a', '§b', '§c', '§d', '§e', '§f', '§l', '§n', '§o', '§m', '§k', '§r'):
            to_print = to_print.replace(_,'')
        print(clr(f"  - {to_print}\n"))
        to_save.append(to_print)

    except:
        pass

# generates random valid ip

def generate_ip():
    while True:
        ip = random_ip()
        if ip in ips or ip in saved: continue
        ips[ip] = ""; break

def generate_ip_targetted():
    while True:
        ip = choice(target_ips, p=target_weights) + f".{randint(0,255)}.{randint(0,255)}" # pylint: disable=used-before-assignment
        if ip in ips or ip in saved: continue
        ips[ip] = ""; break

def main():

    global ips, server_type, port, saved, translator, DANK_TOOL_LANG

    # check if translator is enabled (dank.tool.exe)

    try:
        DANK_TOOL_LANG = os.environ['DANK_TOOL_LANG']
        if DANK_TOOL_LANG == 'en':
            DANK_TOOL_LANG = ''
        else:
            translator = Translator()
    except:
        DANK_TOOL_LANG = ''

    # get user input

    banner = '\n\n     _             _                                                              \n    | |           | |                                                             \n  _ | | ____ ____ | |  _   ____   ____ ___ ___  ____ ____ ____  ____   ____  ____ \n / || |/ _  |  _ \\| | / ) |    \\ / ___|___)___)/ ___) _  |  _ \\|  _ \\ / _  )/ ___)\n( (_| ( ( | | | | | |< ( _| | | ( (___   |___ ( (__( ( | | | | | | | ( (/ /| |    \n \\____|\\_||_|_| |_|_| \\_|_)_|_|_|\\____)  (___/ \\____)_||_|_| |_|_| |_|\\____)_|    \n\n'
    cls(); print(align(clr(banner,4,colours=(red, red_dim))))
    print(clr(f"\n  - Java Server List: https://dank-site.onrender.com/minecraft-java-servers\n\n  - Bedrock Server List: https://dank-site.onrender.com/minecraft-bedrock-servers\n\n  - {translate('You can use the above links to get a list of servers that have been found by the users of this tool')}!"))
    match input(clr("\n  - 1: Open Java Server List | 2: Open Bedrock Server List | ENTER: Skip\n\n  > Choice [1/2/ENTER]: ") + red):
        case "1": os.system("start https://dank-site.onrender.com/minecraft-java-servers")
        case "2": os.system("start https://dank-site.onrender.com/minecraft-bedrock-servers")

    cls(); print(align(clr(banner,4,colours=(red, red_dim))))
    print(clr(f"\n  - {translate('Start with 100 threads and note the performance impact')}.\n\n  - {translate('Generally should be smooth upto 500 threads, you might notice some performance impact above this value')}!\n\n  - {translate('Test it for the first time with 50000 IPs, it will take a few seconds to generate')}."))

    print("")
    while True:
        server_type = input(clr("  > Server Type [java/bedrock]: ") + red).lower()
        match server_type:
            case "java":
                port = 25565
                break
            case "bedrock":
                port = 19132
                break
        rm_line()

    print("")
    while True:
        threads = input(clr("  > Threads: ") + red)
        if threads.isdigit() and int(threads) > 0: threads = int(threads); break
        rm_line()

    print("")
    while True:
        ips_amt = input(clr("  > Amount of IPs to scan: ") + red)
        if ips_amt.isdigit() and int(ips_amt) > 0: ips_amt = int(ips_amt); break
        rm_line()

    if server_type == "java":
        cls(); print(align(clr(banner,4,colours=(red, red_dim))))
        print(clr(f"\n  - [0] {translate('Default Scan: Generates completely random IPs, good chance to find private / locally hosted servers, low find-rate')}.\n\n  - [1] {translate('Targetted Scan: Generates random IPs based on custom rules, good chance to find data center servers, high find-rate')}."))

        print("")
        while True:
            targetted_scan = input(clr("  > Scan Type [0/1]: ") + red)
            if targetted_scan in ('0', '1'): targetted_scan = int(targetted_scan); break
            rm_line()
    else:
        targetted_scan = 0

    # disclaimer

    cls(); input(clr(f"\n  [IMPORTANT]\n\n  - {translate('Do not use [ Ctrl + C ] without selecting text first')}!\n\n  - {translate('All the servers are saved to servers.txt')}!\n\n  - {translate('Be responsible! Do not use the scanner for the wrong reasons')}!\n\n  > {translate('Press [ ENTER ] to start the multithreaded scanner')}... "))
    cls()

    # change directory

    try: os.chdir(get_path('Documents'))
    except: os.chdir("C:\\")
    try: os.mkdir('dank.mc-server-scanner')
    except FileExistsError: pass
    os.system('explorer.exe "dank.mc-server-scanner"')
    os.chdir('dank.mc-server-scanner')

    if not os.path.isfile('scan_count_java.txt'):
        with open('scan_count.txt','w',encoding='utf-8') as _:
            _.write('0')
    if not os.path.isfile('scan_count_bedrock.txt'):
        with open('scan_count.txt','w',encoding='utf-8') as _:
            _.write('0')
    if not os.path.isfile('servers.txt'):
        with open('servers.txt','x',encoding='utf-8') as _:
            _.close()
        saved = {}
    else:
        saved = {}
        with open('servers.txt','r',encoding='utf-8') as _:
            for __ in _.read().splitlines():
                try: saved[__.split(' | ',1)[0]] = None
                except: pass

    # remove old files

    for _ in ('scanned.txt', 'java_scanned.txt', 'java_scanned.json', 'bedrock_scanned.txt', 'bedrock_scanned.json', 'java_scanned_ips.db', 'bedrock_scanned_ips.db'):
        if os.path.isfile(_): os.remove(_)

    # generate and check ips on multiple threads in batches

    gen_rate = 1000 # threads to generate at | higher = faster
    gen_amt = 50000 # max generate / check amount
    gen_rem = ips_amt
    while gen_rem > 0:

        ips = {}
        generated = 0
        if gen_rem < gen_amt:
            gen_amt = gen_rem

        # multithreaded generator

        #cls()
        print(clr(f"\n  - Generating {gen_amt} unique ips..."))
        while generated < gen_amt:
            while True:
                try:
                    if gen_amt >= gen_rate:
                        multithread((generate_ip_targetted if targetted_scan else generate_ip), gen_rate, progress_bar=False)
                        generated += gen_rate
                    else:
                        multithread((generate_ip_targetted if targetted_scan else generate_ip), gen_amt, progress_bar=False)
                        generated += gen_amt
                    break
                except: input(clr(f"\n  > {translate('Failed to generate ips! Do not use [ Ctrl + C ]! Press [ENTER] to try again')}... ",2)); rm_line()

        # multithreaded checker

        while True:
            try:
                print(clr(f"\n  - Checking {len(ips)} unique ips...\n"))
                if server_type == "java": multithread(check_java, threads, tuple(ips.keys())); break
                if server_type == "bedrock": multithread(check_bedrock, threads, tuple(ips.keys())); break
            except: input(clr(f"\n  > {translate('Failed to check ips! Do not use [ Ctrl + C ]! Press [ENTER] to try again')}... ",2)); rm_line()

        # saving scanned ips

        try:
            with open(f'scan_count_{server_type}.txt','r',encoding='utf-8') as _:
                scan_count = int(_.read())
        except: scan_count = 0
        scan_count += len(ips)
        with open(f'scan_count_{server_type}.txt','w',encoding='utf-8') as _:
            _.write(str(scan_count))
        print(clr(f"\n  - Totally Scanned {scan_count} IPs!"))
        time.sleep(5)

        gen_rem -= gen_amt

        if gen_rem > 0:
            print(clr(f"\n  - {gen_rem} IPs remaining..."))

if __name__ == "__main__": 

    to_save = []
    running = True
    target_ips = tuple(['1.14', '100.36', '101.35', '103.123', '104.243', '106.52', '108.31', '109.173', '109.250', '116.204', '121.127', '121.40', '123.249', '124.70', '133.125', '139.144', '140.83', '146.19', '147.189', '149.18', '152.136', '153.127', '158.174', '159.223', '161.35', '163.172', '164.70', '172.218', '173.207', '173.48', '174.52', '175.24', '176.31', '185.156', '185.216', '185.244', '188.193', '193.111', '193.22', '198.12', '198.46', '203.129', '204.111', '206.189', '213.239', '222.187', '36.227', '45.136', '45.58', '45.76', '45.89', '46.38', '46.59', '47.113', '47.160', '49.232', '5.252', '5.39', '50.39', '51.91', '61.245', '64.227', '65.110', '66.94', '69.164', '71.227', '73.217', '77.174', '78.108', '79.143', '81.25', '81.68', '83.147', '85.31', '87.106', '87.107', '87.237', '88.159', '88.214', '89.117', '91.66', '95.154', '96.227', '97.102', '98.38', '101.34', '106.55', '107.174', '129.158', '143.42', '155.4', '158.160', '170.205', '172.104', '172.255', '172.96', '184.144', '185.185', '185.208', '185.233', '193.31', '194.113', '194.36', '209.236', '212.102', '213.32', '216.39', '37.157', '37.221', '45.137', '45.138', '45.141', '45.147', '45.150', '45.59', '45.82', '46.174', '47.144', '47.186', '5.182', '5.188', '5.196', '5.42', '51.159', '51.178', '57.128', '62.210', '66.11', '79.137', '81.167', '82.157', '85.10', '87.98', '91.107', '91.218', '92.221', '92.42', '94.142', '95.111', '98.128', '101.42', '104.129', '111.229', '12.156', '129.80', '131.186', '133.242', '138.197', '144.126', '144.21', '146.56', '152.89', '153.126', '154.12', '154.49', '158.180', '165.22', '172.245', '185.223', '185.57', '192.210', '193.43', '194.156', '194.97', '207.180', '34.116', '34.125', '34.22', '34.81', '45.61', '45.85', '45.88', '45.90', '45.93', '47.157', '75.119', '77.68', '81.70', '85.114', '85.202', '89.187', '93.186', '94.110', '94.23', '104.128', '104.168', '114.132', '128.140', '145.239', '154.56', '175.178', '185.73', '188.68', '207.211', '217.160', '37.59', '45.79', '49.212', '5.135', '5.189', '83.223', '95.165', '107.173', '115.236', '116.203', '137.74', '138.3', '143.244', '151.80', '173.212', '173.233', '173.76', '178.33', '185.199', '188.40', '194.147', '195.90', '211.101', '37.120', '43.248', '5.75', '65.21', '66.242', '8.130', '101.67', '119.91', '138.199', '141.94', '163.5', '168.119', '192.18', '193.70', '194.195', '204.216', '207.127', '23.139', '23.88', '31.220', '37.114', '38.103', '43.139', '45.131', '62.171', '89.35', '103.195', '104.194', '104.247', '124.221', '160.16', '172.65', '180.150', '185.249', '192.9', '198.27', '45.159', '46.105', '51.210', '51.68', '78.47', '82.64', '88.198', '12.217', '148.113', '150.158', '176.9', '212.11', '42.186', '51.254', '51.255', '54.38', '94.16', '95.217', '109.169', '129.159', '141.144', '159.196', '164.68', '167.235', '185.135', '193.123', '194.163', '194.233', '217.182', '23.109', '23.95', '5.181', '5.62', '78.46', '82.65', '85.215', '89.116', '95.216', '104.238', '124.222', '124.223', '144.91', '162.19', '172.105', '192.3', '23.145', '51.75', '65.109', '82.66', '12.132', '148.251', '152.228', '174.136', '178.32', '185.137', '192.95', '209.54', '212.227', '43.138', '43.143', '45.154', '5.161', '51.83', '69.12', '74.91', '82.165', '85.14', '141.148', '142.132', '149.202', '152.69', '162.222', '162.55', '178.63', '192.161', '192.227', '204.152', '204.44', '46.4', '49.12', '5.9', '54.36', '62.72', '88.150', '129.152', '159.69', '178.254', '188.165', '37.187', '65.108', '81.31', '88.99', '164.132', '191.101', '193.122', '198.50', '217.145', '38.242', '54.37', '89.163', '134.255', '155.248', '157.90', '161.97', '5.83', '69.174', '104.224', '167.86', '173.44', '195.201', '198.23', '198.244', '23.156', '38.133', '45.132', '51.77', '66.70', '82.180', '129.153', '133.18', '43.251', '51.38', '133.130', '142.44', '144.76', '15.235', '163.44', '164.152', '116.202', '132.226', '138.2', '45.139', '45.81', '62.104', '91.121', '138.201', '144.22', '172.240', '94.130', '34.64', '101.43', '135.181', '146.59', '209.192', '54.39', '66.118', '144.24', '202.61', '66.59', '104.234', '141.145', '150.230', '152.67', '173.205', '81.169', '143.47', '168.138', '89.58', '152.70', '135.125', '141.95', '158.101', '23.94', '130.162', '192.99', '149.56', '149.88', '158.69', '144.217', '208.52', '63.135', '198.55', '140.238', '167.114', '129.213', '139.99', '141.147', '173.237', '161.129', '37.10', '129.146', '185.236', '51.89', '155.94', '85.214', '132.145', '150.136', '51.79', '51.222', '51.195', '31.214', '169.150', '104.223', '157.7', '51.161', '118.27', '15.204', '129.151', '85.190', '94.250', '162.43', '158.62', '66.248', '147.135', '173.240', '130.61', '176.57', '135.148', '50.20', '162.33', '51.81', '160.251'])
    target_weights = tuple([0.00046992481203007516, 0.00046992481203007516, 0.00046992481203007516, 0.00046992481203007516, 0.00046992481203007516, 0.00046992481203007516, 0.00046992481203007516, 0.00046992481203007516, 0.00046992481203007516, 0.00046992481203007516, 0.00046992481203007516, 0.00046992481203007516, 0.00046992481203007516, 0.00046992481203007516, 0.00046992481203007516, 0.00046992481203007516, 0.00046992481203007516, 0.00046992481203007516, 0.00046992481203007516, 0.00046992481203007516, 0.00046992481203007516, 0.00046992481203007516, 0.00046992481203007516, 0.00046992481203007516, 0.00046992481203007516, 0.00046992481203007516, 0.00046992481203007516, 0.00046992481203007516, 0.00046992481203007516, 0.00046992481203007516, 0.00046992481203007516, 0.00046992481203007516, 0.00046992481203007516, 0.00046992481203007516, 0.00046992481203007516, 0.00046992481203007516, 0.00046992481203007516, 0.00046992481203007516, 0.00046992481203007516, 0.00046992481203007516, 0.00046992481203007516, 0.00046992481203007516, 0.00046992481203007516, 0.00046992481203007516, 0.00046992481203007516, 0.00046992481203007516, 0.00046992481203007516, 0.00046992481203007516, 0.00046992481203007516, 0.00046992481203007516, 0.00046992481203007516, 0.00046992481203007516, 0.00046992481203007516, 0.00046992481203007516, 0.00046992481203007516, 0.00046992481203007516, 0.00046992481203007516, 0.00046992481203007516, 0.00046992481203007516, 0.00046992481203007516, 0.00046992481203007516, 0.00046992481203007516, 0.00046992481203007516, 0.00046992481203007516, 0.00046992481203007516, 0.00046992481203007516, 0.00046992481203007516, 0.00046992481203007516, 0.00046992481203007516, 0.00046992481203007516, 0.00046992481203007516, 0.00046992481203007516, 0.00046992481203007516, 0.00046992481203007516, 0.00046992481203007516, 0.00046992481203007516, 0.00046992481203007516, 0.00046992481203007516, 0.00046992481203007516, 0.00046992481203007516, 0.00046992481203007516, 0.00046992481203007516, 0.00046992481203007516, 0.00046992481203007516, 0.00046992481203007516, 0.000587406015037594, 0.000587406015037594, 0.000587406015037594, 0.000587406015037594, 0.000587406015037594, 0.000587406015037594, 0.000587406015037594, 0.000587406015037594, 0.000587406015037594, 0.000587406015037594, 0.000587406015037594, 0.000587406015037594, 0.000587406015037594, 0.000587406015037594, 0.000587406015037594, 0.000587406015037594, 0.000587406015037594, 0.000587406015037594, 0.000587406015037594, 0.000587406015037594, 0.000587406015037594, 0.000587406015037594, 0.000587406015037594, 0.000587406015037594, 0.000587406015037594, 0.000587406015037594, 0.000587406015037594, 0.000587406015037594, 0.000587406015037594, 0.000587406015037594, 0.000587406015037594, 0.000587406015037594, 0.000587406015037594, 0.000587406015037594, 0.000587406015037594, 0.000587406015037594, 0.000587406015037594, 0.000587406015037594, 0.000587406015037594, 0.000587406015037594, 0.000587406015037594, 0.000587406015037594, 0.000587406015037594, 0.000587406015037594, 0.000587406015037594, 0.000587406015037594, 0.000587406015037594, 0.000587406015037594, 0.000587406015037594, 0.000587406015037594, 0.000587406015037594, 0.000587406015037594, 0.000587406015037594, 0.000587406015037594, 0.000587406015037594, 0.0007048872180451127, 0.0007048872180451127, 0.0007048872180451127, 0.0007048872180451127, 0.0007048872180451127, 0.0007048872180451127, 0.0007048872180451127, 0.0007048872180451127, 0.0007048872180451127, 0.0007048872180451127, 0.0007048872180451127, 0.0007048872180451127, 0.0007048872180451127, 0.0007048872180451127, 0.0007048872180451127, 0.0007048872180451127, 0.0007048872180451127, 0.0007048872180451127, 0.0007048872180451127, 0.0007048872180451127, 0.0007048872180451127, 0.0007048872180451127, 0.0007048872180451127, 0.0007048872180451127, 0.0007048872180451127, 0.0007048872180451127, 0.0007048872180451127, 0.0007048872180451127, 0.0007048872180451127, 0.0007048872180451127, 0.0007048872180451127, 0.0007048872180451127, 0.0007048872180451127, 0.0007048872180451127, 0.0007048872180451127, 0.0007048872180451127, 0.0007048872180451127, 0.0007048872180451127, 0.0007048872180451127, 0.0007048872180451127, 0.0007048872180451127, 0.0007048872180451127, 0.0007048872180451127, 0.0007048872180451127, 0.0008223684210526315, 0.0008223684210526315, 0.0008223684210526315, 0.0008223684210526315, 0.0008223684210526315, 0.0008223684210526315, 0.0008223684210526315, 0.0008223684210526315, 0.0008223684210526315, 0.0008223684210526315, 0.0008223684210526315, 0.0008223684210526315, 0.0008223684210526315, 0.0008223684210526315, 0.0008223684210526315, 0.0008223684210526315, 0.0008223684210526315, 0.0008223684210526315, 0.0009398496240601503, 0.0009398496240601503, 0.0009398496240601503, 0.0009398496240601503, 0.0009398496240601503, 0.0009398496240601503, 0.0009398496240601503, 0.0009398496240601503, 0.0009398496240601503, 0.0009398496240601503, 0.0009398496240601503, 0.0009398496240601503, 0.0009398496240601503, 0.0009398496240601503, 0.0009398496240601503, 0.0009398496240601503, 0.0009398496240601503, 0.0009398496240601503, 0.0009398496240601503, 0.0009398496240601503, 0.0009398496240601503, 0.0009398496240601503, 0.0010573308270676691, 0.0010573308270676691, 0.0010573308270676691, 0.0010573308270676691, 0.0010573308270676691, 0.0010573308270676691, 0.0010573308270676691, 0.0010573308270676691, 0.0010573308270676691, 0.0010573308270676691, 0.0010573308270676691, 0.0010573308270676691, 0.0010573308270676691, 0.0010573308270676691, 0.0010573308270676691, 0.0010573308270676691, 0.0010573308270676691, 0.0010573308270676691, 0.0010573308270676691, 0.0010573308270676691, 0.001174812030075188, 0.001174812030075188, 0.001174812030075188, 0.001174812030075188, 0.001174812030075188, 0.001174812030075188, 0.001174812030075188, 0.001174812030075188, 0.001174812030075188, 0.001174812030075188, 0.001174812030075188, 0.001174812030075188, 0.001174812030075188, 0.001174812030075188, 0.001174812030075188, 0.001174812030075188, 0.001174812030075188, 0.0012922932330827067, 0.0012922932330827067, 0.0012922932330827067, 0.0012922932330827067, 0.0012922932330827067, 0.0012922932330827067, 0.0012922932330827067, 0.0012922932330827067, 0.0012922932330827067, 0.0012922932330827067, 0.0012922932330827067, 0.0014097744360902255, 0.0014097744360902255, 0.0014097744360902255, 0.0014097744360902255, 0.0014097744360902255, 0.0014097744360902255, 0.0014097744360902255, 0.0014097744360902255, 0.0014097744360902255, 0.0014097744360902255, 0.0014097744360902255, 0.0014097744360902255, 0.0014097744360902255, 0.0014097744360902255, 0.0014097744360902255, 0.0014097744360902255, 0.0014097744360902255, 0.0014097744360902255, 0.0014097744360902255, 0.0014097744360902255, 0.0015272556390977443, 0.0015272556390977443, 0.0015272556390977443, 0.0015272556390977443, 0.0015272556390977443, 0.0015272556390977443, 0.0015272556390977443, 0.0015272556390977443, 0.0015272556390977443, 0.0015272556390977443, 0.0015272556390977443, 0.001644736842105263, 0.001644736842105263, 0.001644736842105263, 0.001644736842105263, 0.001644736842105263, 0.001644736842105263, 0.001644736842105263, 0.001644736842105263, 0.001644736842105263, 0.001644736842105263, 0.001644736842105263, 0.001644736842105263, 0.001644736842105263, 0.001644736842105263, 0.001644736842105263, 0.001644736842105263, 0.001644736842105263, 0.001644736842105263, 0.0017622180451127819, 0.0017622180451127819, 0.0017622180451127819, 0.0017622180451127819, 0.0017622180451127819, 0.0017622180451127819, 0.0017622180451127819, 0.0017622180451127819, 0.0017622180451127819, 0.0017622180451127819, 0.0017622180451127819, 0.0017622180451127819, 0.0017622180451127819, 0.0017622180451127819, 0.0017622180451127819, 0.0017622180451127819, 0.0017622180451127819, 0.0018796992481203006, 0.0018796992481203006, 0.0018796992481203006, 0.0018796992481203006, 0.0018796992481203006, 0.0018796992481203006, 0.0018796992481203006, 0.0018796992481203006, 0.0019971804511278194, 0.0019971804511278194, 0.0019971804511278194, 0.0019971804511278194, 0.0019971804511278194, 0.0019971804511278194, 0.0019971804511278194, 0.0019971804511278194, 0.0021146616541353382, 0.0021146616541353382, 0.0021146616541353382, 0.0021146616541353382, 0.0021146616541353382, 0.0021146616541353382, 0.002232142857142857, 0.002232142857142857, 0.002232142857142857, 0.002232142857142857, 0.002232142857142857, 0.002232142857142857, 0.002232142857142857, 0.002232142857142857, 0.002232142857142857, 0.002232142857142857, 0.002232142857142857, 0.002232142857142857, 0.002349624060150376, 0.002349624060150376, 0.002349624060150376, 0.002349624060150376, 0.0024671052631578946, 0.0024671052631578946, 0.0024671052631578946, 0.0024671052631578946, 0.0024671052631578946, 0.0024671052631578946, 0.0025845864661654134, 0.0025845864661654134, 0.0025845864661654134, 0.0025845864661654134, 0.0025845864661654134, 0.0025845864661654134, 0.0025845864661654134, 0.002702067669172932, 0.002702067669172932, 0.002702067669172932, 0.002702067669172932, 0.002819548872180451, 0.0029370300751879698, 0.0029370300751879698, 0.0029370300751879698, 0.0029370300751879698, 0.0029370300751879698, 0.0029370300751879698, 0.0030545112781954886, 0.0030545112781954886, 0.0031719924812030073, 0.003289473684210526, 0.0035244360902255637, 0.0035244360902255637, 0.0035244360902255637, 0.0035244360902255637, 0.0035244360902255637, 0.0036419172932330825, 0.0036419172932330825, 0.0036419172932330825, 0.00387687969924812, 0.003994360902255639, 0.003994360902255639, 0.003994360902255639, 0.003994360902255639, 0.0042293233082706765, 0.0042293233082706765, 0.004346804511278195, 0.004464285714285714, 0.004464285714285714, 0.004581766917293233, 0.004699248120300752, 0.004699248120300752, 0.00481672932330827, 0.004934210526315789, 0.004934210526315789, 0.005051691729323308, 0.005286654135338346, 0.005404135338345864, 0.005521616541353383, 0.005756578947368421, 0.005756578947368421, 0.006109022556390977, 0.006109022556390977, 0.006343984962406015, 0.0064614661654135335, 0.006696428571428571, 0.00681390977443609, 0.00681390977443609, 0.007166353383458646, 0.007636278195488721, 0.00787124060150376, 0.008106203007518797, 0.008576127819548873, 0.00881109022556391, 0.008928571428571428, 0.008928571428571428, 0.00963345864661654, 0.00963345864661654, 0.00975093984962406, 0.00975093984962406, 0.00975093984962406, 0.009868421052631578, 0.012100563909774436, 0.01268796992481203, 0.013157894736842105, 0.013392857142857142, 0.01468515037593985, 0.015977443609022556, 0.022321428571428572, 0.024788533834586467, 0.02854793233082707, 0.03512687969924812, 0.0506343984962406])

    socket.setdefaulttimeout(1)
    executor = ThreadPoolExecutor(2)
    executor.submit(save)
    main()
    running = False
    executor.shutdown()

    # memory cleanup

    if "DANK_TOOL_VERSION" in os.environ:
        for _ in ('to_save', 'running', 'ips', 'server_type', 'port', 'save', 'saved', 'executor', 'translator', 'check_java', 'check_bedrock', 'check', 'generate_ip', 'generate_ip_targetted', 'target_ips', 'target_weights', 'main', 'translate'):
            if _ in globals(): del globals()[_]
