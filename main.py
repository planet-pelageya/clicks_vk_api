import requests
import urllib.parse
import os
from dotenv import load_dotenv


SHORT_LINK_METHOD = "https://api.vk.com/method/utils.getShortLink"
lINK_INFO_METHOD = "https://api.vk.com/method/utils.getLinkStats"
API_VERSION = "5.199"
SHORT_LINK_MARKER = 'vk.cc'


def shorten_link(ACCESS_TOKEN, url):
    params = {
        "access_token": ACCESS_TOKEN,
        "v": API_VERSION,
        "url": url
    }
    response = requests.get(SHORT_LINK_METHOD, params=params)
    if response.ok:
        short_url = response.json()
        if "error" in short_url:
            error_message = short_url["error"]["error_code"]
            return f"Ошибка: {error_message}"
        else:
            short_url = short_url["response"]['short_url']
            return f"Ваша ссылка: {short_url}"
    else:
        return f"Ошибка: {response.status_code}"


def count_clicks(ACCESS_TOKEN, url):
    parsed_url = urllib.parse.urlparse(url)
    parts_of_link = parsed_url.path.split('/')
    key = parts_of_link[-1]
    params = {
        "access_token": ACCESS_TOKEN,
        "v": API_VERSION,
        "key": key,
        "interval": "forever"
    }
    response = requests.get(lINK_INFO_METHOD, params=params)
    if response.ok:
        response_json = response.json()
        if "error" in response_json:
            error_message = response_json["error"]["error_code"]
            return f"Ошибка: {error_message}"
        else:
            count_clicks = response_json["response"]['stats'][0]["views"]
            return f"Колличество кликов:{count_clicks}"
    else:
        return f"Ошибка: {response.status_code}"


def is_shorten_link(ACCESS_TOKEN, url):
    if SHORT_LINK_MARKER in urllib.parse.urlparse(url).netloc:
        return True
    else:
        return False


if __name__ == '__main__':
    url = input("введите ссылку ")
    load_dotenv()
    ACCESS_TOKEN = os.environ["ACCESS_TOKEN"]
    if is_shorten_link(ACCESS_TOKEN, url):
        print(count_clicks(ACCESS_TOKEN, url))
    else:
        print(shorten_link(ACCESS_TOKEN, url))


