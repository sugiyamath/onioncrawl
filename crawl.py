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
        if url in ARRIVED:
            continue
        try:
            r = requests.get(url, timeout=10)
        except:
            ARRIVED.add(url)
            continue
        html = r.content.decode("utf-8")
        _save(html, url)
        for x in re.findall(reg, html):
            if x.startswith("http"):
                URLS.add(x)
            else:
                if x.startswith("/") and r.url.endswith("/"):
                    x = x[1:]
                URLS.add(r.url+x)
        ARRIVED.add(url)

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
        return False
    path = os.path.join(directory, *tmp.split("/"))
    run(f"mkdir -p {path}", shell=True)
    p = os.path.join(path, "data.html")
    if not os.path.isfile(p):
        with open(p, "w") as f:
            f.write(head + "\n" + html)
    return True

if __name__ == "__main__":
    crawl()
