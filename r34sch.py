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

import requests, random, os, time, sys
from bs4 import BeautifulSoup
from curl_cffi import requests as c_requests
from dotenv import load_dotenv
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
import threading
from src import ui, config
from src.ui import RED,GREEN,BLUE,YELLOW,END,RED_BG
load_dotenv()
from src.download import download,getsafe,downloadApi

from src.constants import URL
# OG Image scrapper by ClaustAI/Kiyopon

def parseUrl(hd_image,images,soup,pid,prompt):
    detected = []
    ui.run_spinner("--> scanning urls...")
    while len(detected) < images:
        if hd_image: links = soup.select('.image-list a')
        else: links = soup.select('.image-list img')
        if links == []: break
        for a in links:
            if len(detected) >= images: break
            if hd_image: detected.append(a['href'])
            else: detected.append(a['src'])
        if len(detected) >= images: break
        if len(detected) < images:
            pid     += 1
            pid      = 24 * pid
            url      = f'{URL}/index.php?page=post&s=list&tags={prompt}&pid={pid}'
            response = c_requests.get(url, impersonate="chrome")
            soup     = BeautifulSoup(response.text, 'html.parser')
    ui.stop_spinner()
    time.sleep(0.125) # for spinner
    return detected


def main(prompt:str,
              pid=1,
              hd_image=True,
              images=10,
              output="r34out"):
    if pid == 0:
        print("r34sch: error: page 0 is not allowed")
        exit(1)
    npid=24*pid
    if npid == 24: npid = 0
    pid=npid
    url = f'{URL}/index.php?page=post&s=list&tags={prompt}&pid={pid}'
    response = c_requests.get(url, impersonate="chrome")
    soup = BeautifulSoup(response.text, 'html.parser')
    check_404 = soup.select_one(".content h1")
    if "Nobody here but us chickens!".lower() in str(check_404).lower().strip():
        print(f"r34sch: {RED}error:{END} nothing found for {prompt}, try to reformulate the prompt. or make it yourself.")
        exit(1)
    detected = parseUrl(hd_image,images,soup,pid,prompt)
    if len(detected) < images:
        print(f"r34sch: info: we've detected {len(detected)} images instead of {images}")
        images = len(detected)
    if not os.path.exists(os.path.expanduser(output)): os.makedirs(os.path.expanduser(output), exist_ok=True)
    parsed=1
    for url in detected:
        if hd_image:
            if parsed == images+1: break
            img_url = URL+url
            time.sleep(random.uniform(1,3))
            print(f"[{parsed}/{images}] r34sch: {BLUE}parsing:{END} {img_url}")
            try:
                # Image parsing
                headers = {
                    'Referer': img_url,
                    'Origin': img_url.split("/")[0]+"//"+img_url.split("/")[2]
                }
                img_response = getsafe(img_url, impersonate="chrome", headers=headers)
                img_soup = BeautifulSoup(img_response.text, 'html.parser')
                img_src = img_soup.select_one('.flexi img')['src']
                img_src = img_src.replace(img_src[::-1].split('?')[0][::-1],'')[:-1]
                download(img_src, out=output)
            except:
                # Video parsing
                try:
                    hd = {
                        'Referer': img_url,
                        'Origin': img_url.split("/")[0]+"//"+img_url.split("/")[2],
                        "Cookie": config.extractcfg()["cookie"]
                    }
                    video_r = getsafe(img_url, impersonate="chrome", headers=hd)
                    v_soup = BeautifulSoup(video_r.text, 'html.parser')
                    v_src = v_soup.select_one('.flexi video').select_one('source')['src']
                    v_src = v_src.replace(v_src[::-1].split('?')[0][::-1],'')[:-1]
                    download(v_src, out=output)
                except Exception as e:
                    print(f"r34sch: {RED}error:{END} {e}, sorry!")
                    parsed -= 1
                    images -= 1
        else:
            if parsed == images+1: break
            try:
                img_src = url.replace(url[::-1].split('?')[0][::-1],'')[:-1]
                download(img_src, out=output)
            except Exception as e:
                print(f"r34sch: {RED}error:{END} {e}, sorry!")
        parsed += 1

# prompt=input("Insert prompt (R34): ")
# nimg = int(input("How many images?: "))
def quiet():
    devnull=open(os.devnull,'w')
    os.dup2(devnull.fileno(),sys.stdout.fileno())
    os.dup2(devnull.fileno(),sys.stderr.fileno())
import argparse
from src.constants import CONFIG_PATH
parser = argparse.ArgumentParser(prog="r34sch")
parser.add_argument("prompt", help="The prompt (or tag) for searching Rule 34 content (eg. character_(show) or just character)", type=str, nargs="?", default=None)
parser.add_argument("-i", "--images", help="The amount of images to download. Note that sometimes when you request a high number (more that the registered posts )", type=int, default=10)
parser.add_argument("-p", "--page", help="Tell the program what page to search", type=int, default=None)
parser.add_argument("-t", "--thumbnail", help="Only download the thumbnail instead of the post image, helps speed the program", action="store_true")
parser.add_argument("-o", "--output", help="Where the files will be downloaded", type=str)
parser.add_argument("-q", "--quiet", help="Disables output when running R34Sch.", action="store_true")
parser.add_argument("--load-config", help="Load the configuration file: r34sch.cfg", action="store_true")
parser.add_argument("--skip-metadata", help="Disable writing metadata when downloading files.", action="store_true")
parser.add_argument("--exclude-ai", help="Filter AI posts. Rejects a post from downloading if in one of its tags containes \'ai_\'.", action="store_true")
args=parser.parse_args()
from src import constants

print(f"\x1b[42mR34Sch {constants.VERSION}{END}")

if args.quiet: quiet()

if args.thumbnail:     constants.API_THUMB_DOWNLOAD = True
else:                  constants.API_THUMB_DOWNLOAD = False
if args.skip_metadata: constants.SKIP_METADATA = True
else:                  constants.SKIP_METADATA = False
if args.exclude_ai:    constants.EXCLUDE_AI = True
else:                  constants.EXCLUDE_AI = False

if args.load_config:
    from src.config import loadcfg
    loadcfg()
    exit(0)

if os.path.exists(CONFIG_PATH):
    from src import api
    ui.run_spinner("--> obtaining posts...")
    posts = api.getPostsFromApi(args.images, args.prompt, args.page)
    ui.stop_spinner()
    time.sleep(0.125)
    downloadApi(posts, args.output if args.output else "r34_out")
    exit(0)
else:
    # default to old scraping tools
    main(prompt=args.prompt,
        pid=1 if args.page == None else args.page,
        hd_image=False if args.thumbnail else True,
        images=args.images, output=args.output)
