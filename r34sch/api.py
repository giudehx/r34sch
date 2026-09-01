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

from r34sch import ui
from r34sch.config import extractcfg
from r34sch.ui import fill_print
import requests, json, os, random
from r34sch import utils, constants
from datetime import datetime
from r34sch.utils import vb_print
import xml.etree.ElementTree as ET
import xmltodict

from r34sch.ui import c_ui
RED    = c_ui.RED
YELLOW = c_ui.YELLOW
GREEN  = c_ui.GREEN
BLUE   = c_ui.BLUE
END    = c_ui.END
RED_BG = c_ui.RED_BG

def getApiUid():
    api  = extractcfg()['api_key']
    user = extractcfg()['user_id']
    return api, user

def searchTag(tag):
    url = f"{constants.API_URL}/index.php?page=dapi&s=tag&q=index&name={tag}"
    api, user = getApiUid()
    resp = requests.get(url, params={"api_key": api, "user_id": user})
    resp.raise_for_status()
    root    = ET.fromstring(resp.text)
    tag     = root.find('tag')
    if tag is None: return {}
    t_type  = tag.get('type')
    t_count = tag.get('count')
    t_id    = tag.get('id')
    t_ambig = tag.get('ambiguous')
    return {"type": t_type, "count": t_count, "id": t_id, "ambiguous": t_ambig}

def searchapi(tag):
    url  = f"{constants.API_URL}/autocomplete.php?q={tag}"
    api,user=getApiUid()
    resp = requests.get(url, params={"api_key":api,"user_id":user})
    resp.raise_for_status()
    res = resp.json()
    if not res: print(F"r34sch: {RED}error:{END} nothing found for {tag}")
    print(f"\n{BLUE}search results for:{END} {YELLOW}{tag}{END}")
    for r in res: print(f"--> {GREEN}{r["label"]}{END}")

#       ^  :3
#  \____ \/W/\
#     /\\/./  \__
#   _/  \\/  |****|

def getFromId(id):
    url=f"{constants.API_URL}/index.php?page=dapi&s=post&q=index&id={id}&json=1"
    api,user=getApiUid()
    resp = requests.get(url, params={"api_key":api,"user_id":user})
    resp.raise_for_status()
    res = resp.json()
    if not res: print(f"r34sch: {RED}error:{END} nothing found for '{id}'")
    if constants.EXCLUDE_AI:
        for t in res[0]["tags"].split(' '):
            if t.startswith("ai_"):
                print(f"r34sch: {BLUE}ai:{END} detected: {t} in post. not downloading.")
                exit(1)
    return res

from r34sch.utils import filter_ai, api_only_image, api_only_video

def getPostsFromApi(limit,tags,rating,pid=None):
    if limit > 1000:
        print(f"r34sch: {RED}error:{END} cannot get more than 1000 posts via api")
        exit(1)
    # separate tags with a space
    post_url = constants.API_URL+"/index.php?page=dapi&s=post&q=index"
    api,user_id = getApiUid()
    #try:
    #    count = searchTag(tags)["count"]
    #    vb_print(f"Requesting {count} images for '{tags}'.")
    #except:
    #    print(f"r34sch: {RED}error:{END} no posts found for: {tags}")
    #    exit(1)
    #if int(count) > 1000: count = 1000
    count = 1000
    try:
        params = {"limit":count,"pid":pid,"tags":tags,"json":1,"api_key":api,"user_id":user_id} \
                 if pid is not None else {"limit":count,"tags":tags,"json":1,"api_key": api,"user_id":user_id}
        resp = requests.get(post_url, params=params)
        vb_print(f"Sent {resp.url} with status code of {resp.status_code}")
        resp.raise_for_status()
        try: posts = resp.json()
        except:
            print(f"r34sch: {RED}error:{END} nothing found for '{tags}'.")
            exit(1)
        vb_print(f"Applying modifiers:\n\tRandom: {bool(constants.RANDOM)}\n\tOnly Images: {bool(constants.ONLY_IMAGE)}\n\tOnly Videos: {bool(constants.ONLY_VIDEO)}\n\tExclude AI: {bool(constants.EXCLUDE_AI)}\n\tRating: {constants.RATING} ({rating})\n\tExtension(s): {constants.EXTENSION}")
        # -- filters --
        if constants.RANDOM:     random.shuffle(posts)
        if constants.ONLY_IMAGE: posts = api_only_image(posts)
        if constants.ONLY_VIDEO: posts = api_only_video(posts)
        if constants.EXCLUDE_AI: posts = filter_ai(posts)
        posts = utils.filter_rating(posts, rating=rating) # uhhhhh
        posts = utils.filter_extension(posts, constants.EXTENSION)
        # important
        posts = posts[:limit]
        vb_print("__________\n[ * done ]\n^^^^^^^^^^")
        print(f"{BLUE}[i]{END} retrieved {YELLOW}{len(posts)}{END} posts")
        return posts
    except Exception as e:
        print(f"r34sch: {RED}error:{END} failed to get a response, api_key or user_id may be invalid or expired, try reloading the r34sch.cfg file with a new api_key")
        print(f"detail: {e}")
        exit(1)

def getInfo(posts):
    for post in posts:
        print("\n---\n")
        for p in post:
            if p == "change":
                print(f"Last modified:\t{datetime.fromtimestamp(int(post[p]))} ({datetime.utcfromtimestamp(int(post[p]))} UTC)")
                continue
            pform = p.replace("_", " ")
            print(f"{pform.capitalize()}:\t{post[p]}")

def getComments(post_id):
    url       = f"{constants.API_URL}/index.php?page=dapi&s=comment&q=index&post_id={post_id}"
    api, user = getApiUid()
    resp      = requests.get(url, params={"api_key":api,"user_id":user})
    resp.raise_for_status()
    vb_print(f"Sent {resp.url} with status of {resp.status_code}")
    res       = resp.text
    xml_data  = xmltodict.parse(res)
    try: comments = xml_data["comments"]["comment"]
    except KeyError:
        print(f"r34sch: {RED}error:{END} comments for {post_id} do not exist.")
        exit(1)
    return comments

def parseComments(comments):
    print(f"{BLUE}Showing comments for {END}{YELLOW}'{comments[0]["@post_id"]}'{END}\n")
    for comment in comments:
        print(f"{GREEN}{comment["@creator"]}{END}({comment["@creator_id"]}) {BLUE}{comment["@created_at"]}{END} (ID {comment["@id"]}):")
        print(f"> {comment["@body"]}")
        print(fill_print(symbol="-"))
