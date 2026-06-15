# R34Sch - CLI Rule 34 Scraper and downloader
# Copyright (C) 2026 GiudeHX <errno.giudetest@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# R34Sch UI
RED = "\033[0;31m"
GREEN = "\033[0;32m"
BLUE = "\033[0;34m"
YELLOW = "\033[1;33m"
END = "\033[0m"
RED_BG = "\x1b[41m"

import time, threading, sys
import os
sp_flag = threading.Event()
def Spinner(msg:str,stopflag):
    anim = "- \\ | /"
    while not stopflag.is_set():
        m_len = len(msg)+2
        for a in anim.split():
            print(f"{msg} {a}", end="\r")
            sp_flag.wait(0.125)
    print(" "*m_len,end="\r")
    print(msg+f" {GREEN}[ok]{END}")
def run_spinner(msg:str):
    if sp_flag.is_set(): sp_flag.clear()
    x=threading.Thread(target=Spinner,args=(msg,sp_flag,))
    x.start()
def stop_spinner(): sp_flag.set()

def progress(value, symbol="@"):
    ts = os.get_terminal_size()
    cl = int(str(ts).split('=')[1].split(',')[0])
    clp = cl-14 # [ &&& ] [  1.00%], where & is pbar
    pbar = "[ "+(" "*(clp))+f" ] [{value:6.2f}%]"
    print(pbar, end='\r')
    if not value >= 100:
        am = int((value/100)*clp)
        pbar = "[ "+(symbol*am)
        print(pbar, end='\r')
    else:
        print(" "*cl,end="\r")

def printBottom(msg:str):
    sys.stdout.write(f"\033[s\033[999H\033[J{msg}\033[u")
    sys.stdout.flush()
