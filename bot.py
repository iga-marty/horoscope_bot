import os
import asyncio
import logging
from datetime import date

from aiogram import F, Bot, Dispatcher
from aiogram.types import Message, CallbackQuery, BotCommand
from aiogram.types.input_media_photo import InputMediaPhoto
from aiogram.filters.command import Command
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from dotenv import load_dotenv

import db
import kb
import gotten_horoscope

load_dotenv()
logging.basicConfig(level=logging.INFO)

token = os.environ.get('TOKEN')
bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

sign_names = {
    '♈': ('aries', 'https://i.artfile.me/wallpaper/04-09-2019/640x480/raznoe-znaki-zodiaka-zodiak-1478062.jpg'),
    '♉': ('taurus', 'https://i.artfile.me/wallpaper/04-09-2019/640x480/raznoe-znaki-zodiaka-zodiak-1478069.jpg'),
    '♊': ('gemini', 'https://i.artfile.me/wallpaper/04-09-2019/640x480/raznoe-znaki-zodiaka-zodiak-1478068.jpg'),
    '♋': ('cancer', 'https://i.artfile.me/wallpaper/04-09-2019/640x480/raznoe-znaki-zodiaka-zodiak-1478070.jpg'),
    '♌': ('leo', 'https://i.artfile.me/wallpaper/04-09-2019/640x480/raznoe-znaki-zodiaka-zodiak-1478071.jpg'),
    '♍': ('virgo', 'https://i.artfile.me/wallpaper/04-09-2019/640x480/raznoe-znaki-zodiaka-zodiak-1478072.jpg'),
    '♎': ('libra', 'https://i.artfile.me/wallpaper/04-09-2019/640x480/raznoe-znaki-zodiaka-zodiak-1478075.jpg'),
    '♏': ('scorpio', 'https://i.artfile.me/wallpaper/04-09-2019/640x480/raznoe-znaki-zodiaka-zodiak-1478074.jpg'),
    '♐': ('sagittarius', 'https://i.artfile.me/wallpaper/04-09-2019/640x480/raznoe-znaki-zodiaka-zodiak-1478073.jpg'),
    '♑': ('capricorn', 'https://i.artfile.me/wallpaper/04-09-2019/640x480/raznoe-znaki-zodiaka-zodiak-1478063.jpg'),
    '♒': ('aquarius', 'https://i.artfile.me/wallpaper/04-09-2019/640x480/raznoe-znaki-zodiaka-zodiak-1478076.jpg'),
    '♓': ('pisces', 'https://i.artfile.me/wallpaper/04-09-2019/640x480/raznoe-znaki-zodiaka-zodiak-1478077.jpg')
}

today_horoscope = dict(gotten_horoscope.today_horo)


@dp.message(Command('start'))
@dp.message(Command('change_zodiac'))
async def start(msg: Message):
    # await msg.delete()
    db.create_user(msg.chat.id)
    await msg.answer(text='Выберите свой знак зодиака:', reply_markup=kb.menu)


@dp.message(lambda query: query.text in sign_names.keys())
async def get_horoscope(msg: Message):
    sign_name = sign_names[msg.text][0]
    db.change_sign(msg.chat.id, sign_name)
    personal_horoscope = today_horoscope[sign_name][0]
    today = date.today()
    await bot.send_photo(chat_id=msg.chat.id,
                         photo=sign_names[msg.text][1],
                         caption=f'<b>{today.day}.{today.month}.{today.year}</b>\n' + personal_horoscope,
                         reply_markup=kb.update_button(sign_name, msg.text, 0))


@dp.callback_query(F.data)
async def update(call: CallbackQuery):
    sign_name, sign, fragment = call.data.split(' ')
    personal_horoscope = today_horoscope[sign_name][int(fragment)]
    today = date.today()
    caption = f'<b>{today.day}.{today.month}.{today.year}</b>\n' + personal_horoscope
    await call.message.edit_media(InputMediaPhoto(media=sign_names[sign][1], caption=caption),
                                  reply_markup=kb.update_button(sign_name, sign, int(fragment)))


@dp.message(Command('clear_history'))
async def clear_history():
    pass


@dp.message(F.text)
async def trash_recognition(msg: Message):
    await msg.answer(text='Извините, я не понял')


async def main_menu():
    main_menu_commands = [
        BotCommand(command='/change_zodiac', description='Выбрать знак зодиака'),
        BotCommand(command='/update', description='Обновить гороскоп'),
        BotCommand(command='/clear_history', description='Очистить историю'),
    ]
    await bot.set_my_commands(main_menu_commands)


async def main():
    await main_menu()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
