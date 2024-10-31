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
from aiogram.exceptions import TelegramBadRequest
from dotenv import load_dotenv
from apscheduler.schedulers.asyncio import AsyncIOScheduler

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


@dp.message(Command('start'))
@dp.message(Command('change_zodiac'))
async def start(msg: Message):
    await msg.delete()
    db.create_user(msg.chat.id)
    message = await msg.answer(text='Выберите свой знак зодиака:', reply_markup=kb.menu)
    db.add_message(message.message_id, msg.chat.id)


async def send_and_save_message(today, chat_id, sign_name, personal_horoscope):
    last_message = await bot.send_photo(chat_id=chat_id,
                                        photo=sign_names[sign_name],
                                        caption=f'<b>{today.day}.{today.month}.{today.year}</b>\n' + personal_horoscope,
                                        reply_markup=kb.update_button(sign_name))
    db.change_last_message_id(chat_id, last_message.message_id)
    db.add_message(last_message.message_id, chat_id)


@dp.message(lambda query: query.text in sign_names.keys())
async def get_horoscope(msg: Message):
    sign_name, chat_id = msg.text, msg.chat.id
    db.add_message(msg.message_id, chat_id)
    db.change_sign(chat_id, sign_name)
    horoscope_number = 0
    db.change_number(chat_id, horoscope_number)
    personal_horoscope = db.get_horoscope(sign_name, horoscope_number)
    today = date.today()
    await send_and_save_message(today, chat_id, sign_name, personal_horoscope)


async def update_horoscope(chat_id, sign_name):
    horoscope_number = db.get_number(chat_id)
    db.change_number(chat_id, horoscope_number)
    personal_horoscope = db.get_horoscope(sign_name, horoscope_number)
    today = date.today()
    caption = f'<b>{today.day}.{today.month}.{today.year}</b>\n' + personal_horoscope
    last_message = db.get_last_message_id(chat_id)
    try:
        await bot.edit_message_media(InputMediaPhoto(media=sign_names[sign_name], caption=caption),
                                     chat_id=chat_id, message_id=last_message,
                                     reply_markup=kb.update_button(sign_name))
    except TelegramBadRequest:
        await send_and_save_message(today, chat_id, sign_name, personal_horoscope)


@dp.callback_query(F.data)
async def update_call(call: CallbackQuery):
    sign_name, chat_id = call.data, call.message.chat.id
    await update_horoscope(chat_id, sign_name)


@dp.message(Command('update'))
async def update_msg(msg: Message):
    await msg.delete()
    chat_id = msg.chat.id
    sign_name = db.get_sign(chat_id)
    await update_horoscope(chat_id, sign_name)


@dp.message(Command('clear_history'))
async def clear_history(msg: Message):
    await msg.delete()
    chat_id = msg.chat.id
    last_message = db.get_last_message_id(chat_id)
    id_list = db.get_messages(chat_id)
    id_list.remove(last_message)
    await bot.delete_messages(chat_id, id_list)
    db.delete_user_messages(chat_id)


@dp.message(F.text)
async def trash_recognition(msg: Message):
    await msg.delete()
    message = await msg.answer(text='Извините, я не понял')
    db.add_message(message.message_id, msg.chat.id)


async def main_menu():
    main_menu_commands = [
        BotCommand(command='/change_zodiac', description='Выбрать знак зодиака'),
        BotCommand(command='/update', description='Обновить гороскоп'),
        BotCommand(command='/clear_history', description='Очистить историю'),
    ]
    await bot.set_my_commands(main_menu_commands)


async def update_daily_horo():
    db.create_or_update_horo_base(gotten_horoscope.horoscopes())


async def daily_notifications():
    await update_daily_horo()
    notifications_data = db.get_data_for_notifications()
    if not len(notifications_data) - 1:
        for chat_id, sign in notifications_data.items():
            await update_horoscope(chat_id, sign)
    else:
        chat_id, sign = list(notifications_data.items())[0]
        await update_horoscope(chat_id, sign)


async def main():
    await main_menu()
    await update_daily_horo()

    scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
    scheduler.add_job(daily_notifications, 'cron', hour=10)
    scheduler.start()

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
