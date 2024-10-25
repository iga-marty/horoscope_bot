import requests
import re

text_xml = requests.get('https://ignio.com/r/export/utf/xml/daily/com.xml').text
signs = ('aries', 'taurus', 'gemini', 'cancer',
         'leo', 'virgo', 'libra', 'scorpio',
         'sagittarius', 'capricorn', 'aquarius', 'pisces')

today_horo = {sign: re.search(fr'<{sign}>.+<today>\n(.+)\n</today>.+</{sign}>', text_xml, re.S).group(1)
              for sign in signs}
