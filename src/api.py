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

from src.config import extractcfg
from src.constants import API_URL, R34SCH_FOLDER
from src.ui import RED,END, BLUE, YELLOW
import requests, json, os
from datetime import datetime
def getApiUid():
    api  = extractcfg()['api_key']
    user = extractcfg()['user_id']
    return api, user

import xml.etree.ElementTree as ET
def searchTag(tag):
    url = f"{API_URL}/index.php?page=dapi&s=tag&q=index&name={tag}"
    api, user = getApiUid()
    resp = requests.get(url, params={"api_key": api, "user_id": user})
    resp.raise_for_status()
    root    = ET.fromstring(resp.text)
    tag     = root.find('tag')
    if tag is None: return {}
    t_type  = tag.get('type')
    t_count = tag.get('count')
    t_id    = tag.get('id')
    return {"type": t_type, "count": t_count, "id": t_id}

def getPostsFromApi(limit,tags,pid=None):
    # separate tags with a space
    post_url = API_URL+"/index.php?page=dapi&s=post&q=index"
    api,user_id = getApiUid()
    r_val = ['preview_url','file_url',
            'hash','id','image','source',
            'change','owner','tags']
    ret_arr = []
    count = searchTag(tags)["count"]
    if int(limit) > int(count): limit = int(count)
    try:
        if pid is not None:
            params={
                "limit":   limit,
                "pid":     pid,
                "tags":    tags,
                "json":    1,
                "api_key": api,
                "user_id": user_id
            }
        else:
            params={
                "limit":   limit,
                "tags":    tags,
                "json":    1,
                "api_key": api,
                "user_id": user_id
            }
        resp = requests.get(post_url, params=params)
        resp.raise_for_status()
        posts = resp.json()
        for post in posts:
            all_p = {}
            for k in post:
                if k in r_val: all_p[k] = post[k]
            ret_arr.append(all_p)
        # print(f"debug url: {resp.url}")
        print(f"{BLUE}[i]{END} retrieved a total of {YELLOW}{len(ret_arr)}{END} posts")
        return ret_arr
    except Exception as e:
        print(f"r34sch: {RED}error:{END} failed to get a response [{resp.status_code}], api_key or user_id may be invalid or expired, try reloading the r34sch_config.cfg file with a new api_key")
        print(f"detail: {e}")
        exit(1)

