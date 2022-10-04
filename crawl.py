# torsocks -i python3 crawl.py
import os
import re
import requests
from subprocess import run

URLS = set()
ARRIVED = set()

def crawl():
    reg = re.compile(r'href="(.+?)"')
    URLS = set(_load_initials())
    while URLS:
        url = URLS.pop()
        if not _check_url(url):
            continue
        success, html, rurl = _download(url)
        if not success:
            continue
        _extract_urls(html, rurl, reg)


def _extract_urls(html, rurl, reg):
    for x in re.findall(reg, html):
        if x.startswith("http"):
            URLS.add(x)
        else:
            if x.startswith("/") and rurl.endswith("/"):
                x = x[1:]
            elif not x.startswith("/") and not rurl.endswith("/"):
                x = "/" + x                
            URLS.add(rurl+x)


def _download(url):
    try:
        r = requests.get(url, timeout=10)
        html = r.content.decode("utf-8")
        _save(html, url)
        flag = True
        rurl = r.url
    except:
        flag = False
        html = None
        rurl = None
    finally:
        ARRIVED.add(url)
    return flag, html, rurl
        
def _check_url(url):
    if ".onion" not in url:
        return False
    if url in ARRIVED:
        return False
    return True


def _load_initials(path="initials.txt"):
    with open(path) as f:
        for line in f:
            if line.startswith("http"):
                yield line.strip()


def _save(html, url, directory="download"):
    head = f"<!-- URL: {url} -->"
    if "https://" in url:
        tmp = url.replace("https://", "")
    elif "http://" in url:
        tmp = url.replace("http://", "")
    else:
        return
    path = os.path.join(directory, *tmp.split("/"))
    os.makedirs(path, exist_ok=True)
    p = os.path.join(path, "data.html")
    if not os.path.isfile(p):
        with open(p, "w") as f:
            f.write(head + "\n" + html)

if __name__ == "__main__":
    crawl()
