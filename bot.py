import os
import asyncio
import logging

from aiogram import F, Bot, Dispatcher, types
from aiogram.filters.command import Command
from dotenv import load_dotenv

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
        await msg.answer(text=personal_horoscope)
    except KeyError:
        await msg.answer(text='Неверная команда')
        await start(msg)


async def get_xml_horoscope():
    pass


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
