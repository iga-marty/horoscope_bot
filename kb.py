from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

zodiac = (('\u2648', '\u2649', '\u264A', '\u264B'),
          ('\u264C', '\u264D', '\u264E', '\u264F'),
          ('\u2650', '\u2651', '\u2652', '\u2653'))

buttons = [[KeyboardButton(text=sign) for sign in row] for row in zodiac]
menu = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True, one_time_keyboard=True)
