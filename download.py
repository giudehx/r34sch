import os,uuid
from ui import RED,GREEN,END,BLUE,YELLOW
from curl_cffi import requests as c_requests
import random,time,threading
import ui

def getsafe(url, *args,**kwargs):
    IMPERSONATE_OPTIONS = ["chrome", "edge", "safari", "chrome110", "chrome120"]
    retries, delay = 9, 2
    if "headers" not in kwargs: kwargs["headers"] = {}
    with c_requests.Session() as s:
        while retries > 0:
            c_imp = kwargs.get("impersonate", random.choice(IMPERSONATE_OPTIONS))
            kwargs["impersonate"] = c_imp
            try:
                resp = s.get(url, *args, **kwargs)
                if resp.status_code == 200: return resp
                elif resp.status_code == 429: raise c_requests.errors.RequestsError("429 Too many requests")
                else: raise c_requests.err.RequestsError(f"Unexpected status {resp.status_code}")
            except (c_requests.errors.RequestsError, Exception) as e:
                retries-=1
                print(f"r34sch: {YELLOW}warn:{END} something happened, sleeping for {delay} seconds (retries: {retries})")
                time.sleep(delay)
                delay*=2
                kwargs["impersonate"]=random.choice([b for b in IMPERSONATE_OPTIONS if b != c_imp])

retries = 5
def download(urlf, out="r34out"):
    time.sleep(random.uniform(1,3))
    print(f"--> {BLUE}downloading:{END} {urlf}",end="",flush=True)
    try:
        headers = {
            'Referer': urlf,
            'Origin': urlf.split("/")[0]+"//"+urlf.split("/")[2]
        }
        unique=uuid.uuid4().hex[:8]
        fname=os.path.abspath(os.path.join(out,f"{unique}_{urlf.split('/')[-1]}"))
        r = getsafe(urlf, stream=True, headers=headers, impersonate="chrome")
        print(f" [{r.status_code}]",end="")
        with open(fname,'wb') as f:
            for c in r.iter_content(chunk_size=8192):
                f.write(c)
                print('.',end="",flush=True)
        # checking if file exists
        if not os.path.exists(fname): raise Exception(f"( OnO )=p File {fname} does not exist!")
        print(f" {GREEN}[ok]{END} ({os.path.getsize(fname)} bytes @ {fname})",flush=True)
        retries = 5
        time.sleep(0.25)
    except Exception as e:
        if retries == 0: return False
        retries -= 1
        print(f"r34sch: {RED}error:{END} error when downloading: {e}, attempting retry in 5 seconds...")
        time.sleep(5)
        download(fname,urlf,out)
