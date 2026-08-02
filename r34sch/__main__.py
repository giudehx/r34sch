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
from curl_cffi import const, requests as c_requests
from dotenv import load_dotenv
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
import threading
from r34sch import ui, config, constants
from r34sch.ui import RED,GREEN,BLUE,YELLOW,END,RED_BG
load_dotenv()
from r34sch.download import download,getsafe,downloadApi

from r34sch.constants import API_THUMB_DOWNLOAD, URL
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


def main_old(prompt:str,
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
from r34sch.constants import CONFIG_PATH

def main():
    try:
        parser = argparse.ArgumentParser(prog="r34sch")
        parser.add_argument("prompt", help="The prompt (or tag, or id if -I is passed) for searching Rule 34 content", type=str, nargs="?", default=None)
        parser.add_argument("-n", "--number", help="The number of images to download.", type=int, default=10)
        parser.add_argument("-i", "--info", help="Get the information of a post (if -I is passed) or posts instead of downloading", action="store_true")
        parser.add_argument("-v", "--verbose", help="Enable verbosity, basically more output when executing", action="store_true")
        parser.add_argument("-p", "--page", help="Tell the program what page to search", type=int, default=None)
        parser.add_argument("-t", "--thumbnail", help="Only download the thumbnail instead of the post image, helps speed the program", action="store_true")
        parser.add_argument("-o", "--output", help="Where the images will be downloaded, default is 'r34_out'", type=str)
        parser.add_argument("-T", "--tag-search", help="Search the type, count (n. posts) and id of a tag", action="store_true")
        parser.add_argument("-q", "--quiet", help="Disables output when running R34Sch.", action="store_true")
        parser.add_argument("-I", "--id", help="Download from an ID.", action="store_true")
        parser.add_argument("-r", "--rating", help="Filter posts by rating, options are: safe, questionable and explicit, can also be combined but have to be seperated by commas. (safe,questionable; explicit,safe ...)", type=str, default="all")
        parser.add_argument("-e", "--extension", help="Filter posts by extension, options are: png, jpg, jpeg, gif & mp4, can also be combined but have to be seperated by commas. (mp4,gif; png,jpeg,jpg; gif,png ...)", type=str, default="all")
        parser.add_argument("-s", "--search", help="Search for posts instead of downloading.", action="store_true")
        parser.add_argument("--no-write", help="Disable writing an archive after downloading", action="store_true")
        parser.add_argument("--load-config", help="Load the configuration file: r34sch.cfg, basically required, for more information read the README.md file", action="store_true")
        parser.add_argument("--exclude-ai", help="Filter AI posts. Rejects a post from downloading if in one of its tags containes \'ai_\'.", action="store_true")
        parser.add_argument("-R", "--random", help="Randomize posts.", action="store_true")
        parser.add_argument("--only-image", help="Retrieve only images", action="store_true")
        parser.add_argument("--only-video", help="Retrieve only videos", action="store_true")
        parser.add_argument("-c","--clear-cache", help="Clear the cache folder.", action="store_true")
        parser.add_argument("-l","--list-cache", help="View the currently cached/archived downloads.", action="store_true")
        parser.add_argument("-d","--delete",help="Delete a specific cache/archive, please do -l or --list-cache first", type=str)
        args=parser.parse_args()

        print(f"{GREEN}R34Sch {constants.VERSION}{END}")
        # do some cleaning
        import shutil
        from r34sch import api, utils

        shutil.rmtree(constants.TEMP_FOLDER)
        os.makedirs(constants.TEMP_FOLDER)

        if args.quiet:         quiet()
        if args.clear_cache:   utils.clear_cache()
        if args.list_cache:    utils.list_archives()

        constants.API_THUMB_DOWNLOAD = bool(args.thumbnail)
        constants.EXCLUDE_AI         = bool(args.exclude_ai)
        constants.RANDOM             = bool(args.random)
        constants.ONLY_IMAGE         = bool(args.only_image)
        constants.ONLY_VIDEO         = bool(args.only_video)
        constants.VERBOSE            = bool(args.verbose)
        constants.RATING             = args.rating
        constants.EXTENSION          = args.extension

        if args.tag_search:
            lol1 = api.searchTag(args.prompt)
            print(f"--> {BLUE}search results for:{END} {YELLOW}{args.prompt}:{END}")
            type_name = "Ambiguous"
            if   int(lol1["type"]) == 0: type_name = "Generic"
            elif int(lol1["type"]) == 1: type_name = "Artist"
            elif int(lol1["type"]) == 2: type_name = "Character"
            elif int(lol1["type"]) == 3: type_name = "Copyright"
            elif int(lol1["type"]) == 4: type_name = "Metadata generic"
            print(f"Type:\t{lol1["type"]} ({type_name})\nCount:\t{lol1["count"]}\nID:\t{lol1["id"]}")
            exit(0)

        if args.delete:
            utils.delete_archive(args.delete)
            exit(0)
        # it's and not &&!!
        if args.only_image and args.only_video:
            print(f"r34sch: {RED}error:{END} you cannot pass both --only-image and --only-video")
            exit(1)

        if args.search:
            api.searchapi(args.prompt)
            exit(0)

        if args.load_config:
            from src.config import loadcfg
            loadcfg()
            exit(0)

        if args.info:
            posts = api.getFromId(args.prompt) if args.id else api.getPostsFromApi(limit=args.number, tags=args.prompt, rating=args.rating, pid=args.page)
            api.getInfo(posts)
            exit(0)

        if args.id:
            ui.run_spinner("--> obtaining post...")
            posts = api.getFromId(args.prompt)
            ui.stop_spinner()
            time.sleep(0.125)
            downloadApi(posts, args.prompt, args.output if args.output else "r34_out", gen_archive=False)
            exit(0)

        if os.path.exists(CONFIG_PATH):
            ui.run_spinner("--> obtaining posts...")
            posts = api.getPostsFromApi(args.number, args.prompt, args.rating, args.page)
            ui.stop_spinner()
            time.sleep(0.125)
            c_posts = utils.read_cached_archive(args.prompt, args.output if args.output else "r34_out", posts)
            downloadApi(c_posts, args.prompt, args.output if args.output else "r34_out", gen_archive=False if args.no_write else True)
            exit(0)
        else:
            # default to old scraping tools
            print(f"[!] {YELLOW}you are running the old parser tool because you don't have the r34sch.cfg file loaded, such options like --exclude-ai, --random and etc are not supported in this mode.{END} this mode is going to be removed soon")
            main_old(prompt=args.prompt,
                pid=1 if args.page == None else args.page,
                hd_image=False if args.thumbnail else True,
                images=args.number, output=args.output)
    except Exception as e:
        print(f"r34sch: {RED}error:{END} {e}")
        exit(1)
if __name__ == "__main__": main()
