import os
import platform
import socket
from urllib.request import Request, urlopen
from banner import banner

tool = "rvshell"
HOST = "0.0.0.0"
PORT = 9001
InternetProtocol = urlopen(Request("https://api.ipify.org")).read().decode().strip()
OSys = platform.system() + ' ' + platform.release()

banner(2)
'''print(
f"""
 ██▀███   ██▒   █▓  ██████  ██░ ██ ▓█████  ██▓     ██▓    
▓██ ▒ ██▒▓██░   █▒▒██    ▒ ▓██░ ██▒▓█   ▀ ▓██▒    ▓██▒    
▓██ ░▄█ ▒ ▓██  █▒░░ ▓██▄   ▒██▀▀██░▒███   ▒██░    ▒██░    
▒██▀▀█▄    ▒██ █░░  ▒   ██▒░▓█ ░██ ▒▓█  ▄ ▒██░    ▒██░    
░██▓ ▒██▒   ▒▀█░  ▒██████▒▒░▓█▒░██▓░▒████▒░██████▒░██████▒
░ ▒▓ ░▒▓░   ░ ▐░  ▒ ▒▓▒ ▒ ░ ▒ ░░▒░▒░░ ▒░ ░░ ▒░▓  ░░ ▒░▓  ░
  ░▒ ░ ▒░   ░ ░░  ░ ░▒  ░ ░ ▒ ░▒░ ░ ░ ░  ░░ ░ ▒  ░░ ░ ▒  ░
  ░░   ░      ░░  ░  ░  ░   ░  ░░ ░   ░     ░ ░     ░ ░   
   ░           ░        ░   ░  ░  ░   ░  ░    ░  ░    ░  ░
              ░
    Made by:    eSKa-0
    OS:         {OSys}
    IP:         {InternetProtocol}                                
""")'''

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(1)

while True:
    print(f"[+] listening on port {PORT}")
    client = s.accept()
    print(f"connected to {client[1]}")
    client[0].send("connected".encode("UTF-8"))
    while True:
        cmd = input(">>> ")
        client[0].send(cmd.encode("UTF-8"))
        if cmd.lower() in ["quit", "exit", "bye", 'q']:
            break
        result = client[0].recv(2048).decode("UTF-8")
        print(result)
        if cmd.lower() in ["cls", "clear"]:
            os.system('cls' if os.name == 'nt' else 'clear')
            banner(2)
            '''print(
f"""
 ██▀███   ██▒   █▓  ██████  ██░ ██ ▓█████  ██▓     ██▓    
▓██ ▒ ██▒▓██░   █▒▒██    ▒ ▓██░ ██▒▓█   ▀ ▓██▒    ▓██▒    
▓██ ░▄█ ▒ ▓██  █▒░░ ▓██▄   ▒██▀▀██░▒███   ▒██░    ▒██░    
▒██▀▀█▄    ▒██ █░░  ▒   ██▒░▓█ ░██ ▒▓█  ▄ ▒██░    ▒██░    
░██▓ ▒██▒   ▒▀█░  ▒██████▒▒░▓█▒░██▓░▒████▒░██████▒░██████▒
░ ▒▓ ░▒▓░   ░ ▐░  ▒ ▒▓▒ ▒ ░ ▒ ░░▒░▒░░ ▒░ ░░ ▒░▓  ░░ ▒░▓  ░
  ░▒ ░ ▒░   ░ ░░  ░ ░▒  ░ ░ ▒ ░▒░ ░ ░ ░  ░░ ░ ▒  ░░ ░ ▒  ░
  ░░   ░      ░░  ░  ░  ░   ░  ░░ ░   ░     ░ ░     ░ ░   
   ░           ░        ░   ░  ░  ░   ░  ░    ░  ░    ░  ░
              ░
    Made by:    eSKa-0
    OS:         {OSys}
    IP:         {InternetProtocol}                                
""")'''
            print(f"connected to {client[1]}")
    client[0].close()
    cmd = input("wait for new client y/n") or "y"
    if cmd.lower() in ["n" or "no"]:
        break
s.close()