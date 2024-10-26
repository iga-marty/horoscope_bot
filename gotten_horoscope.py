# TODO
# Вместо поиска подходящего API или объединения гороскопов c нескольких порталов, было принято решение использовать
# гороскопы <yesterday>, <tomorrow>, <tomorrow02> из xml-файла как вариации сегодняшнего (кнопка бота "Обновить").
# Займусь, если останется время.


import requests
import re

text_xml = requests.get('https://ignio.com/r/export/utf/xml/daily/com.xml').text

signs = ('aries', 'taurus', 'gemini', 'cancer',
         'leo', 'virgo', 'libra', 'scorpio',
         'sagittarius', 'capricorn', 'aquarius', 'pisces')

today_horo = {sign: (
    re.search(fr'<{sign}>.+<yesterday>\n(.+)\n</yesterday>.+</{sign}>', text_xml, re.S).group(1),
    re.search(fr'<{sign}>.+<today>\n(.+)\n</today>.+</{sign}>', text_xml, re.S).group(1),
    re.search(fr'<{sign}>.+<tomorrow>\n(.+)\n</tomorrow>.+</{sign}>', text_xml, re.S).group(1),
    re.search(fr'<{sign}>.+<tomorrow02>\n(.+)\n</tomorrow02>.+</{sign}>', text_xml, re.S).group(1)
        ) for sign in signs}
