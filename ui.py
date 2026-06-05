# R34Sch UI
RED = "\033[0;31m"
GREEN = "\033[0;32m"
BLUE = "\033[0;34m"
YELLOW = "\033[1;33m"
END = "\033[0m"
RED_BG = "\x1b[41m"

import time, threading, sys

sp_flag = threading.Event()
def Spinner(msg:str,stopflag):
    anim = "- / | \\"
    while not stopflag.is_set():
        m_len = len(msg)+2
        for a in anim.split():
            print(f"{msg} {a}", end="\r")
            sp_flag.wait(0.125)
            print(" "*m_len, end="\r")
    print(" "*m_len,end="\r")
    print(msg+f" {GREEN}[ok]{END}")
def run_spinner(msg:str):
    x=threading.Thread(target=Spinner,args=(msg,sp_flag,))
    x.start()
def stop_spinner(): sp_flag.set()

def printBottom(msg:str):
    sys.stdout.write(f"\033[s\033[999H\033[J{msg}\033[u")
    sys.stdout.flush()

