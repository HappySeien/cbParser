import requests
import fake_useragent
import csv
import time
from bs4 import BeautifulSoup


URL = 'https://cbr.ru/currency_base/daily/'
user_agent = fake_useragent.UserAgent().random  # Имитация браузера
HEADERS = {'User-Agent': user_agent}
CSV = 'currency.csv'


def get_html(url, headers=HEADERS, params=None):
    """Запрос к серверу"""
    response = requests.get(url, headers=HEADERS, params=params)
    response.close()  # Закрывааем соединение
    return response


def get_content(html_):
    """Получение контента из ответа сервера"""
    soup = BeautifulSoup(html_, 'html.parser')
    items = soup.find_all('tr')  # Получаем список всех тегов tr со страницы
    currency = []

    for item in items[1:]:
        itm = item.find_all('td')  # Получаем список тегов td из тега tr
        currency.append(
            {
                'Цифр.код': itm[0].get_text(),
                'Букв.код': itm[1].get_text(),
                'Единиц': itm[2].get_text(),
                'Валюта': itm[3].get_text(),
                'Курс': itm[4].get_text()
            }
        )
    return currency


def save_data(data, path):
    """Запись таблицы в файл"""
    with open(path, 'w', newline='') as f:
        writer = csv.writer(f, delimiter= ';')
        writer.writerow(['Цифр.код', 'Букв.код', 'Единиц', 'Валюта', 'Курс'])
        for i in data:
            writer.writerow(
                [i['Цифр.код'], i['Букв.код'], i['Единиц'],
                 i['Валюта'], i['Курс']]
            )


def parser():
    """Узловая функция, парсит данные сервера и сохраняет их в csv"""
    html_ = get_html(URL)
    if html_.status_code == 200:
        print('conection OK')
        time.sleep(1)
        print('Получаем данные о валютах')
        currency_ = get_content(html_.text)
        time.sleep(1)
        print('Данные получены')
        time.sleep(1)
        print('Записываем данные в файл')
        save_data(currency_, CSV)
        time.sleep(1)
        print('Данные записаны в файл currency.csv')
    else:
        print('Error conection ', html_)

parser()
print('Parsing finish, press ENTER to close window')
input()
