import requests
import re

text_xml = requests.get('https://ignio.com/r/export/utf/xml/daily/com.xml').text
today_horo = {'aries': '\u2648', 'taurus': '\u2649', 'gemini': '\u264A', 'cancer': '\u264B',
              'leo': '\u264C', 'virgo': '\u264D', 'libra': '\u264E', 'scorpio': '\u264F',
              'sagittarius': '\u2650', 'capricorn': '\u2651', 'aquarius': '\u2652', 'pisces': '\u2653'}

for sign in today_horo.keys():
    result = re.search(r'<{}>.+<today>\n(.+)\n</today>'.format(sign), text_xml, re.S)
    sign_horoscope = result.group(1)

print(today_horo)
