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

import os,uuid
from src.ui import RED,GREEN,END,BLUE,YELLOW
from curl_cffi import requests as c_requests
import random,time,threading
from src import utils
from src import ui
from src import constants
from .metadata import writeMetadataToFile
def getsafe(url, *args,**kwargs):
    IMPERSONATE_OPTIONS = ["chrome", "edge", "safari", "chrome110", "chrome120"]
    retries, delay = 9, 2
    if "headers" not in kwargs: kwargs["headers"] = {}
    with c_requests.Session() as s:
        while retries > 0:
            c_imp = kwargs.get("impersonate", random.choice(IMPERSONATE_OPTIONS))
            kwargs["impersonate"] = c_imp
            try:
                resp = s.get(url, *args, **kwargs)
                if resp.status_code == 200: return resp
                elif resp.status_code == 429: raise c_requests.errors.RequestsError("429 Too many requests")
                else: raise c_requests.err.RequestsError(f"Unexpected status {resp.status_code}")
            except (c_requests.errors.RequestsError, Exception) as e:
                retries-=1
                print(f"r34sch: {YELLOW}warn:{END} something happened, sleeping for {delay} seconds (retries: {retries})")
                time.sleep(delay)
                delay*=2
                kwargs["impersonate"]=random.choice([b for b in IMPERSONATE_OPTIONS if b != c_imp])

def download(urlf, out="r34out"):
    print(f"--> {BLUE}downloading:{END} {urlf}",end="",flush=True)
    headers = {
        'Referer': urlf,
        'Origin': urlf.split("/")[0]+"//"+urlf.split("/")[2]
    }
    unique=uuid.uuid4().hex[:8]
    fname=os.path.abspath(os.path.join(out,f"r34sch_{unique}_{urlf.split('/')[-1]}"))
    r = getsafe(urlf, stream=True, headers=headers, impersonate="chrome")
    print(f" [{r.status_code}]",end="")
    url_fs = int(r.headers.get("Content-Length"))
    with open(fname,'wb') as f:
        for c in r.iter_content(chunk_size=8192):
            f.write(c)
            print(".",end="")
    # checking if file exists
    if not os.path.exists(fname): raise Exception(f"( OnO )=p File {fname} does not exist!")
    print(f" {GREEN}[ok]{END} ({os.path.getsize(fname)} bytes @ {fname})",flush=True)
    time.sleep(0.25)

def downloadApi(ret_arr, out="r34_out"):
    if not os.path.exists(out): os.makedirs(out)
    for link in ret_arr:
        if constants.API_THUMB_DOWNLOAD: urlf = link["preview_url"]
        else: urlf = link["file_url"]
        headers = {
            'Referer': urlf,
            'Origin': urlf.split("/")[0]+"//"+urlf.split("/")[2]
        }
        print(f"[{ret_arr.index(link)+1}/{len(ret_arr)}] {BLUE}downloading:{END} {YELLOW}{urlf}{END}",end="",flush=True)
        try:fname=os.path.abspath(os.path.join(out,link["image"]))
        except:
            unique=uuid.uuid4().hex[:8]
            fname=os.path.abspath(os.path.join(out,f"r34sch_{unique}_{urlf.split('/')[-1]}"))
        r = getsafe(urlf, stream=True, headers=headers, impersonate="chrome")
        print(f" [{r.status_code}]",end="")
        url_fs = int(r.headers.get("Content-Length"))
        with open(fname,'wb') as f:
            c_w=0
            for c in r.iter_content(chunk_size=8192):
                f.write(c)
                c_w+=8192
                ui.progress(utils.percent(c_w,url_fs))
        # checking if file exists, add metadata writing
        if not os.path.exists(fname): raise Exception(f"( OnO )=p File {fname} does not exist!")
        print(f"{GREEN}[ok]{END} ({os.path.getsize(fname)} bytes @ {YELLOW}{fname}{END})",flush=True)
        ui.run_spinner(f"... writing metadata for: {fname}")
        writeMetadataToFile(fname, link)
        ui.stop_spinner()
        time.sleep(0.25)
