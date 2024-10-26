import os
import asyncio
import logging
from datetime import date

from aiogram import F, Bot, Dispatcher, types
from aiogram.filters.command import Command
from dotenv import load_dotenv

import db
import kb
import gotten_horoscope

load_dotenv()
logging.basicConfig(level=logging.INFO)

token = os.environ.get('TOKEN')
bot = Bot(token=token)
dp = Dispatcher()

sign_names = {'♈': 'aries', '♉': 'taurus', '♊': 'gemini', '♋': 'cancer',
              '♌': 'leo', '♍': 'virgo', '♎': 'libra', '♏': 'scorpio',
              '♐': 'sagittarius', '♑': 'capricorn', '♒': 'aquarius', '♓': 'pisces'}

commands = ('/start',)

today_horoscope = dict(gotten_horoscope.today_horo)

@dp.message(Command('start'))
async def start(msg: types.Message):
    # await msg.delete()
    db.create_user(msg.chat.id)
    await msg.answer(text='Выберите свой знак зодиака:', reply_markup=kb.menu)


@dp.message(lambda query: query.text in sign_names.keys())
async def get_horoscope(msg: types.Message):
    sign_name = sign_names[msg.text]
    db.change_sign(msg.chat.id, sign_name)
    personal_horoscope = today_horoscope[sign_name][0]
    today = date.today()
    await msg.answer(text=f'<b>{today.day}.{today.month}.{today.year}</b>\n' + personal_horoscope,
                     reply_markup=kb.refresh_button(sign_name, 0), parse_mode='html')


@dp.message(F.text)
async def trash_recognition(msg: types.Message):
    await msg.answer(text='Извините, я не понял')


@dp.callback_query(F.data)
async def get_xml_horoscope(call: types.CallbackQuery):
    sign_name, fragment = call.data.split(' ')
    personal_horoscope = today_horoscope[sign_name][int(fragment)]
    today = date.today()
    await call.message.edit_text(text=f'<b>{today.day}.{today.month}.{today.year}</b>\n' + personal_horoscope,
                                 reply_markup=kb.refresh_button(sign_name, int(fragment)), parse_mode='html')


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
