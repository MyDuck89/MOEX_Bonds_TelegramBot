import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from auth_data import token
from data_parser import bond_info


API_TOKEN = token

# Configure logging
logging.basicConfig(level = logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token = API_TOKEN)
dp = Dispatcher(bot)

# Шаблонный Хэндлер вывода первого сообщения
@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """

    
    await message.answer('Для получения информации об облигации, отправьте её код (не ISIN) сообщением боту\n\
По вопросам работоспособности бота пищите @MyDuck89\n\
Мой ' '<a href="https://www.tinkoff.ru/invest/social/profile/MyDuck_89/">профиль в Пульсе</a>',parse_mode="HTML", \
    disable_web_page_preview=True)


# Хэндлер вывода информации по облигации и кнопки-ссылки
@dp.message_handler()
async def bond_information(message: types.Message):

    # Получение кода облигации из сообщения и формирование ссылки
    # для использования парсера
    bond_code = message.text.strip()

    try:
        url = 'https://smart-lab.ru/q/bonds/' + bond_code + '/'
        
        to_answer = bond_info(url)
        
        # Формирование ссылок для кнопок
        get_link_tinkoff = 'https://www.tinkoff.ru/invest/bonds/' + \
            message.text.strip().upper() + '/'
        get_link_bcs = 'https://bcs.ru/markets/bonds/' + \
            message.text.strip().upper() + '/tqob'

        # Вывод в консоль ID пользователя, сделавшего запрос
        # print(message.chat.id)

        # Создание кнопки
        keyboard = InlineKeyboardMarkup()

        button_tinkoff = InlineKeyboardButton('Тинькофф', url = get_link_tinkoff)
        button_bcs = InlineKeyboardButton('БКС', url = get_link_bcs)
        
        keyboard.add(button_tinkoff).insert(button_bcs)

        # Вывод сообщения с информацией по облигации + Инлайн кнопки-ссылки
        await message.answer(to_answer, reply_markup=keyboard)

    # Вывод сообщения об ошибке в случае некорректного ввода информации
    except:
        await message.answer(f'{message.text.strip()} - некорректный ввод.\n\
Возможно введен ISIN вместо кода облигации.')
        # print(message.text.strip(), message.chat.id)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)