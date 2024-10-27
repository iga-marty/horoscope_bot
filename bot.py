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
    '♈': 'https://i.artfile.me/wallpaper/04-09-2019/640x480/raznoe-znaki-zodiaka-zodiak-1478062.jpg',
    '♉': 'https://i.artfile.me/wallpaper/04-09-2019/640x480/raznoe-znaki-zodiaka-zodiak-1478069.jpg',
    '♊': 'https://i.artfile.me/wallpaper/04-09-2019/640x480/raznoe-znaki-zodiaka-zodiak-1478068.jpg',
    '♋': 'https://i.artfile.me/wallpaper/04-09-2019/640x480/raznoe-znaki-zodiaka-zodiak-1478070.jpg',
    '♌': 'https://i.artfile.me/wallpaper/04-09-2019/640x480/raznoe-znaki-zodiaka-zodiak-1478071.jpg',
    '♍': 'https://i.artfile.me/wallpaper/04-09-2019/640x480/raznoe-znaki-zodiaka-zodiak-1478072.jpg',
    '♎': 'https://i.artfile.me/wallpaper/04-09-2019/640x480/raznoe-znaki-zodiaka-zodiak-1478075.jpg',
    '♏': 'https://i.artfile.me/wallpaper/04-09-2019/640x480/raznoe-znaki-zodiaka-zodiak-1478074.jpg',
    '♐': 'https://i.artfile.me/wallpaper/04-09-2019/640x480/raznoe-znaki-zodiaka-zodiak-1478073.jpg',
    '♑': 'https://i.artfile.me/wallpaper/04-09-2019/640x480/raznoe-znaki-zodiaka-zodiak-1478063.jpg',
    '♒': 'https://i.artfile.me/wallpaper/04-09-2019/640x480/raznoe-znaki-zodiaka-zodiak-1478076.jpg',
    '♓': 'https://i.artfile.me/wallpaper/04-09-2019/640x480/raznoe-znaki-zodiaka-zodiak-1478077.jpg'
}

today_horoscope = dict(gotten_horoscope.today_horo)


@dp.message(Command('start'))
@dp.message(Command('change_zodiac'))
async def start(msg: Message):
    await msg.delete()
    db.create_user(msg.chat.id)
    await msg.answer(text='Выберите свой знак зодиака:', reply_markup=kb.menu)


@dp.message(lambda query: query.text in sign_names.keys())
async def get_horoscope(msg: Message):
    sign_name, chat_id = msg.text, msg.chat.id
    db.change_sign(chat_id, sign_name)
    horoscope_number = 0
    db.change_number(chat_id, horoscope_number)
    personal_horoscope = today_horoscope[sign_name][horoscope_number]
    today = date.today()
    last_message = await bot.send_photo(chat_id=chat_id,
                                        photo=sign_names[sign_name],
                                        caption=f'<b>{today.day}.{today.month}.{today.year}</b>\n' + personal_horoscope,
                                        reply_markup=kb.update_button(sign_name))
    db.change_last_message_id(last_message.chat.id, last_message.message_id)


async def update_horoscope(chat_id, sign_name):
    horoscope_number = db.get_number(chat_id)  # костыль: номер гороскопа меняется через базу
    db.change_number(chat_id, horoscope_number)  # в этих двух строчках
    personal_horoscope = today_horoscope[sign_name][horoscope_number]
    today = date.today()
    caption = f'<b>{today.day}.{today.month}.{today.year}</b>\n' + personal_horoscope
    last_message = db.get_last_message_id(chat_id)

    await bot.edit_message_media(InputMediaPhoto(media=sign_names[sign_name], caption=caption),
                                 chat_id=chat_id, message_id=last_message,
                                 reply_markup=kb.update_button(sign_name))


@dp.callback_query(F.data)
async def update(call: CallbackQuery):
    sign_name, chat_id = call.data, call.message.chat.id
    await update_horoscope(chat_id, sign_name)


@dp.message(Command('update'))
async def update(msg: Message):
    chat_id = msg.chat.id
    sign_name = db.get_sign(chat_id)
    await update_horoscope(chat_id, sign_name)
    await msg.delete()


@dp.message(Command('clear_history'))
async def clear_history(msg: Message):
    await msg.delete()


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
