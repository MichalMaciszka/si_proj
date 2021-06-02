import requests
import requests.utils
from http.server import BaseHTTPRequestHandler, HTTPServer
import webbrowser
import os
from PyQt5 import QtCore
import numpy as np

CLIENT_ID = "a90652706b9a40eab09ba6d932775125"
CLIENT_SECRET = "8hn8faw2p2gomG8RTzK0iGx2eK8KZTQx7fTczRLr9GWdYq84PJG3rJfuA3DIgcG4"
OAUTH_URL = "https://allegro.pl/auth/oauth"
REDIRECT_URI = "http://localhost:8000"
TOKEN_URL = "https://allegro.pl/auth/oauth/token"
API_URL = "https://api.allegro.pl"

def get_access_code(client_id, redirect_uri = REDIRECT_URI, ouath_url = OAUTH_URL):
    auth_url = '{}/authorize'\
                '?response_type=code'\
                '&client_id={}' \
                '&redirect_uri={}'.format(ouath_url, client_id, redirect_uri)

    parsed_redirect_uri = requests.utils.urlparse(redirect_uri)
    server_address = parsed_redirect_uri.hostname, parsed_redirect_uri.port

    class AllegroAuthHandler(BaseHTTPRequestHandler):
        def __init__(self, request, address, server):
            super().__init__(request, address, server)

        def do_GET(self):
            self.send_response(200, 'OK')
            self.send_header('Content-Type', 'text/html')
            self.end_headers()

            self.server.path = self.path
            self.server.access_code = self.path.rsplit('?code=', 1)[-1]
    
    
    
    # print('server_address:', server_address)
    webbrowser.open(auth_url)
    httpd = HTTPServer(server_address, AllegroAuthHandler)
    print('Waiting for response with access_code from Allegro.pl (user authorization in progress)...')

    httpd.handle_request()
    httpd.server_close()
    access_code = httpd.access_code
    print("Auth code: ", access_code)
    return access_code

def sign_in(client_id, client_secret, access_code, redirect_uri=REDIRECT_URI, oauth_url=OAUTH_URL):
    token_url = TOKEN_URL
    access_token_data = {'grant_type': 'authorization_code',
                        'code': access_code,
                        'redirect_uri': redirect_uri}
    response = requests.post(url=token_url, auth=requests.auth.HTTPBasicAuth(client_id, client_secret), data=access_token_data)
    return response.json()

def refresh_token(client_id, client_secret, refresh_token, redirect_uri = REDIRECT_URI, ouath_url = OAUTH_URL):
    token_url = TOKEN_URL
    access_token_data = {'grant_type': 'refresh_token',
                         'refresh_token': refresh_token,
                         'redirect_uri': redirect_uri}
    response = requests.post(url=token_url,
                             auth=requests.auth.HTTPBasicAuth(client_id, client_secret),
                             data=access_token_data)

    return response.json()

def get_offers(access_token, phrase, num):
    headers = {}
    headers['charset'] = 'utf-8'
    headers['Accept-Language'] = 'pl-PL'
    headers['Content-Type'] = 'application/json'
    headers['Accept'] = 'application/vnd.allegro.public.v1+json'
    headers['Authorization'] = "Bearer {}".format(access_token)
    names_array = []
    images_urls_array = []

    with requests.Session() as session:
        session.headers.update(headers)
        response = session.get(API_URL + "/sale/products?phrase=" + phrase)
        response = response.json()
        next_page = response['nextPage']
        products = response['products'] #array with 30 products
        for x in products:
            if x['images']:
                names_array.append(x['name'])
                images_urls_array.append(x['images'][0]['url'])
        while len(names_array) < num:
            response = session.get(API_URL + "/sale/products?phrase=" + phrase + "&page.id=" + next_page['id'])
            response = response.json()
            next_page = response['nextPage']
            products = response['products']
            for x in products:
                if x['images']:
                    names_array.append(x['name'])
                    images_urls_array.append(x['images'][0]['url'])
                    if len(names_array) >= num:
                        break
    return names_array, images_urls_array


def download(url, path, it):
    if not os.path.isdir(path):
        os.makedirs(path)
    response = requests.get(url, stream=True)
    filename = os.path.join(path, str(it))
    filename += ".jpg"
    file = open(filename, "wb")
    file.write(response.content)
    file.close()
    print("Downloaded " + filename)

def write_access_token():
    file = open("keys.txt", "w")
    code = get_access_code(CLIENT_ID)
    r = sign_in(CLIENT_ID, CLIENT_SECRET, code)
    file.write(r['access_token'])
    file.close()


def download_and_get_texts(progressBar, num):
    write_access_token()
    notify = QtCore.pyqtSignal()
    file = open("keys.txt", "r")
    access_token = file.readline()
    # refresh_token = file.readline()
    file.close()
    names, images = get_offers(access_token, "pendrive", num)
    path = "imgs"
    file = open("names.txt", "w")
    for line in names:
        print(line)
        t = file.write(line)
        t = file.write('\n')
    no = 1
    for img in images:
        download(img, path, no)
        no += 1
        progressBar.setProperty("value", (no/num)*20)
    file.close()
    return names

def import_texts(path):
    file = open(path, 'r')
    names = file.readlines()
    file.close()
    return names


if __name__ == "__main__":
    download_and_get_texts()
