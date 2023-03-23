from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import types

# main_search = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('🔍 Поиск ПК'),
#                                                            KeyboardButton('🔍 Поиск PS'))
main_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton('Мой профиль', callback_data='My profile'),
    InlineKeyboardButton('Поиск товара', callback_data='Поиск товара')]
])
main_menu.add(types.InlineKeyboardButton('Мои\nПредзаказы', callback_data='My-pre-orders'),
          types.InlineKeyboardButton('Предзаказы', callback_data='Preorders'))

main_menu.add(types.InlineKeyboardButton('Покупка', callback_data='Buying'))


search_products = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton('Игровые ПК', callback_data='GamingPC'),
    InlineKeyboardButton('Игровые консоли', callback_data='Concole_Gaming')]
])

main_back = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('Назад'))