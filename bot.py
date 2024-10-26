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


@dp.message(Command('start'))
async def start(msg: types.Message):
    # await msg.delete()
    await msg.answer(text='Выберите свой знак зодиака:', reply_markup=kb.menu)


@dp.message(F.text)
async def get_horoscope(msg: types.Message):
    try:
        sign_name = sign_names[msg.text]
        personal_horoscope = gotten_horoscope.today_horo[sign_name]
        if not db.create_user(msg.chat.id, sign_name):
            db.change_sign(msg.chat.id, sign_name)
        today = date.today()
        await msg.answer(text=f'<b>{today.day}.{today.month}.{today.year}</b>\n' + personal_horoscope,
                         reply_markup=kb.refresh_button(sign_name), parse_mode='html')
    except KeyError:
        await msg.answer(text='Неверная команда')
        await start(msg)


@dp.callback_query(F.data)
async def get_xml_horoscope(call: types.CallbackQuery):
    sign_name = call.data
    personal_horoscope = gotten_horoscope.today_horo[sign_name]
    today = date.today()
    await call.message.edit_text(text=f'<b>{today.day}.{today.month}.{today.year}</b>\n' + personal_horoscope,
                                 reply_markup=kb.refresh_button(sign_name), parse_mode='html')


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
