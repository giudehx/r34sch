'''
Documentation, License etc.

@package r34sch
'''
import requests, random, os, time
from bs4 import BeautifulSoup

URL="https://rule34.us"
# OG Image scrapper by ClaustAI/Kiyopon
def r34search(prompt:str, hd_image=True, images=10, rand=True):
    """
    Search R34 Content using a prompt.
    prompt (str): prompt to search (eg. foo_(bar))
    images (int): number of images to return, default is 5.
    rand (bool): If set to True (default), it will randomize the images.
    hd_image (bool): If set to True (default) it will download the image from the post instead of the thumbnail, if the searching takes too much time, set this to False.
    """
    url = f'{URL}/index.php?r=posts/index&q={prompt}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    img_src_array = []
    if hd_image:
        for a in soup.select('.thumbail-container a'):
            img_url = a['href']
            img_response = requests.get(img_url)
            img_soup = BeautifulSoup(img_response.text, 'html.parser')
            img_src = img_soup.select_one('.content_push img')['src']
            if img_src.endswith('.png') or img_src.endswith('.jpeg') or img_src.endswith('.jpg'):
                img_src_array.append(img_src)
    else:
        for i in soup.select('.thumbail-container img'):
            img_src = i['src']
            if img_src.endswith('.png') or img_src.endswith('.jpeg') or img_src.endswith('.jpg'):
                img_src_array.append(img_src)
    # mods
    if rand:img_src_array=random.sample(img_src_array,k=images)
    else:   img_src_array=img_src_array[:images]
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
        r = requests.get(i, headers=headers, stream=True)
        r.raise_for_status()
        with open(fname,'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):f.write(chunk)
        print(f"downloaded: {fname} ({os.path.getsize(fname)} bytes)")
        time.sleep(1)
    print(f"\nall done, files are in:\n\t{os.getcwd()}")

prompt=input("[0_0] Insert prompt (R34): ")
nimg = int(input("How many images?: "))
urls=r34search(prompt, hd_image=False)
download(urls)
print("-- r34sch done, many thanks!! :D --")
