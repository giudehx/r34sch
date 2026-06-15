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

import os, shutil, sys
from src.constants import CONFIG_FILE, R34SCH_FOLDER, CONFIG_PATH
from src.ui import RED,END
def securecfg():
    if not os.path.exists(CONFIG_PATH): print("[??] well, thats a new one.")
    if sys.platform == "linux":
        os.chmod(CONFIG_PATH, 0o600)
        return True
    elif sys.platform == "win32":
        import subprocess
        subprocess.run(f"icalcs \"{CONFIG_PATH}\" /inheritance:r",shell=True,check=True)
        subprocess.run(f"icalcs \"{CONFIG_PATH}\" /grant:r \"{os.getlogin()}\":F",shell=True,check=True)
        return True
def loadcfg():
    if CONFIG_FILE in os.listdir(os.getcwd()):
        os.makedirs(R34SCH_FOLDER, exist_ok=True)
        shutil.copyfile(CONFIG_FILE, CONFIG_PATH)
        securecfg()
    else:
        print(f"r34sch: {RED}error:{END} no config file found, is the config named {CONFIG_FILE}?")
def extractcfg():
    if os.path.exists(CONFIG_PATH):
        creds = {}
        with open(CONFIG_PATH) as cfg:
            cfg.seek(0)
            config = str(cfg.read()).splitlines() # holy shit
            for line in config:
                if line.startswith('api_key='):   creds['api_key']=line.removeprefix('api_key=')
                elif line.startswith('user_id='): creds['user_id']=line.removeprefix('user_id=')
                elif line.startswith('cookie='):  creds['cookie']=line.removeprefix('cookie=')
            # if 'cookies' in cfg.read():
            #     cookies = cfg.read().strip('=')[3]
            #     creds['cookies']=cookies
        return creds
    else: return False
