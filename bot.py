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
    def needed_horo(sign):
        number = int(msg.text[0])
        if not number:
            number = 3
        else:
            number -= 1
        print(number)
        return today_horoscope[sign][number][1::]

    sign_name = sign_names[msg.text]
    db.change_sign(msg.chat.id, sign_name)
    personal_horoscope = needed_horo(sign_name)
    today = date.today()
    await msg.answer(text=f'<b>{today.day}.{today.month}.{today.year}</b>\n' + personal_horoscope,
                     reply_markup=kb.refresh_button(sign_name), parse_mode='html')


@dp.message(F.text)
async def trash_recognition(msg: types.Message):
    await msg.answer(text='Извините, я не понял')


@dp.callback_query(F.data)
async def get_xml_horoscope(call: types.CallbackQuery):
    sign_name = call.data
    personal_horoscope = gotten_horoscope.today_horo[sign_name]
    today = date.today()
    if call.message.text.startswith(f'{today.day}'):
        await call.answer(text='Завтра еще не наступило!')
    else:
        await call.message.edit_text(text=f'<b>{today.day}.{today.month}.{today.year}</b>\n' + personal_horoscope,
                                     reply_markup=kb.refresh_button(sign_name), parse_mode='html')

    # await bot.send_message(chat_id=call.message.chat.id,
    #                        text=f'<b>{today.day}.{today.month}.{today.year}</b>\n' + personal_horoscope,
    #                        reply_markup=kb.refresh_button(sign_name), parse_mode='html')
    # await call.message.delete()


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
