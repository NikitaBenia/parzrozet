import keyboards
from aiogram import types, executor, Dispatcher, Bot
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import requests
from bs4 import BeautifulSoup
from keyboards import main_menu, main_back
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from dotenv import dotenv_values
import asyncio

storage = MemoryStorage()

config = dotenv_values('.env')
bot = Bot(config['key'])
dp = Dispatcher(bot, storage=storage)

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await bot.send_message(message.chat.id, message.from_user.first_name + " Привет")
    await asyncio.sleep(2)
    await bot.send_message(message.chat.id, 'Я бот для поиска товаров с сайта розетка.')
    await asyncio.sleep(2)
    await message.answer('Главное меню', reply_markup=keyboards.main_menu)

@dp.callback_query_handler(lambda c: c.data == 'Поиск товара')
async def search_products(callback: types.CallbackQuery):
    await callback.message.answer('Выберите товар', reply_markup=keyboards.search_products)

@dp.callback_query_handler(lambda c: c.data =='GamingPC')
async def search_computer(callback: types.CallbackQuery):
    await storage.set_state(chat=callback.from_user.id, state='chek') # обработка следуещего сообщения
    await storage.update_data(chat=callback.from_user.id, data={'console_gaming': True})
    await callback.message.answer('Начинаю парсинг', reply_markup=keyboards.main_back)
    url = "https://hard.rozetka.com.ua/computers/c80095/"
    req = requests.get(url)

    soup = BeautifulSoup(req.text, 'html.parser')
    page_count = int(soup.find('div', class_='pagination').find_all('a', class_='pagination__link')[-1].text.strip())
    print(f'Всего страниц {page_count}')
    for page in range(1, page_count + 1):
        print(f'[INFO] Всего страниц {page}')
        url = f'https://hard.rozetka.com.ua/computers/c80095/page={page}'
        req = requests.get(url)
        soup = BeautifulSoup(req.text, 'html.parser')
        l = soup.select('.goods-tile__inner')
        for item in l:
            data = await storage.get_data(chat=callback.from_user.id)
            if not data.get('console_gaming'):
                await callback.message.answer('Выберите товар', reply_markup=keyboards.search_products)
                return
            title = item.find('a', class_='goods-tile__heading').text.strip()
            link = item.find('a', class_='goods-tile__heading').get('href').strip()
            price = item.select('.goods-tile__price-value')[0].text.strip()
            nalichie = item.select('.goods-tile__availability')[0].text.strip()
            img = item.find('a', class_='goods-tile__picture').find('img')
            img = img['src']
            await asyncio.sleep(3)
            await bot.send_message(callback.message.chat.id,
            "<b>" + title + "</b>\n<i>" + "<b>" + nalichie + "</b>\n" + price + f"</i>\n<a href='{link}'>Ссылка на сайт</a>",
            parse_mode='HTML')

@dp.message_handler(state='chek')
async def stop_parsing(message: types.Message, state):
    if message.text == "Назад":
        await state.update_data({'console_gaming': False})
        await state.finish()

@dp.callback_query_handler(lambda c: c.data == 'Concole_Gaming')
async def search_playstation(callback: types.CallbackQuery):
    await storage.set_state(chat=callback.from_user.id, state='chekPS')  # обработка следуещего сообщения
    await storage.update_data(chat=callback.from_user.id, data={'gaming_pc': True})
    await callback.message.answer('Начинаю парсинг', reply_markup=keyboards.main_back)
    url = "https://rozetka.com.ua/consoles/c80020/"
    req = requests.get(url)

    soup = BeautifulSoup(req.text, 'html.parser')
    page_countPS = int(soup.find('div', class_='pagination').find_all('a', class_='pagination__link')[-1].text.strip())
    print(f'Всего страниц {page_countPS}')
    for pageone in range(1, page_countPS + 1):
        print(f'[INFO] Всего страниц {pageone}')
        urlone = f'https://rozetka.com.ua/consoles/c80020/page={pageone}'
        reqPS = requests.get(urlone)
        soupone = BeautifulSoup(reqPS.text, 'html.parser')
        lone = soup.select('.goods-tile__inner')
        for itemPS in lone:
            data = await storage.get_data(chat=callback.from_user.id)
            if not data.get('gaming_pc'):
                await callback.message.answer('Выберите товар', reply_markup=keyboards.search_products)
                return
            titlePS = itemPS.find('a', class_='goods-tile__heading').text.strip()
            linkPS = itemPS.find('a', class_='goods-tile__heading').get('href').strip()
            pricePS = itemPS.select('.goods-tile__price-value')[0].text.strip()
            nalichiePS = itemPS.select('.goods-tile__availability')[0].text.strip()
            imgPS = itemPS.find('a', class_='goods-tile__picture').find('img')
            imgPS = imgPS['src']
            await asyncio.sleep(3)
            await bot.send_message(callback.message.chat.id,
                                   "<b>" + titlePS + "</b>\n<i>" + "<b>" + nalichiePS + "</b>\n" + pricePS + f"</i>\n<a href='{linkPS}'>Ссылка на сайт</a>",
                                   parse_mode='HTML')

@dp.message_handler(state='chekPS')
async def stop_parsing(message: types.Message, state):
    if message.text == "Назад":
        await state.update_data({'gaming_pc': False})
        await state.finish()
#
executor.start_polling(dp)