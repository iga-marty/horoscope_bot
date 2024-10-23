from aiogram.utils.keyboard import InlineKeyboardBuilder

zodiac = {'Овен': '\u2648', 'Телец': '\u2649', 'Близнецы': '\u264A', 'Рак': '\u264B',
          'Лев': '\u264C', 'Дева': '\u264D', 'Весы': '\u264E', 'Скорпион': '\u264F',
          'Стрелец': '\u2650', 'Козерог': '\u2651', 'Водолей': '\u2652', 'Рыбы': '\u2653'}

menu = InlineKeyboardBuilder()
for key, value in zodiac.items():
    menu.button(text=value, callback_data=key)
menu.adjust(4)
menu = menu.as_markup()
