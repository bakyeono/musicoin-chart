from datetime import date
from operator import itemgetter
import json
import requests
import time

from bs4 import BeautifulSoup


url_template = 'https://www.musicoin.co/song/{song_id}'


def digits_to_number(text):
    return int(''.join([ch for ch in text if ch.isdigit()]))


def fetch_song_document(song_id):
    url = url_template.format(song_id=song_id)
    return requests.get(url).text


def extract_title_info(soup):
    title_info_tag = soup.find('div', attrs={'class': 'thumb_wrap'})
    return {
        'title': title_info_tag.find('strong').text,
        'author': title_info_tag.find('em', attrs={'class': 'name'}).text,
    }


def extract_buy_options(soup):
    buy_option_tags = soup.find('li', attrs={'class': 'u_buy_option'}).find_all('div', attrs={'class': 'option'})
    buy_options = []
    for buy_option_tag in buy_option_tags:
        items = buy_option_tag.find_all('li')
        stock_price = digits_to_number(items[0].text)
        num_stocks = digits_to_number(items[1].text)
        buy_options.append({'stock_price': stock_price, 'num_stocks': num_stocks})
    return buy_options


def extract_last_year_income(soup):
    income_info_tags = soup.find('ul', attrs={'class': 'old_money'}).find_all('li')
    return digits_to_number(income_info_tags[0].text)


def parse_song_document(song_document):
    soup = BeautifulSoup(song_document, 'html.parser')
    title_info = extract_title_info(soup)
    buy_options = extract_buy_options(soup)
    last_year_income = extract_last_year_income(soup)
    lowest_price = buy_options[-1]['stock_price'] if buy_options else 0
    income_rate = last_year_income / lowest_price if lowest_price else 0
    return {
        'title_info': title_info,
        'buy_options': buy_options,
        'last_year_income': last_year_income,
        'lowest_price': lowest_price,
        'income_rate': income_rate,
    }


def crawl_song_documents(start_song_id, end_song_id, exclude_ids=None):
    if exclude_ids is None:
        exclude_ids = set()

    song_infos = []
    for song_id in range(start_song_id, end_song_id):
        if song_id in exclude_ids:
            pring('skip:', song_id)
            continue
        try:
            song_document = fetch_song_document(song_id)
            song_info = parse_song_document(song_document)
            song_info.update({'song_id': song_id})
            song_infos.append(song_info)
            print(song_info)
        except Exception as e:
            print('error:', song_id, type(e), e)
        time.sleep(0.3)
    return song_infos


def sort_song_infos(song_infos, key='income_rate', reverse=True):
    return sorted(song_infos, key=itemgetter(key), reverse=reverse)


def save_song_infos(song_infos):
    with open(f'musicoin-{date.today()}.json', 'w') as file:
        file.write(json.dumps(song_infos))


if __name__ == '__main__':
    song_infos = sort_song_infos(crawl_song_documents(start_song_id=25, end_song_id=713))
    save_song_infos(song_infos)

