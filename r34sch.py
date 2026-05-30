'''
Documentation, License etc.

@package r34sch
'''
import requests, random, os, time
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
    retries, delay = 5, 2
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
                return resp
            except (c_requests.errors.RequestsError, Exception) as e:
                retries -= 1
                if retries == 0:
                    return resp
                print(f"r34sch: warn: rate-limited, sleeping for {delay} seconds (retries: {retries})")
                time.sleep(delay)
                delay *= 2
                kwargs["impersonate"] = random.choice([b for b in IMPERSONATE_OPTIONS if b != c_imp])
def r34search(prompt:str,
              pid=1,
              hd_image=True,
              images=10,
              rand=True):
    """
    Search R34 Content using a prompt.
    prompt (str): prompt to search (eg. foo_(bar))
    images (int): number of images to return, default is 5.
    rand (bool): If set to True (default), it will randomize the images.
    hd_image (bool): If set to True (default) it will download the image from the post instead of the thumbnail, if the searching takes too much time, set this to False.
    pid (int): Page number.
    """
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
    n_imgs = len(soup.select(".image-list span"))
    if n_imgs < images:
        print(f"r34sch: info: there are {n_imgs} images instead of {images}, sorry to dissapoint.")
        images = n_imgs
    img_src_array = []
    parsed = 1
    if hd_image:
        for a in soup.select('.image-list a'):
            if parsed == images+1: break
            img_url = URL+a['href']
            print(f"[{parsed}/{images}] r34sch: parsing: {img_url}")
            try:
                # Image parsing
                img_response = getsafe(img_url, impersonate="chrome")
                img_soup = BeautifulSoup(img_response.text, 'html.parser')
                img_src = img_soup.select_one('.flexi img')['src']
                img_src = img_src.replace(img_src[::-1].split('?')[0][::-1],'')[:-1]
                img_src_array.append(img_src)
            except:
                # Video parsing
                try:
                    try:hd = {"Cookie": os.getenv("R34_COOKIE")}
                    except:
                        print("r34sch: error: no cookie found.\nYou can fix it by:\n\n\t1. create a .env file at the same directory as r34sch.\n\t2. In the .env file, type: R34_COOKIE=\"<YOUR R34 COOKIE TEXT>\"")
                        exit(1)
                    video_r = getsafe(img_url, impersonate="chrome", headers=hd)
                    v_soup = BeautifulSoup(video_r.text, 'html.parser')
                    v_src = v_soup.select_one('.flexi video').select_one('source')['src']
                    v_src = v_src.replace(v_src[::-1].split('?')[0][::-1],'')[:-1]
                    img_src_array.append(v_src)
                except Exception as e:
                    print(f"r34sch: error: {e}")
                    exit(1)
            time.sleep(random.uniform(1, 2))
            parsed += 1
    else:
        for i in soup.select('.image-list img'):
            img_src=i['src']
            img_src = img_src.replace(img_src[::-1].split('?')[0][::-1],'')[:-1]
            img_src_array.append(img_src)
    # mods
    if rand:img_src_array=random.sample(img_src_array,len(img_src_array))
    return  img_src_array

def download(img_array:list, out="r34out"):
    os.makedirs(out, exist_ok=True)
    os.chdir(out)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': URL
    }
    for i in img_array:
        fname=i.split('/')[-1]
        r = requests.get(i, stream=True, headers=headers)
        r.raise_for_status()
        with open(fname,'wb') as f: f.write(r.content)
        print(f"[{img_array.index(i)+1}/{len(img_array)}] downloaded: {fname} ({os.path.getsize(fname)} bytes)")
        time.sleep(1)
    print(f"\nall done, files are in:\n\t{os.getcwd()}")

prompt=input("Insert prompt (R34): ")
nimg = int(input("How many images?: "))
urls=r34search(prompt, hd_image=True, images=nimg)
print("\n")
download(urls)
print("\n-- r34sch done, many thanks!! :D --")
