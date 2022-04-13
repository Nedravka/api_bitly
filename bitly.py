import os

import requests
from dotenv import load_dotenv


def shorten_links(TOKEN, link_api_bitly, url):
    url_for_shorten = {
        'long_url': f'{url}'
    }

    short_link = requests.post(f'{link_api_bitly}shorten', headers=headers, json=url_for_shorten)
    short_link.raise_for_status()

    return short_link.json()['id']


def count_clicks(TOKEN, link_api_bitly, bitlink):
    response_number_of_clicks_on_bitlink = requests.get(f'{link_api_bitly}bitlinks/{bitlink}/clicks/summary', headers=headers)
    response_number_of_clicks_on_bitlink.raise_for_status()

    return response_number_of_clicks_on_bitlink.json()['total_clicks']


def is_bitlink(url):
    check_url = requests.get(f'{link_api_bitly}bitlinks/{url}', headers=headers)
    if check_url.ok:
        return True
    return False


if __name__ == '__main__':
    load_dotenv()
    TOKEN = os.getenv("BITLY_TOKEN")
    link_api_bitly = 'https://api-ssl.bitly.com/v4/'
    url = input('Введи ссылку для сокращения: ') #'https://www.atlassian.com/ru/git/tutorials/saving-changes/gitignore' 'bit.ly/3jx2kO8'
    headers = {
        'Authorization': f'Bearer {TOKEN}'
    }
    if is_bitlink(url):
        print('Количество кликов: ', count_clicks(TOKEN, link_api_bitly, url))
    else:
        try:
            validate_url = requests.get(url).raise_for_status()
            print('Битлинк: ', shorten_links(TOKEN, link_api_bitly, url))
        except:# requests.exceptions.HTTPError as error:
            # if error.response.status_code == 400:
            print('Не корректная ссылка')
            # else:
            #     raise requests.exceptions.HTTPError
