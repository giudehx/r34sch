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

import os,uuid,shutil
from r34sch.ui import RED,GREEN,END,BLUE,YELLOW
from curl_cffi import requests as c_requests
import random,time,threading
from r34sch import utils
from r34sch import ui
from r34sch import constants
from r34sch.utils import vb_print
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

def downloadApi(ret_arr, tag, out="r34_out", gen_archive=True):
    if not os.path.exists(out): os.makedirs(out)
    if not os.path.exists(constants.TEMP_FOLDER): os.makedirs(constants.TEMP_FOLDER)
    dw_files, og_hash = [], []
    for link in ret_arr:
        if constants.API_THUMB_DOWNLOAD: urlf = link["preview_url"]
        else: urlf = link["file_url"]
        headers = {
            'Referer': urlf,
            'Origin': urlf.split("/")[0]+"//"+urlf.split("/")[2]
        }
        print(f"[{ret_arr.index(link)+1}/{len(ret_arr)}] {BLUE}downloading:{END} {YELLOW}{urlf}{END}",flush=True)
        # --
        pre_fname = link["image"]
        fname=os.path.abspath(os.path.join(constants.TEMP_FOLDER,pre_fname))
        r = getsafe(urlf, stream=True, headers=headers, impersonate="chrome")
        vb_print(f"[dw] Server returned {r.status_code}")
        url_fs = int(r.headers.get("Content-Length"))
        vb_print(f"[dw] Size of image is {url_fs} bytes")
        with open(fname,'wb') as f:
            c_wri = 0
            for c in r.iter_content(chunk_size=8192):
                f.write(c)
                c_wri += len(c)
                ui.progress(utils.percent(c_wri,url_fs))
        # checking if file exists, add metadata writing
        if not os.path.exists(fname): raise Exception(f"( OnO )=p File {fname} does not exist!")
        print(f"{GREEN}[ok]{END} ({os.path.getsize(fname)} bytes)",flush=True)
        # start new thread here
        dest_p = os.path.abspath(os.path.join(out, pre_fname))
        shutil.copy2(fname, dest_p)
        dw_files.append(dest_p)
        og_hash.append(link["hash"])
        vb_print(f"[dw] Downloaded {len(dw_files)} files.")
        os.remove(fname)
    # generate cache
    if ret_arr and gen_archive:
        print("[*] generating archive...")
        utils.create_cached_archive(dw_files, tag, meta=ret_arr)
        print(f"{GREEN}[ok]{END}")
