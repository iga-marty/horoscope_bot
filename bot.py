import os
import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from dotenv import load_dotenv


load_dotenv()
logging.basicConfig(level=logging.INFO)

token = os.environ.get('TOKEN')
bot = Bot(token=token)
