import os
import asyncio

from aiogram import Bot, Dispatcher,F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from dotenv import load_dotenv

import keyboard as kb
import service
from states import Questionnairre, Order
from db_interaction import db


load_dotenv()


TOKEN = os.getenv('BOT_TOKEN')


WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")


bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.callback_query()
async def get_callback(callback : CallbackQuery):
    if callback.data == 'like':
        await callback.message.answer('Мы рады')
    elif callback.data == 'dislike':
        await callback.message.answer('Нам очень жаль')
    elif callback.data == 'tiger':
        await callback.message.answer('Ухх какой тигр')
    elif callback.data == 'car':
        await callback.message.answer('Ухх какая машина')



@dp.message(CommandStart())
async def greet_user(message: Message):
    username = message.from_user.username
    if username:
        await message.answer(f'Hello @{username}!',
        reply_markup=kb.main_page_keyboard)
    else:
        full_name = message.from_user.full_name
        await message.answer(f'Hello {full_name}',
        reply_markup=kb.main_page_keyboard)


# @dp.message(Command(commands='order'))
# async def order_command(message : Message):
#     await message.answer('Do you want to order something?',
#     reply_markup=kb.main_page_keyboard)


@dp.message(F.text == 'ORDER NOW')
async def get_order(message : Message,state:FSMContext):
        await message.answer('What product would you like to order')
        await state.set_state(Order.product)


@dp.message(F.text == 'WEATHER')
async def weather_command(message: Message):
    await service.handle_weather(message)



@dp.message(Order.product)
async def product_command(message : Message,state:FSMContext):
    await state.update_data(product=message.text)
    await state.set_state(Order.color)
    await message.answer('What color')


@dp.message(Order.color)
async def color_command(message: Message, state:FSMContext):
    await state.update_data(color=message.text)
    await state.set_state(Order.amount)
    await message.answer('What amount')


@dp.message(Order.amount)
async def amount_command(message: Message, state:FSMContext):
    await state.update_data(amount=message.text)
    await state.set_state(Order.address)
    await message.answer('Address')


@dp.message(Order.address)
async def address_command(message: Message, state:FSMContext):
    await state.update_data(address=message.text)
    await state.set_state(Order.payment)
    await message.answer('Payment')


@dp.message(Order.payment)
async def payment_command(message: Message, state:FSMContext):
    data = await state.get_data()
    await message.answer(f"Клиент: {message.from_user.username}\n"
                         f"Товар: {data['product']}\n"
                         f"Цвет: {data['color']}\n"
                         f"Количество: {data['amount']}\n"
                         f"Адресс: {data['address']}\n"
                         f"Оплата: {message.text}")
    await state.clear()


@dp.message(Command(commands='help'))
async def help_command(message: Message):
    await message.reply('I am here to help',
    reply_markup=kb.inline_keyboard_kb2)


@dp.message(Command(commands='questions'))
async def about_command(message:Message,state:FSMContext):
    await state.set_state(Questionnairre.gender)
    await message.answer('Какой у тебя пол?')


@dp.message(Questionnairre.gender)
async def gender_command(message: Message,state:FSMContext):
    await state.update_data(gender=message.text)
    await state.set_state(Questionnairre.age)
    await message.answer('Сколько тебе лет?')


@dp.message(Questionnairre.age)
async def age_command(message: Message,state:FSMContext):
    if message.text.isdigit():
        await state.update_data(age=message.text)
        await state.set_state(Questionnairre.job)
        await message.answer('Кем ты работаешь?')
    else:
        await message.answer('Ответь на мой вопрос')


@dp.message(Questionnairre.job)
async def job_command(message: Message, state: FSMContext):
    data = await state.get_data()
    await message.answer(f"Aнкета для заполнения : {message.from_user.username}\n"
                         f"Пол : {data['gender']}\n"
                         f"Работа : {message.text}")
    await state.clear()


@dp.message(F.text)
async def message_handler(message: Message):
    user = await db.check_user(message.chat.id)
    if user is None:
        await db.add_user(message.chat.id, message.from_user.username)
    if message.text ==  'AI CHAT':
        await message.answer('Пока что в разработке',parse_mode=ParseMode.HTML,reply_markup=kb.inline_keyboard_kb)
    elif message.text == 'AI IMAGE':
        await message.answer('Пока что в разработке',parse_mode=ParseMode.HTML,reply_markup=kb.inline_keyboard_kb)
    else:
        await message.answer(f'You typed {message.text}')


@dp.message(F.photo)
async def photo_handler(message: Message):
    await  message.reply('Some photo')


async def main():
    print('Bot started')
    try:
        await db.connect()
        await dp.start_polling(bot)
    except Exception as e:
        print(e)
    finally:
        await db.disconnect()


if __name__ == '__main__':
    asyncio.run(main())

