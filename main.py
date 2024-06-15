import requests
import urllib.parse
import os
from dotenv import load_dotenv

load_dotenv()
access_token = os.getenv("access_token")
access_token = '8ca4df288ca4df288ca4df284c8fbc47c388ca48ca4df28eac3e3d2779f4d335be97f67'
get_short_link = "https://api.vk.com/method/utils.getShortLink"
link_info = "https://api.vk.com/method/utils.getLinkStats"
url = input()
api_version = "5.199"
short_link_marker = 'vk.cc'
def shorten_link(access_token, url):
    params = {
        "access_token": access_token,
        "v": api_version,
        "url": url
    }
    response = requests.get(get_short_link, params=params)
    if response.status_code == 200:
        short_url = response.json()
        if "error" in short_url:
            error_message = short_url["error"]["error_code"]
            print(error_message)
        else:
            print(short_url["response"]['short_url'])
            return short_url["response"]['short_url']
    else:
        print (f"Ошибка: {response.status_code}")
def count_clicks(access_token, url):
    parsed_url = urllib.parse.urlparse(url)
    path = parsed_url.path
    parts = path.split('/')
    key = parts[-1]
    params = {
        "access_token": access_token,
        "v": api_version,
        "key": key
    }
    response = requests.get(link_info, params = params)
    if response.status_code == 200:
        response_json = response.json()
        if "error" in response_json:
            error_message = response_json["error"]["error_code"]
            print(error_message)
        else:
            print(response_json["response"]['stats'][0]["views"])
    else:
        print(f"Ошибка: {response.status_code}")
def is_shorten_link(url,access_token):
    if short_link_marker in urllib.parse.urlparse(url).netloc:
        count_clicks(access_token, url)
    else:
        shorten_link(access_token, url)


if __name__ == '__main__':
    is_shorten_link(url,access_token)


