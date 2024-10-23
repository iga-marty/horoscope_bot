import os
import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from dotenv import load_dotenv

import kb

load_dotenv()
logging.basicConfig(level=logging.INFO)

token = os.environ.get('TOKEN')
bot = Bot(token=token)
dp = Dispatcher()


@dp.message(Command('start'))
async def start(msg: types.Message):
    await msg.delete()
    await msg.answer(text='Выберите свой знак зодиака:', reply_markup=kb.menu)


async def pprr(chat_id):
    await bot.send_message(chat_id, ':gemini:')


pprr(260143685)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
