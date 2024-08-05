import requests
from datetime import datetime
from bs4 import BeautifulSoup
import re
from collections import defaultdict
import json
import sys


def get_quizplease():
    # URL для получения расписания мероприятий в Алматы
    url = 'https://almaty.quizplease.ru/schedule'

    # Отправка GET-запроса для получения страницы
    response = requests.get(url)
    if response.status_code == 200:  # Проверка статуса ответа, должен быть 200 для успешного запроса

        # Парсинг страницы с использованием BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Поиск всех блоков с информацией о мероприятиях
        events = soup.find_all('div', class_='schedule-column')

        # Список для хранения информации о мероприятиях
        events_info = []

        # Проход по каждому блоку и извлечение нужных данных
        for i, event in enumerate(events):
            # Дата проведения
            date_element = event.find('div', class_='h3 h3-green h3-mb10 block-date-with-language-game game-active') or \
                           event.find('div', class_='h3 h3-yellow h3-mb10 block-date-with-language-game game-end') or \
                           event.find('div', class_='h3 h3-mb10 block-date-with-language-game')
            if date_element:
                date_text = date_element.text.strip()
                date_match = re.search(r'(\d{1,2} \w+)', date_text)
                date_ = date_match.group(1)

            # Название игры
            title_element = event.find('div', class_='h2 h2-game-card h2-left')
            title = title_element.text.strip()

            # Место проведения
            place_element = event.find('div', class_='schedule-block-info-bar')
            place = place_element.text.strip()

            # Время проведения
            time_element = event.find_all('div', class_='techtext')
            if time_element:
                time_text = time_element[-1].text.strip()
                time_match = re.search(r'(\d{2}:\d{2})', time_text)
                time = time_match.group(1)

            date = convert_date(str(date_))

            events_info.append({
                "date": date,
                "title": title,
                "place": str(place).replace('`', "'"),
                "time": time
            })
    return events_info

def get_quizium():
    # URL для AJAX-запроса
    ajax_url = "https://quizium.ru/ajax?city=4280&date=0&location=all&type=all&level=all&status-reserv=0&status=0&category=offline&limit=30&action=get/games"

    # Заголовки, которые могут потребоваться для выполнения запроса
    headers = {
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'
    }

    # Выполняем GET-запрос
    response = requests.get(ajax_url, headers=headers)

    # Проверяем успешность запроса
    if response.status_code == 200:
        # Парсим HTML контент
        soup = BeautifulSoup(response.content, 'html.parser')

        # Находим расписание (пример поиска, измените под свои нужды)
        events = soup.find_all('div', class_='col-xs-6 col-md-6 col-sm-12 offset')  # Пример класса, замените на реальный

        # Сохраняем результаты в словарь
        schedule = []
        for i, event in enumerate(events):
            date_ = event.find('span', class_='date-kviz').text.strip()
            date = convert_date(str(date_))
            event_details = {
                'date': date,
                'title': event.find('span', class_='title-card').text.strip(),
                'place': str(event.find('span', class_='card-location-kviz').text.strip()).replace('`', "'"),
                'time': event.find('span', class_='card-time-kviz').text.strip()
            }
            schedule.append(event_details)

        return schedule
    else:
        print("Ошибка выполнения запроса")
        return None

def get_club60sec():

    # URL для получения расписания мероприятий в Алматы
    url = 'https://club60sec.ru/city/almaty'

    # Отправка GET-запроса для получения страницы
    response = requests.get(url)
    if response.status_code == 200:  # Проверка статуса ответа, должен быть 200 для успешного запроса

        # Парсинг страницы с использованием BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Поиск всех блоков с информацией о мероприятиях
        events = soup.find_all('div', class_='schedule_games_item wow fadeInUp')

        # Список для хранения информации о мероприятиях
        events_info = []

        # Проход по каждому блоку и извлечение нужных данных
        for event in events:
            date_time_elements = event.find_all('div', class_='schedule_detail_item schedule_detail_item--date')
            title_element = event.find('h3', class_='schedule_games_item_title')
            address_element = event.find('div', class_='schedule_detail_item schedule_detail_item--address')

            # Извлечение названия мероприятия
            title = title_element.get_text(strip=True) if title_element else "Название не найдено"

            # Извлечение адреса мероприятия
            address = address_element.get_text(strip=True) if address_element else "Адрес не найден"

            for element in date_time_elements:
                # Извлечение текста и разделение даты и времени
                date_text = element.get_text(strip=True)

                # Извлечение даты и времени
                date_match = re.search(r'(\d{2} \w+)', date_text)
                time_match = re.search(r'(\d{2}:\d{2})', date_text)

                date_ = date_match.group(1) if date_match else "Дата не найдена"
                time = time_match.group(1) if time_match else "Время не найдено"
                date = convert_date(str(date_))
                # Добавление данных в список
                events_info.append({
                    "date": date,
                    "title": title,
                    "place": str(address).replace('`', "'"),
                    "time": time

                })
        return events_info

