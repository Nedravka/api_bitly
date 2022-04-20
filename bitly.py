import os
import argparse

import requests
from dotenv import load_dotenv
from urllib.parse import urlparse

LINK_API_BITLY = 'https://api-ssl.bitly.com/v4/'


def shorten_links(url, headers):
    url_for_shorten = {
        'long_url': url
    }
    response_a_shorten_link = requests.post(
        f'{LINK_API_BITLY}shorten',
        headers=headers,
        json=url_for_shorten
    )
    response_a_shorten_link.raise_for_status()
    return response_a_shorten_link.json()['id']


def count_clicks(bitlink, headers):
    parse_url = urlparse(bitlink)
    response_clicks_summary_for_a_bitlink = requests.get(
        f'{LINK_API_BITLY}bitlinks/{parse_url.netloc}'
        f'{parse_url.path}/clicks/summary', headers=headers
    )
    response_clicks_summary_for_a_bitlink.raise_for_status()
    return response_clicks_summary_for_a_bitlink.json()['total_clicks']


def is_bitlink(url, headers):
    parse_url = urlparse(url)
    response_retrieve_a_bitlink = requests.get(
        f'{LINK_API_BITLY}bitlinks/{parse_url.netloc}{parse_url.path}',
        headers=headers
    )
    return response_retrieve_a_bitlink.ok


def check_url_accessibility(url):
    return requests.get(url).raise_for_status()


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('name', nargs='?')
    return parser


def main(url):
    load_dotenv()
    token = os.getenv("bitly_token")
    headers = {
        'Authorization': f'Bearer {token}'
    }
    try:
        check_url_accessibility(url)
        if is_bitlink(url, headers):
            print('Количество кликов: ', count_clicks(url, headers))
        else:
            print('Битлинк: ', shorten_links(url, headers))
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


if __name__ == '__main__':
    parser = create_parser()
    namespace = parser.parse_args()
    if namespace.name:
        main(url=namespace.name)
    else:
        main(url=input('Введи ссылку для сокращения: '))
