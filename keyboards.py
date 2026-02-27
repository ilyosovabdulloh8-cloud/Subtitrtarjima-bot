from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from openn import videos_ochish
from tekshir import adminmi, ownermi


Videos=videos_ochish()
async def contents():
    Videos=videos_ochish()
    builder=ReplyKeyboardBuilder()

    for nomi in Videos.keys():
      builder.button(text=str(nomi))
    builder.adjust(2)
    builder.row(KeyboardButton(text="Orqaga"))
    return builder.as_markup(resize_keyboard=True)
async def Mavsumlar_main( nomi):
    if nomi in Videos:
        fasllar=Videos[nomi]
        builder=ReplyKeyboardBuilder()
        for i in fasllar.keys():
            builder.button(text=str(i))
        builder.adjust(2)
        builder.row(KeyboardButton(text="Orqaga"))
        return builder.as_markup(resize_keyboard=True)
    else:
        return None

async def start_all(message: Message):

    if  ownermi(message.from_user.id) or adminmi(message.from_user.id):

        markup = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="🎬 Kontent")],
                [KeyboardButton(text="🗑 Kontent o'chirish")],
                [KeyboardButton(text="📦 Postlar")],
                [KeyboardButton(text="📢 Broadcast")],
                [KeyboardButton(text="👮 Adminlar")],
                [KeyboardButton(text="⚙️ Majburiy obunalar")]
            ],
            resize_keyboard=True
        )

        await message.answer(" Assalomu alaykum! Kerakli bo‘limni tanlang:",
           
            reply_markup=markup
        )

    else:

        markup = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="Kontentlar ro'yxati")]],
            resize_keyboard=True
        )

        await message.answer(
            "Assalomu alaykum! Kerakli bo‘limni tanlang:",
            reply_markup=markup
        )

async def videolar_main(nomi,fasl):
    if nomi in Videos and fasl in Videos[nomi]:
        video_raqamlari=tartiblash(Videos[nomi][fasl])
        builder=ReplyKeyboardBuilder()
        for i in video_raqamlari:
            builder.button(text=str(i))
        builder.adjust(2)
        builder.row(KeyboardButton(text="Orqaga"))
        return builder.as_markup(resize_keyboard=True)
    else:
        return None
def orqaga1():
    markub = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Orqaga")]],
        resize_keyboard=True
    )
    return markub
def tartiblash(dict1):
    tartiblangan_dict = {}
    for key in sorted(dict1.keys(), key=lambda x: int(x) if x.isdigit() else x):
        tartiblangan_dict[key] = dict1[key]
    return tartiblangan_dict
async def adminlar_upload():
   try:
         with open("admins.txt","r") as f:
            admins=f.read().splitlines()
            builder=ReplyKeyboardBuilder()
            for i in admins:
                builder.button(text=str(i))
            builder.adjust(2)
            builder.row(KeyboardButton(text="Orqaga"))
            return builder.as_markup(resize_keyboard=True)
   except FileNotFoundError:
        return None
