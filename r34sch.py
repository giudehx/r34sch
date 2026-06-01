'''
Documentation, License etc.

@package r34sch
'''
import requests, random, os, time, sys
from bs4 import BeautifulSoup
from curl_cffi import requests as c_requests
from dotenv import load_dotenv
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
load_dotenv()

IMPERSONATE_OPTIONS = ["chrome", "edge", "safari", "chrome110", "chrome120"]
URL="https://rule34.xxx"
# OG Image scrapper by ClaustAI/Kiyopon
def getsafe(url, *args,**kwargs):
    retries, delay = 6, 2
    if "headers" not in kwargs:
        kwargs["headers"] = {}
    while retries > 0:
        with c_requests.Session() as s:
            c_imp = kwargs.get("impersonate", random.choice(IMPERSONATE_OPTIONS))
            kwargs["impersonate"] = c_imp
            try:
                resp = s.get(url, *args, **kwargs)
                if resp.status_code == 403:
                    raise c_requests.errors.RequestsError("403 blocked")
                if resp.status_code == 429:
                    raise c_requests.errors.RequestsError("429 too many requests")
                return resp
            except (c_requests.errors.RequestsError, Exception) as e:
                retries -= 1
                if retries == 0:
                    return resp
                print(f"r34sch: warn: rate-limited, sleeping for {delay} seconds (retries: {retries})")
                time.sleep(delay)
                delay *= 2
                kwargs["impersonate"] = random.choice([b for b in IMPERSONATE_OPTIONS if b != c_imp])
def download(urlf, out="r34out"):
    print(f"--> downloading: {urlf}", end="")
    if not os.path.exists(os.path.abspath(out)):
        os.makedirs(os.path.abspath(out), exist_ok=True)
    os.chdir(os.path.abspath(out))
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': URL
    }
    fname=urlf.split('/')[-1]
    r = requests.get(urlf, stream=True, headers=headers); print(".", end="")
    r.raise_for_status()
    with open(fname,'wb') as f:
        for c in r.iter_content(chunk_size=8192):
            f.write(c)
            print(".", end="")
    print(" [ok]")
    os.chdir("..")
    time.sleep(0.25)
def r34search(prompt:str,
              pid=1,
              hd_image=True,
              images=10):
    """
    Search R34 Content using a prompt.
    prompt (str): prompt to search (eg. foo_(bar))
    images (int): number of images to return, default is 5.
    hd_image (bool): If set to True (default) it will download the image from the post instead of the thumbnail, if the searching takes too much time, set this to False.
    pid (int): Page number.
    """
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
        print(f"r34sch: error: nothing found for {prompt}, try to reformulate the prompt. or make it yourself.")
        exit(1)
    # fancy url scraping
    detected = []
    while len(detected) < images:
        if hd_image: links = soup.select('.image-list a')
        else: links = soup.select('.image-list img')
        if links == []: break
        for a in links:
            print(f"FOUND LINK --> {a['href']}")
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
        print(detected)
    if len(detected) < images:
        print(f"r34sch: info: we've detected {len(detected)} images instead of {images}")
        images = len(detected)
    img_src_array = []
    parsed = 1
    if hd_image:
        for a in detected:
            if parsed == images+1: break
            img_url = URL+a
            print(f"[{parsed}/{images}] r34sch: parsing: {img_url}")
            try:
                # Image parsing
                img_response = getsafe(img_url, impersonate="chrome")
                img_soup = BeautifulSoup(img_response.text, 'html.parser')
                img_src = img_soup.select_one('.flexi img')['src']
                img_src = img_src.replace(img_src[::-1].split('?')[0][::-1],'')[:-1]
                img_src_array.append(img_src)
                download(img_src)
            except:
                # Video parsing
                try:
                    hd = {"Cookie": os.getenv("R34_COOKIE")}
                    video_r = getsafe(img_url, impersonate="chrome", headers=hd)
                    v_soup = BeautifulSoup(video_r.text, 'html.parser')
                    v_src = v_soup.select_one('.flexi video').select_one('source')['src']
                    v_src = v_src.replace(v_src[::-1].split('?')[0][::-1],'')[:-1]
                    download(v_src)
                    img_src_array.append(v_src)
                except Exception as e:
                    print(f"r34sch: error: {e}, sorry!")
                    images -= 1
                    continue
            time.sleep(random.uniform(0.5, 1.5))
            parsed += 1
    else:
        for i in detected:
            if parsed == images+1: break
            img_src = i.replace(i[::-1].split('?')[0][::-1],'')[:-1]
            img_src_array.append(img_src)
            download(img_src)
            parsed += 1
    # mods.. there were mods
    return img_src_array

prompt=input("Insert prompt (R34): ")
nimg = int(input("How many images?: "))
urls=r34search(prompt, hd_image=True, images=nimg)
print("\n-- r34sch done, many thanks!! :D --")
