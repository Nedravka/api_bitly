import os

import requests
from dotenv import load_dotenv
from urllib.parse import urlparse


LINK_API_BITLY = 'https://api-ssl.bitly.com/v4/'
load_dotenv()
TOKEN = os.getenv("BITLY_TOKEN")
HEADERS = {
    'Authorization': f'Bearer {TOKEN}'
}


def shorten_links(url, headers):
    url_for_shorten = {
        'long_url': f'{url}'
    }
    short_link = requests.post(f'{LINK_API_BITLY}shorten', headers=headers, json=url_for_shorten)
    short_link.raise_for_status()
    return short_link.json()['id']


def count_clicks(bitlink, headers):
    parse_url = urlparse(bitlink)
    response_number_of_clicks_on_bitlink = requests.get(f'{LINK_API_BITLY}bitlinks/{parse_url.netloc}{parse_url.path}/clicks/summary', headers=headers)
    response_number_of_clicks_on_bitlink.raise_for_status()
    return response_number_of_clicks_on_bitlink.json()['total_clicks']


def is_bitlink(url, headers):
    parse_url = urlparse(url)
    check_url = requests.get(f'{LINK_API_BITLY}bitlinks/{parse_url.netloc}{parse_url.path}', headers=headers)
    return check_url.ok


def check_url_accessibility(url):
    return requests.get(url).raise_for_status()


if __name__ == '__main__':

    url = input('Введи ссылку для сокращения: ')
    try:
        check_url_accessibility(url)
        if is_bitlink(url, HEADERS):
            print('Количество кликов: ', count_clicks(url, HEADERS))
        else:
            print('Битлинк: ', shorten_links(url, HEADERS))
    except requests.exceptions.HTTPError as err:
        print(err.response.status_code)
        if err.response.status_code in [400, 404]:
            print('Не корректная ссылка')
        elif err.response.status_code == 403:
            print('Проверьте токен доступа')
        else:
            raise
    except requests.exceptions.MissingSchema:
        print('Веедите ссылку в формате https://...')



