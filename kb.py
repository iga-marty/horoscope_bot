from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

# zodiac = {'Овен': '\u2648', 'Телец': '\u2649', 'Близнецы': '\u264A', 'Рак': '\u264B',
#           'Лев': '\u264C', 'Дева': '\u264D', 'Весы': '\u264E', 'Скорпион': '\u264F',
#           'Стрелец': '\u2650', 'Козерог': '\u2651', 'Водолей': '\u2652', 'Рыбы': '\u2653'}

zodiac = (('\u2648', '\u2649', '\u264A', '\u264B'),
          ('\u264C', '\u264D', '\u264E', '\u264F'),
          ('\u2650', '\u2651', '\u2652', '\u2653'))

buttons = [[KeyboardButton(text=sign) for sign in row] for row in zodiac]
menu = ReplyKeyboardMarkup(keyboard=buttons)