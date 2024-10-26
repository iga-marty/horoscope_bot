from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

zodiac = (('\u2648', '\u2649', '\u264A', '\u264B'),
          ('\u264C', '\u264D', '\u264E', '\u264F'),
          ('\u2650', '\u2651', '\u2652', '\u2653'))

menu_buttons = [[KeyboardButton(text=sign) for sign in row] for row in zodiac]
menu = ReplyKeyboardMarkup(keyboard=menu_buttons, resize_keyboard=True, one_time_keyboard=True)


def refresh_button(sign, fragment):
    if fragment == 3:
        fragment = 0
    else:
        fragment += 1
    button = InlineKeyboardButton(text='Обновить', callback_data=sign + ' ' + str(fragment))
    return InlineKeyboardMarkup(inline_keyboard=[[button]])
