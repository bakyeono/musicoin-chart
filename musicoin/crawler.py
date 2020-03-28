import requests
import time

from bs4 import BeautifulSoup

from musicoin.models import MusicCopyright

list_url = 'https://www.musicoin.co/auctions?tab=market&keyword=&sortorder=&page={page_number}'
detail_url = 'https://www.musicoin.co/song/{song_id}'


def digits_to_number(text):
    return int(''.join([ch for ch in text if ch.isdigit()]))


def fetch_song_list(page_number):
    url = list_url.format(page_number=page_number)
    return requests.get(url).text


def parse_song_list_document(song_list_document):
    soup = BeautifulSoup(song_list_document, 'html.parser')
    song_list_tag = soup.find('ul', attrs={'class': 'user_buy'})
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


def find_song_documents_between(start_song_id, end_song_id, exclude_ids=None):
    if exclude_ids is None:
        exclude_ids = set()

    song_infos = []
    for song_id in range(start_song_id, end_song_id):
        if song_id in exclude_ids:
            continue
        try:
            song_document = fetch_song_document(song_id)
            song_info = parse_song_document(song_document)
            song_info.update({'song_id': song_id})
            song_infos.append(song_info)
        except Exception as e:
            pass
        time.sleep(0.2)
    return song_infos


def find_song_documents(exec=None, error_handler=None):
    page_number = 1
    song_numbers = parse_song_list_document(fetch_song_list(page_number))
    time.sleep(0.2)
    while song_numbers:
        for song_number in song_numbers:
            try:
                song_document = fetch_song_document(song_number)
                song_info = parse_song_document(song_document)
                song_info.update({'song_id': song_number})
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
            'stock_sales': stock_sales,
        }
    )


def find_and_update_song_infos():
    find_song_documents(update_song_info)

