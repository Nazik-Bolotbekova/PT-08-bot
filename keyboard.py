from aiogram import types
# from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton


main_page_keyboard = types.ReplyKeyboardMarkup(
    keyboard=[
        [

            types.KeyboardButton(text='AI CHAT'),
            types.KeyboardButton(text='AI IMAGE')

        ],
        [
            types.KeyboardButton(text='ORDER NOW'),
            types.KeyboardButton(text='WEATHER')

        ]

    ],
    resize_keyboard = True
)

inline_keyboard_kb = types.InlineKeyboardMarkup(
    inline_keyboard = [
        [
            types.InlineKeyboardButton(text="👍",
            callback_data ='like'),

        ],
        [
            types.InlineKeyboardButton(text="👎",
            callback_data ='dislike'),
        ]

    ]
)

inline_keyboard_kb2 = types.InlineKeyboardMarkup(
    inline_keyboard = [
        [
            types.InlineKeyboardButton(text='🐯',
            callback_data = 'tiger'),
        ],
        [
            types.InlineKeyboardButton(text='🚗',
            callback_data = 'car'),
        ]
    ]
)

