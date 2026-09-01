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

# R34Sch Utilities/Miscellaneous Stuff

def percent(min_n, max_n) -> float: return (min_n/max_n)*100

import shutil, hashlib, subprocess
import base64, os, tarfile, sys, json
from r34sch import constants
from r34sch.ui import fill_print, progress
from r34sch import ui

from r34sch.ui import c_ui
RED    = c_ui.RED
YELLOW = c_ui.YELLOW
GREEN  = c_ui.GREEN
BLUE   = c_ui.BLUE
END    = c_ui.END
RED_BG = c_ui.RED_BG

def vb_print(msg:str, *args, **kwargs):
    if constants.VERBOSE: print(msg, *args, **kwargs)

# -- filters --

def filter_ai(posts):
    ai_gen = []
    for post in posts:
        for tag in post["tags"].split(' '):
            if str(tag).startswith("ai_"):
                ai_gen.append(post)
                continue
    return [p for p in posts if p not in ai_gen]

def filter_rating(posts, rating:str):
    o_posts = [] # output posts
    if rating == "all": return posts
    rating = rating.split(',')
    for post in posts:
        for i in rating:
            if i in ["safe", "questionable", "explicit"]:
                if post["rating"] == i:
                    o_posts.append(post)
                    vb_print(f"--> grabbed post, length of o_posts is {len(o_posts)}")
            else:
                print(f"r34sch: {RED}error:{END} {i} is not a valid rating, you can choose between: safe, questionable & explicit.")
                exit(1)
    return o_posts

def filter_extension(posts, ext:str):
    o_posts = []
    if ext == "all": return posts
    ext = ext.split(',')
    for post in posts:
        for i in ext:
            if i in ["png","gif","mp4","jpeg","jpg"]:
                # abc123def456.ext
                if post["image"].split('.')[1] == i:
                    o_posts.append(post)
                    vb_print(f"FltExtension: length of o_posts is: {len(o_posts)}")
            else:
                print(f"r34sch: {RED}error:{END} {i} is not a valid type, you can choose between: png, gif, mp4 & jpeg/jpg")
                exit(1)
    return o_posts

def api_only_image(posts):   return [p for p in posts if p["image"].endswith((".png", ".jpeg", ".jpg", ".gif"))]
def api_only_video(posts):   return [p for p in posts if p["image"].endswith((".mp4"))]

def secure(fpath):
    vb_print(f"secure(): securing {os.path.abspath(fpath)}...")
    if sys.platform == "win32":
        # fuck you windows
        subprocess.run(["icacls",os.path.abspath(fpath),"/inheritance:d"],check=True,capture_output=True)
        subprocess.run(["icacls",os.path.abspath(fpath),"/remove","Users"],capture_output=True)
        subprocess.run(["icacls",os.path.abspath(fpath),"/remove","Everyone"],capture_output=True)
        subprocess.run(["icacls",os.path.abspath(fpath),"/grant:r",f"{os.getlogin()}:F"],check=True,capture_output=True)
    else:
        os.chmod(os.path.abspath(fpath), 0o600)

def encode_b64(name: str): return base64.urlsafe_b64encode(name.encode("utf-8")).decode("utf-8")
def decode_b64(name: str): return base64.urlsafe_b64decode(name.encode("utf-8")).decode("utf-8")

def write_report(report_path, post_ids, rp_type="csv"):
    # f"{constants.URL}/index.php?page=post&s=view&id={post_id}"
    if rp_type == "csv":
        rppth = os.path.join(report_path, "report.csv")
        with open(rppth, "w") as f:
            f.write("Filename,Path,ID,MD5,SHA256,URL")
            for fname in post_ids:
                # {filename: id, ...}
                hash_md5    = hashlib.md5(open(fname,'rb').read()).hexdigest()
                hash_sha256 = hashlib.sha256(open(fname,'rb').read()).hexdigest()
                file_report = f"{os.path.basename(fname)},{fname},{post_ids[fname]},{hash_md5},{hash_sha256},{constants.URL}/index.php?page=post&s=view&id={post_ids[fname]}"
                f.write(f"\n{file_report}")
                vb_print(f"write_report(): Wrote: {file_report}")
        return rppth
    if rp_type == "txt":
        rppth = os.path.join(report_path, "report.txt")
        with open(rppth, "w") as f:
            for fname in post_ids:
                hash_md5    = hashlib.md5(open(fname,'rb').read()).hexdigest()
                hash_sha256 = hashlib.sha256(open(fname,'rb').read()).hexdigest()
                file_report = f"Filename: {os.path.basename(fname)}\nPath: {fname}\nID: {post_ids[fname]}\nMD5: {hash_md5}\nSHA-256: {hash_sha256}\nURL: {constants.URL}/index.php?page=post&s=view&id={post_ids[fname]}"
                f.write(f"{file_report}\n---\n")
                vb_print(f"write_report(): Wrote: {file_report}")
        return rppth
    if rp_type == "none": return True

