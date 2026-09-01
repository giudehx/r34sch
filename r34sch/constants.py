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

import os

VERSION       = "1.3"

# urls
URL           = "https://rule34.xxx"
API_URL       = "https://api.rule34.xxx"

# folders
R34SCH_FOLDER = os.path.expanduser("~/.r34sch/")
TEMP_FOLDER   = os.path.join(R34SCH_FOLDER, "temp")
CACHE_FOLDER  = os.path.join(R34SCH_FOLDER, "cache")

# config
CONFIG_FILE   = "r34sch.cfg"
CONFIG_PATH   = os.path.join(R34SCH_FOLDER,CONFIG_FILE)

# options
VERBOSE            = False
API_THUMB_DOWNLOAD = False
EXCLUDE_AI         = False
RANDOM             = False
ONLY_IMAGE         = False
ONLY_VIDEO         = False
NO_COLOR           = False
RATING             = "all"
EXTENSION          = "all"
REPORT_TYPE        = "csv"
