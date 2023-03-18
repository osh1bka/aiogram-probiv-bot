# Автор https://t.me/osh1script

from aiogram import Bot, types, asyncio
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import sqlite3 as sql
from aiogram.utils.exceptions import Throttled
from aiogram.dispatcher.filters import BoundFilter
import requests
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import random
from aiogram.dispatcher import FSMContext                            
from aiogram.dispatcher.filters import Command                     
from aiogram.contrib.fsm_storage.memory import MemoryStorage        
from aiogram.dispatcher.filters.state import StatesGroup, State 
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import urllib.request
import json

from dadata import DadataAsync

oken = "5272716245:AAFVfC9OySn96H81wFogut7qbwEmLOfsolA" # токен бота тг

# Автор https://t.me/osh1script

token = "9cda453c6c4f7bb972863ded663849826d9b834c" # получать на dadata
secret = "bf035e448d7b655df28c7043dc91b5a6bf097db7" # получать на dadata
dadata = DadataAsync(token, secret)

# Автор https://t.me/osh1script

bot = Bot(token=oken)
dp = Dispatcher(bot, storage=MemoryStorage())

# Автор https://t.me/osh1script

class meinfo(StatesGroup):
	Q3 = State()
	Q2 = State()

@dp.message_handler(commands=['start'])
async def start(message):
	await message.answer('Привет, я помогу найти информацию о номере телефона/ip\n\nДля пробива по номеру введите /number\nДля пробива по IP введите /ip\n\nАвтор - https://t.me/osh1script')

@dp.message_handler(content_types=['text'])
async def get_message(message):
	if message.text == "/number":           
		await message.answer("Введите номер телефона")
		await meinfo.Q3.set()
	if message.text == "/ip":             
		await message.answer("Введите IP адрес")
		await meinfo.Q2.set()

# Автор https://t.me/osh1script

@dp.message_handler(state=meinfo.Q3)
async def answer_q3(message: types.Message, state: FSMContext):
	answer = message.text
	await state.update_data(answer3=answer)
	data = await state.get_data()                #
	answer3 = data.get("answer3")
	result = await dadata.clean("phone", answer3)
	cont = InlineKeyboardMarkup(row_width=2)
	wh = InlineKeyboardButton("✅ WhatsApp", url=f"""wa.me/{result["phone"]}""")
	ch = InlineKeyboardButton("✅ Канал прогера", url=f"https://t.me/osh1script")
	cont.add(wh, ch)

	await bot.send_message(message.from_user.id, f"""📱 Телефон: {result["number"]}
🏬 Страна: {result["country"]}
🏠 Регион: {result["region"]}
🏭 Город: {result["city"]}
🕗 Часовой пояс: {result["timezone"]}
📶 Оператор: {result["provider"]}""", reply_markup=cont)
 
	await state.finish()

@dp.message_handler(state=meinfo.Q2)
async def answer_q2(message: types.Message, state: FSMContext):
	answer = message.text
	await state.update_data(answer2=answer)
	data = await state.get_data()                #
	ip = data.get("answer2")
	url = f'https://ipapi.co/{ip}/json/'
	json = requests.get(url).json()
	await message.reply(f'Город: {json["city"]}\nРегион: {json["region"]}\nСтрана: {json["country_name"]}\nВалюта: {json["currency"]}\nНаселение страны: {json["country_population"]}\nПровайдер: {json["org"]}')
	await state.finish()

# Автор https://t.me/osh1script

if __name__ == "__main__":
	executor.start_polling(dp, skip_updates=True)   