def gen_post_ids(meta, out):
    post_ids = {}
    for m in meta:
        abc = os.path.abspath(os.path.join(out, m["image"]))
        post_ids[abc] = m["id"]
    return post_ids

def gen_hashes(directory_to_hash, block=65536):
    vb_print(f"directory_to_hash: {directory_to_hash}")
    with open(os.path.join(directory_to_hash, "hashes"), 'w') as hsh:
        for ar in os.listdir(directory_to_hash):
            sha256 = hashlib.sha256()
            if ar == "hashes": continue
            with open(os.path.join(directory_to_hash, ar), 'rb') as f:
                for bl in iter(lambda: f.read(block), b''): sha256.update(bl)
            hsh.write(f"{os.path.join(directory_to_hash, ar)}|{sha256.hexdigest()}\n")
    return os.path.join(directory_to_hash, "hashes")

def verify_hashes(hashfile, base_dir):
    entries = []
    if os.path.exists(hashfile):
        with open(hashfile, 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 2:
                    hsh, fpath = parts
                    entries.append((parts[0], parts[1]))
                else: print('Error parsing hashes file: Invalid syntax...\nYou shouldn\'t modify this file!')
        def check(fname, expect):
            h = hashlib.sha256()
            with open(fname, 'rb') as f:
                for chunk in iter(lambda: f.read(65536), b""): h.update(chunk)
            return expect == h.hexdigest()
        for filepath,exp_hash in entries:
            filepath = os.path.abspath(os.path.join(base_dir, filepath))
            if filepath == "hashes": continue
            vb_print(f"Path is {filepath}")
            if not os.path.exists(filepath): print(f"r34sch: {YELLOW}warn:{END} file not found: {filepath}")
            elif check(filepath, exp_hash): print(f"{GREEN}-->{END} Verified: {filepath}")
            else:
                print(f"{RED}-->{END} Hash does not match: {filepath}. Removing.")
                os.remove(filepath)
    else:
        vb_print("Thought you were slick huh? Too bad.")
        shutil.rmtree(base_dir)
        os.makedirs(base_dir, exist_ok=True)


# -- CACHE --

# create a tar file 0o600 w all downloaded images inside
def create_cached_archive(dw_files, tag:str, meta):
    # downloaded files should be a list
    fname     = encode_b64(tag)
    arch_path = os.path.join(constants.CACHE_FOLDER, f"{fname}.tar.gz")
    vb_print(f"[cache] Creating {arch_path}...")
    if os.path.exists(arch_path):
        vb_print("[cache] Archive already exists, updating...")
        print(f"{BLUE}-->{END} Extracting old archive...")
        with tarfile.open(arch_path) as f:
            existing   = f.getnames()
            media_mbrs = [m for m in existing if m != "Metadata.json"]
            for i,m in enumerate(media_mbrs, 1):
                f.extract(member=m, path=constants.TEMP_FOLDER)
                vb_print(f"Extracted: {m}")
                progress(percent(i,len(media_mbrs)))
            f.extract(member="Metadata.json", path=constants.R34SCH_FOLDER)
            old = [os.path.abspath(os.path.join(constants.TEMP_FOLDER, m)) for m in media_mbrs]
        # merge metadatas
        print(f"{BLUE}-->{END} Merging metadatas...")
        with open(os.path.join(constants.R34SCH_FOLDER, "Metadata.json"), 'r') as f: old_meta = json.load(f)
        new_meta = []
        for d in meta + old_meta:
            if d not in new_meta: new_meta.append(d)
        meta = new_meta
        vb_print(f"Old metadata: {old_meta}\nNew metadata: {meta}")
        os.remove(os.path.join(constants.R34SCH_FOLDER, "Metadata.json"))
        dw_files += old
        dw_files  = list(dict.fromkeys(dw_files))
        vb_print(f"DW_FILES: {dw_files}")
    # catalog
    catalog_path = os.path.join(constants.TEMP_FOLDER, "Metadata.json")
    if os.path.exists(catalog_path): os.remove(catalog_path) # Remove existing metadata.json
    vb_print(f"temp folder: {os.listdir(constants.TEMP_FOLDER)}")
    with open(catalog_path,"w",encoding="utf-8") as f: json.dump(meta, f, indent=4)
    with tarfile.open(arch_path,"w:gz") as tar:
        for f in dw_files:
            tar.add(f,arcname=os.path.basename(f))
            vb_print(fill_print(f"--> Added {f} as {os.path.basename(f)}"))
            progress(percent(dw_files.index(f)+1,len(dw_files)))
        tar.add(catalog_path,arcname="Metadata.json")
        secure(arch_path)
    print(f"{BLUE}-->{END} Creating hashes file...")
    hshfile = gen_hashes(constants.CACHE_FOLDER)
    vb_print(f"Generated hash at {hshfile}")
    print(f"{YELLOW}    Created archive.{END}")
    return arch_path

def read_cached_archive(tag, out, meta):
    # search for tag in b64 format
    vb_print(f"[cache] Now checking for {tag}...")
    files   = [os.path.splitext(f)[0] for f in os.listdir(constants.CACHE_FOLDER)]
    tag_b64 = encode_b64(tag)
    vb_print(f"Found {len(files)} archives.")
    for d in files:
        d = d.split('.')[0]
        vb_print(f"[cache] Checked {d}")
        if tag_b64 == d:
            print(f"{BLUE}-->{END} Found existing archive for {tag}, extracting...")
            extr_path = os.path.join(constants.TEMP_FOLDER, tag)
            with tarfile.open(os.path.join(constants.CACHE_FOLDER, str(d)+".tar.gz")) as f:
                existing = f.getnames()
                vb_print(f"Existing (archive): {existing}")
                # f.extractall(out, members=track_extract_prg(f))
                for m in existing:
                    f.extract(member=m, path=extr_path)
                    progress(percent(existing.index(m)+1,len(existing)))
            print(f"{GREEN}-->{END} Extracted {len(existing)} images.")
            with open(os.path.join(extr_path,"Metadata.json")) as f: mdata_json = json.load(f)
            # filters
            if constants.EXCLUDE_AI: mdata_json = filter_ai(mdata_json)
            if constants.ONLY_IMAGE: mdata_json = api_only_image(mdata_json) # TO TEST
            if constants.ONLY_VIDEO: mdata_json = api_only_video(mdata_json)
            mdata_json = filter_rating(mdata_json, constants.RATING)
            mdata_json = filter_extension(mdata_json, constants.EXTENSION)
            vb_print(f"Metadata.json: {mdata_json}")
            imgs = [m["image"] for m in mdata_json]
            print(f"{BLUE}-->{END} Copying {len(imgs)} images to {out}...")
            if not os.path.exists(out): os.makedirs(out)
            for img in imgs:
                shutil.copy2(os.path.join(extr_path,img),os.path.join(out,img))
                progress(percent(imgs.index(img)+1,len(imgs)))
            print(f"{GREEN}-->{END} Success.")
            n_imgs = [n["image"] for n in meta if n["image"] not in set(imgs)]
            vb_print(f"read_cached_archive:\n\timages: {imgs}\n\tnew imgs: {n_imgs}\n\tReturn: {[m for m in meta if m["image"] in n_imgs]}")
            shutil.rmtree(constants.TEMP_FOLDER)
            os.makedirs(constants.TEMP_FOLDER, exist_ok=True)
            return   [m for m in meta if m["image"] in n_imgs]
    return meta

def delete_archive(archive):
    arch_p = os.path.join(constants.CACHE_FOLDER, encode_b64(archive)+".tar.gz")
    vb_print(f"Looking for {arch_p} ...")
    if not os.path.exists(arch_p):
        print(f"r34sch: {RED}error:{END} {archive} does not exist")
        exit(1)
    vb_print("Found, deleting ...")
    os.remove(arch_p)
    vb_print("OK")

def list_archives():
    files = [os.path.splitext(f)[0].split('.')[0] for f in os.listdir(constants.CACHE_FOLDER)]
    vb_print(f"{files}",flush=True)
    names = [decode_b64(str(a)) for a in files]
    for n in names: print(f"--> {YELLOW}{n}{END}")
    if not names:   print("[ * But nobody came... ]")
    exit(0)

def clear_cache():
    shutil.rmtree(constants.CACHE_FOLDER)
    os.makedirs(constants.CACHE_FOLDER, exist_ok=True)
    exit(0)
