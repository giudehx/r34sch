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

import os,sys

VERSION = "1.1"

# urls
URL="https://rule34.xxx"
API_URL="https://api.rule34.xxx"

# config
CONFIG_FILE="r34sch_config.cfg"
if sys.platform.startswith('linux'): R34SCH_FOLDER=os.path.expanduser("~/.r34sch/")
elif sys.platform.startswith('win'): R34SCH_FOLDER=os.path.expanduser("~//R34Sch//")
CONFIG_PATH = os.path.join(R34SCH_FOLDER,CONFIG_FILE)

# misc
API_THUMB_DOWNLOAD=False
