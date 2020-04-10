import json

import requests
import time

from bs4 import BeautifulSoup

from musicoin.models import MusicCopyright

list_url = 'https://www.musicow.com/auctions?tab=market&keyword=&sortorder=&page={page_number}'
detail_url = 'https://www.musicow.com/song/{song_id}'


def digits_to_number(text):
    return int(''.join([ch for ch in text if ch.isdigit()]))


def fetch_song_list(page_number):
    url = list_url.format(page_number=page_number)
    return requests.get(url).text


def parse_song_list_document(song_list_document):
    soup = BeautifulSoup(song_list_document, 'html.parser')
    song_list_tag = soup.find('ul', {'class': 'user_buy'})
    song_numbers = []
    if song_list_tag:
        for anchor in song_list_tag.find_all('a'):
            try:
                song_numbers.append(int(anchor['href'].strip('/song/')))
            except Exception:
                pass
    return song_numbers


def fetch_song_document(song_id):
    url = detail_url.format(song_id=song_id)
    return requests.get(url).text


def fetch_market_info(song_id):
    url = 'https://www.musicow.com/api/market'
    data = {'song_id': song_id}
    headers = {'referer': 'https://www.musicow.com/song/91'}
    response = requests.post(url, data=data, headers=headers)
    result = response.json()
    sell_list = result['market_order']['type'].get('1', [])
    buy_list = result['market_order']['type'].get('2', [])
    return sell_list, buy_list


def extract_title_info(soup):
    header_tag = soup.find('div', {'class': 'song_header'})
    title_info_tag = header_tag.find('div', {'class': 'information'})
    return {
        'title': title_info_tag.find('strong', {'class': 'title'}).text,
        'author': title_info_tag.find('em', {'class': 'artist'}).text,
    }


def fetch_income_history(song_id):
    url = 'https://www.musicow.com/song/{song_id}?tab=info'.format(song_id=song_id)
    html_doc = requests.get(url).text
    soup = BeautifulSoup(html_doc, 'html.parser')
    return soup


def extract_income_history(soup):
    script = soup.find('div', {'class': 'div_half'}).find('script', {'type': 'text/javascript'}).text
    try:
        line = next(filter(lambda line: line.strip().startswith('arr_amt_royalty_ym'), script.split('\n')))
    except StopIteration:
        return []
    json_data = line[line.find('{'): line.find(';')]
    yearly_incomes = sorted(json.loads(json_data).items())
    incomes = []
    for year, monthly_incomes in yearly_incomes:
        for month, income in sorted(monthly_incomes.items()):
            incomes.append(((int(year), int(month)), int(income)))
    return incomes


def parse_song_document(song_document):
    soup = BeautifulSoup(song_document, 'html.parser')
    title_info = extract_title_info(soup)
    return {
        'title_info': title_info,
    }


def find_song_documents(exec=None, error_handler=None):
    page_number = 1
    song_numbers = parse_song_list_document(fetch_song_list(page_number))
    while song_numbers:
        time.sleep(0.2)
        for song_number in song_numbers:
            try:
                song_document = fetch_song_document(song_number)
                song_info = parse_song_document(song_document)
                sell_list, buy_list = fetch_market_info(song_number)
                try:
                    lowest_price = sorted(map(int, sell_list.keys()))[0]
                except IndexError:
                    lowest_price = 0
                income_history_doc = fetch_income_history(song_number)
                income_history = extract_income_history(income_history_doc)
                last_year_income = sum(amount for (time, amount) in income_history[-12:])
                income_rate = last_year_income / lowest_price if lowest_price else 0
                song_info.update({'lowest_price': lowest_price})
                song_info.update({'song_id': song_number})
                song_info.update({'last_year_income': last_year_income})
                song_info.update({'income_rate': income_rate})
            except Exception as e:
                if getattr(error_handler, '__call__'):
                    error_handler(e)
            else:
                if getattr(exec, '__call__'):
                    exec(song_info)
            time.sleep(0.2)
        page_number += 1
        song_numbers = parse_song_list_document(fetch_song_list(page_number))


def update_song_info(song_info):
    title_info = song_info.get('title_info', '')
    stock_income_rate = song_info.get('income_rate', 0.0)
    stock_lowest_price = song_info.get('lowest_price', 0)
    last_12_months_income = song_info.get('last_year_income', 0)
    stock_sales = song_info.get('buy_options', [])
    MusicCopyright.objects.update_or_create(
        number=song_info['song_id'],
        defaults={
            'title': title_info and title_info.get('title'),
            'artist': title_info and title_info.get('author'),
            'stock_income_rate': stock_income_rate,
            'stock_lowest_price': stock_lowest_price,
            'last_12_months_income': last_12_months_income,
            'stock_sales': [],
        }
    )


