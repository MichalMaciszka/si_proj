import requests
import os
from tqdm import tqdm
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin, urlparse
import string


# only really used function from this file, less is irrelevant while we have access to Allegro API
def create_words_vector(all_texts):
    tmp = []
    words = []
    for item in all_texts:
        split = item.split()
        for i in split:
            a = i.lower()
            a = a.translate(str.maketrans('', '', string.punctuation))
            tmp.append(a)
    for x in tmp:
        if x not in words:
            words.append(x)
    return words


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

def download(url, pathname, it):
    # if path doesn't exist, make that path dir
    if not os.path.isdir(pathname):
        os.makedirs(pathname)
    # download the body of response by chunk, not immediately
    response = requests.get(url, stream=True)
    # get the total file size
    file_size = int(response.headers.get("Content-Length", 0))
    # get the file name
    # filename = os.path.join(pathname, url.split("/")[-1])
    filename = os.path.join(pathname, str(it))
    filename += ".jpg"
    # progress bar, changing the unit to bytes instead of iteration (default by tqdm)
    progress = tqdm(response.iter_content(1024), f"Downloading {filename}", total=file_size, unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "wb") as f:
        for data in progress:
            # write data read to the file
            f.write(data)
            # update the progress bar manually
            progress.update(len(data))


def get_text(url="https://www.olx.pl/elektronika/q-pendrive/"):
    list = []
    page = 1
    while len(list) < 100:
        print("Page = " + str(page), " Len = ", len(list))
        tmp = url + "?page=" + str(page)
        html = requests.get(tmp).content
        soup = bs(html, "html.parser")
        s = soup.find("table", {"summary": "Ogłoszenia"})
        for a in s.find_all("a"):
            item = a.find("strong")
            if item is not None:
                list.append(item.next)
        page += 1
    return list


def download_and_get_text():
    url = "https://www.olx.pl/elektronika/q-pendrive/"
    path = "imgs"
    images = get_list_of_images(url)
    no = 1
    for img in images:
        download(img, path, no)
        no += 1
    return get_text(url)
