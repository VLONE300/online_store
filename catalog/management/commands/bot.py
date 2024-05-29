import asyncio
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram import Router, F
from asgiref.sync import sync_to_async
from django.conf import settings
from django.core.management.base import BaseCommand
from catalog.models import Category, Seller
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext


class SomeState(StatesGroup):
    waiting_for_login = State()
    waiting_for_password = State()


bot = Bot(token=settings.TELEGRAM_API_KEY)

router = Router()
dp = Dispatcher()

button_categories = KeyboardButton(text='Show Categories')
button_sellers = KeyboardButton(text='Show Sellers')
button_show_cart = KeyboardButton(text='Show Cart')
keyboard = ReplyKeyboardMarkup(
    keyboard=[[button_sellers], [button_categories], [button_show_cart]],
    resize_keyboard=True,
    one_time_keyboard=False
)


@sync_to_async
def get_categories():
    return list(Category.objects.all())


@sync_to_async
def get_sellers():
    return list(Seller.objects.all())


async def fetch_user_cart(login, password):
    cart_url = 'http://127.0.0.1:8000/catalog/cart/'
    auth = 'http://127.0.0.1:8000/users/auth/jwt/create'

    async with aiohttp.ClientSession() as session:
        auth_data = {'email': login, 'password': password}
        async with  session.post(auth, json=auth_data) as response:
            if response.status == 200:
                auth_content = await response.json()
                token = auth_content.get('access')

                headers = {'Authorization': f'Baerer {token}'}

                async with session.get(cart_url, headers=headers) as cart_response:
                    cart_content = await cart_response.json()
                    return cart_content
            else:
                return None


@router.message(F.text == '/start')
async def command_start(message: types.Message):
    await message.answer(f'Hello {message.from_user.first_name}!', reply_markup=keyboard)


@router.message(F.text == 'Show Categories')
async def show_categories(message: types.Message):
    categories = await get_categories()
    msg_to_answer = ''
    for category in categories:
        msg_to_answer += (f'Category{category.name}\n'
                          f'Description: {category.description}\n'
                          f'-------------------------------------------------------\n')
    await bot.send_message(message.chat.id, msg_to_answer)


# @router.message(F.text == 'Show Sellers')
# async def show_sellers(message: types.Message):
#     sellers = await get_sellers()
#     msg_to_answer = ''
#     for seller in sellers:
#         msg_to_answer += (f'Seller: {seller.name}\n'
#                           f'-------------------------------------------------------\n')
#         await bot.send_message(message.chat.id, msg_to_answer)


@router.message(F.text == 'Show Sellers')
async def show_sellers(message: types.Message):
    async with aiohttp.ClientSession() as session:
        async with session.get('http://127.0.0.1:8000/catalog/sellers/') as response:
            data = await response.json()
            msg_to_answer = ''
            for item in data:
                msg_to_answer += (f'Seller: {item["name"]}'
                                  f'Contact: {item["contact"]}\n'
                                  f'@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n')
            await bot.send_message(message.chat.id, msg_to_answer)


@router.message(F.text == 'Show Cart')
async def ask_for_login(message: types.Message, state: FSMContext):
    await message.reply('Enter login')
    await state.set_state(SomeState.waiting_for_login)


@router.message(SomeState.waiting_for_login)
async def capture_login(message: types.Message, state: FSMContext):
    await state.update_data(login=message.text)
    await message.reply('Enter password')
    await state.set_state(SomeState.waiting_for_password)


@router.message(SomeState.waiting_for_password)
async def capture_password(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    login = user_data['login']
    password = message.text

    user_cart_data = await fetch_user_cart(login, password)

    if user_cart_data:
        msg_to_answer = ''
        print(user_cart_data)
        products = user_cart_data['products']
        for product in products:
            msg_to_answer += (f'Product: {product["name"]}\n'
                              f'Count: {product["count"]}\n')
        msg_to_answer += f'Result price: {user_cart_data["result_price"]}'
        await bot.send_message(message.chat.id, msg_to_answer)
    else:
        await bot.send_message(message.chat.id, 'Wrong login or password')


async def main():
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


class Command(BaseCommand):
    help = 'Telegram bot for online shop'

    def handle(self, *args, **options):
        asyncio.run(main())
