import requests
import os
from tqdm import tqdm
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin, urlparse
import time

def is_valid(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)


def get_list_of_images(url):
    array = []
    urls_array = []
    page = 1
    while len(array) < 100:
        tmp = url + "?page=" + str(page)
        urls_array.append(tmp)
        html = requests.get(tmp).content
        soup = bs(html, "html.parser")
        s = soup.find("table", {"summary": "Ogłoszenia"})
        l = s.find_all("img")
        img_urls = get_images_urls(l, tmp)
        array.extend(img_urls)
        page += 1
    return array

def get_images_urls(array, page_url):
    urls = []
    for img in tqdm(array, "Extracting..."):
        img_url = img.attrs.get("src")
        if not img_url:
            continue
        img_url = urljoin(page_url, img_url)
        try:
            pos = img_url.index("?")
            img_url = img_url[:pos]
        except ValueError:
            pass
        if(is_valid(img_url)):
            urls.append(img_url)
    return urls

def download(url, pathname):
    # if path doesn't exist, make that path dir
    if not os.path.isdir(pathname):
        os.makedirs(pathname)
    # download the body of response by chunk, not immediately
    response = requests.get(url, stream=True)
    # get the total file size
    file_size = int(response.headers.get("Content-Length", 0))
    # get the file name
    filename = os.path.join(pathname, url.split("/")[-1])
    #filename = os.path.join(pathname, str(it) + ".jpg")
    # progress bar, changing the unit to bytes instead of iteration (default by tqdm)
    progress = tqdm(response.iter_content(1024), f"Downloading {filename}", total=file_size, unit="B", unit_scale=True, unit_divisor=1024)
    time.sleep(10)
    with open(filename, "wb") as f:
        for data in progress:
            time.sleep(10)
            # write data read to the file
            f.write(data)
            # update the progress bar manually
            progress.update(len(data))

def main():
    url = "https://www.olx.pl/elektronika/q-pendrive/"
    path = "imgs"
    images= get_list_of_images(url)
    for img in images:
        download(img, path)

main()