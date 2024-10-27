# Вместо поиска подходящего API или объединения гороскопов c нескольких порталов, было принято решение использовать
# гороскопы <yesterday>, <tomorrow>, <tomorrow02> из xml-файла как вариации сегодняшнего (кнопка бота "Обновить").


import requests
import re
from datetime import datetime


def horoscopes() -> dict:
    print(3, datetime.now(), 'запрос, регулярки')
    text_xml = requests.get('https://ignio.com/r/export/utf/xml/daily/com.xml').text

    signs = {'aries': '♈', 'taurus': '♉', 'gemini': '♊', 'cancer': '♋',
             'leo': '♌', 'virgo': '♍', 'libra': '♎', 'scorpio': '♏',
             'sagittarius': '♐', 'capricorn': '♑', 'aquarius': '♒', 'pisces': '♓'}

    today_horo = {sign_smiley: (
        re.search(fr'<{sign_name}>.+<yesterday>\n(.+)\n</yesterday>.+</{sign_name}>', text_xml, re.S).group(1),
        re.search(fr'<{sign_name}>.+<today>\n(.+)\n</today>.+</{sign_name}>', text_xml, re.S).group(1),
        re.search(fr'<{sign_name}>.+<tomorrow>\n(.+)\n</tomorrow>.+</{sign_name}>', text_xml, re.S).group(1),
        re.search(fr'<{sign_name}>.+<tomorrow02>\n(.+)\n</tomorrow02>.+</{sign_name}>', text_xml, re.S).group(1)
    ) for sign_name, sign_smiley in signs.items()}

    return today_horo