def get_quizyasha():
    # Устанавливаем кодировку для стандартного вывода
    sys.stdout.reconfigure(encoding='utf-8')

    # URL-адреса запросов и их заголовки
    requests_data = [
        {
            'url': 'https://store.tildaapi.pro/api/getproductslist/?storepartuid=108952566671&recid=727992541&c=1717447987100&getparts=true&getoptions=true&slice=1&size=3',
            'headers': {
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate, br, zstd',
                'Accept-Language': 'ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7',
                'Dnt': '1',
                'Origin': 'https://quizyasha.kz',
                'Referer': 'https://quizyasha.kz/',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'cross-site',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'
            }
        },
        {
            'url': 'https://store.tildaapi.pro/api/getproductslist/?storepartuid=108952566671&recid=727992541&c=1717451675769&slice=2&getparts=true&size=3',
            'headers': {
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate, br, zstd',
                'Accept-Language': 'ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7',
                'Dnt': '1',
                'Origin': 'https://quizyasha.kz',
                'Referer': 'https://quizyasha.kz/',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'cross-site',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'
            }
        }
    ]

    # Регулярное выражение для поиска даты в названии
    date_pattern = re.compile(r'(\d{1,2}\s[а-яА-Я]+)')

    # Список для хранения информации о мероприятиях
    events_info = []

    def fetch_data(url, headers):
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return json.loads(response.content.decode('utf-8'))
        else:
            print(f'Ошибка доступа: статус код {response.status_code} для URL {url}')
            return None

    def process_data(data):
        for product in data.get('products', []):
            # Полное название мероприятия
            event_name_full = product.get('title', '')

            # Извлечение даты из полного названия
            date_match = date_pattern.search(event_name_full)
            event_date = date_match.group(0)

            # Обрезаем название по символу "|"
            event_name = event_name_full.split('|')[0].strip()

            # Сохранение информации из каждого издания
            for edition in product.get('editions', []):
                event_location = edition.get('МЕСТО ПРОВЕДЕНИЯ').replace('\u200b', '')
                event_location = event_location[:event_location.find(',')]
                event_time = edition.get('НАЧАЛО').replace('\u200b', '')

                # Добавляем информацию в список словарей
                date_ = event_date.replace('\u200b', '')
                date = convert_date(str(date_))

                events_info.append({
                    "date": date,
                    "title": event_name.replace('\u200b', ''),
                    "place": str(event_location).replace('`', "'"),
                    "time": event_time
                })

    for req in requests_data:
        data = fetch_data(req['url'], req['headers'])
        if data:
            process_data(data)
    return events_info

def get_wowquiz():
    url = 'https://almaty.wowquiz.ru/schedule'

    # Отправка GET-запроса для получения страницы
    response = requests.get(url)

    if response.status_code == 200:  # Проверка статуса ответа, должен быть 200 для успешного запроса

        # Парсинг страницы с использованием BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Поиск всех блоков с информацией о мероприятиях
        events = soup.find_all('div', class_='game-column')

        # Список для хранения информации о мероприятиях
        events_info = []

        for event in events:
            date_ = event.find('span', class_='date').text.strip()
            title = event.find('div', class_='game-item__title').text.strip()
            place = event.find('span', class_='place').text.strip()
            time = event.find('span', class_='time').text.strip()

            date = convert_date(date_)

            events_info.append({
                "date": date,
                "title": title,
                "place": str(place).replace('`', "'"),
                "time": time
            })
    return events_info


def convert_date(date_str):
    months = {
        'января': '01',
        'февраля': '02',
        'марта': '03',
        'апреля': '04',
        'мая': '05',
        'июня': '06',
        'июля': '07',
        'августа': '08',
        'сентября': '09',
        'октября': '10',
        'ноября': '11',
        'декабря': '12'
    }
    day, month_name = date_str.split()
    month = months[(month_name).lower()]
    year = "2024"
    return f"{year}-{month}-{int(day):02d}"


def parse_event(line):
    match = re.match(r"– (.*?) \[(.*?)\] - (\d{2}:\d{2}), (.*)", line)
    if match:
        quiz_name = match.group(1)
        quiz_title = match.group(2)
        quiz_time = match.group(3)
        quiz_place = match.group(4)
        return f"{quiz_name}:{quiz_title}:{quiz_place}/{quiz_time}"
    return None


def clean_input_data(data):
    # Удаляем начальные и конечные пробелы, разбиваем текст на строки
    lines = data.strip().splitlines()
    # Убираем начальные пробелы у каждой строки
    cleaned_lines = [line.strip() for line in lines]
    # Объединяем строки обратно в один текстовый блок
    cleaned_data = "\n".join(cleaned_lines)
    return cleaned_data


def parse_schedule(data):
    schedule = defaultdict(dict)
    current_date = None

    for line in data.strip().split('\n'):
        if re.match(r"^\d{2} \w+", line):
            date_str = line.split()[0] + " " + line.split()[1]
            current_date = convert_date(date_str)

        elif current_date:
            event = parse_event(line)
            if event:
                if current_date not in schedule:
                    schedule[current_date] = {}
                schedule[current_date][event.split(':')[0].strip()] = event

    return schedule