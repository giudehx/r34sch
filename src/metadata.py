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

from datetime import datetime
from PIL import Image, PngImagePlugin
import json, piexif
from mutagen.mp4 import MP4, MP4FreeForm
from .constants import API_THUMB_DOWNLOAD, VERSION
from . import ui

def writeMetadataToFile(fname, c_meta):
        # strange indentatiion, there was a try block but it was a pain to debug now ok
        if fname.endswith(".jpg") or fname.endswith(".jpeg"):
            img = Image.open(fname)
            # initialize exif structure for jpegs
            exif_dict = {"0th": {}, "Exif": {}, "GPS": {}, "1st": {}, "thumbnail": None}
            exif_dict["0th"][piexif.ImageIFD.Artist] = bytes(c_meta["owner"].encode('utf-8'))
            exif_dict["0th"][piexif.ImageIFD.DateTime] = datetime.fromtimestamp(c_meta["change"]).strftime("%Y-%m-%d %H:%M:%S").encode("utf-8")
            exif_dict["0th"][piexif.ImageIFD.Software] = bytes(f"R34Sch {VERSION}".encode('utf-8'))
            adata = {"id": c_meta["id"], "hash": c_meta["hash"],
                    "url": c_meta["preview_url"] if API_THUMB_DOWNLOAD else c_meta["file_url"],
                    "tags": c_meta["tags"]}
            desc = f"URL: {adata['url']}\n\nID: {adata['id']}\nHash: {adata['hash']}\n\nTags: {adata['tags']}"
            exif_dict["0th"][piexif.ImageIFD.ImageDescription] = bytes(desc.encode('utf-8'))
            exifb = piexif.dump(exif_dict)
            img.save(fname, exif=exifb)
        elif fname.endswith(".png"):
            data = {
                "Artist": c_meta["owner"],
                "Software": f"R34Sch {VERSION}",
                "URL": c_meta["preview_url"] if API_THUMB_DOWNLOAD else c_meta["file_url"],
                "Hash": c_meta["hash"],
                "ID": c_meta["id"],
                "DateTimeChanged": datetime.fromtimestamp(c_meta["change"]).strftime("%Y-%m-%d %H:%M:%S"),
                "Tags": c_meta["tags"].split(' ')}
            img  = Image.open(fname)
            meta = PngImagePlugin.PngInfo()
            for d in data: meta.add_text(d, str(data[d]))
            img.save(fname, pnginfo=meta)
        elif fname.endswith(".gif"):
            data = {
                "Artist": c_meta["owner"],
                "Software": f"R34Sch {VERSION}",
                "URL": c_meta["preview_url"] if API_THUMB_DOWNLOAD else c_meta["file_url"],
                "Hash": c_meta["hash"],
                "ID": c_meta["id"],
                "DateTimeChanged": datetime.fromtimestamp(c_meta["change"]).strftime("%Y-%m-%d %H:%M:%S"),
                "Tags": c_meta["tags"].split(' ')}
            img = Image.open(fname)
            img.save(fname, comment=bytes(json.dumps(data).encode('utf-8')))
        elif fname.endswith(".mp4"):
            video = MP4(fname)
            video["\xa9ART"] = [str(c_meta["owner"])]
            video["keyw"] =    c_meta["tags"].split(' ')
            video["\xa9nam"] = [str(c_meta["id"])]
            video["\xa9url"] = [c_meta["preview_url"] if API_THUMB_DOWNLOAD else c_meta["file_url"]]
            video["----:com.apple.iTunes:file_hash"] = [bytes(c_meta["hash"].encode('utf-8'))]
            video["----:com.apple.iTunes:date_changed"] = [bytes(datetime.fromtimestamp(c_meta["change"]).strftime("%Y-%m-%d %H:%M:%S").encode('utf-8'))]
            video.save()
        else:
            print(f"[??] internal error, {fname.split('.')[-1]} is not implemented")
