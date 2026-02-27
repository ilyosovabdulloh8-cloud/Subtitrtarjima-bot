from aiogram.fsm.state import StatesGroup, State
from aiogram import Bot, Dispatcher, F
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from openn import *
from tekshir import *
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from keyboards import *
bot = Bot(token=token())
dp = Dispatcher()
Videos=videos_ochish()
users=videos_ochish()
def admin_idni_ochir(admin_id):
  admin_ids=admin_idlarni_ochish()
  admin_id=str(admin_id)
  if admin_id in admin_ids:
    with open("admins.txt", "w") as file:
        for id in admin_ids:
            if id != admin_id:
                file.write(str(id) + "\n")
def Majburiy_obunalar_ochir(channel_id):
  kanallar=kanallar_ochish()
  channel_id=str(channel_id)
  if channel_id in kanallar:
    with open("kanallar.txt", "w") as file:
        for id in kanallar:
            if id != channel_id:
                file.write(str(id) + "\n")
def intmi(text):
    try:
        int(text)
        return True
    except ValueError:
        return False
async def yarat(rep1, rep2):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = KeyboardButton(text=rep1)
    btn2 = KeyboardButton(text=rep2)
    markup.add(btn1, btn2)
    return markup
def tartiblash(dict1):
    tartiblangan_dict = {}
    for key in sorted(dict1.keys(), key=lambda x: int(x) if x.isdigit() else x):
        tartiblangan_dict[key] = dict1[key]
    return tartiblangan_dict
async def video_yuborish(nomi,fasl,video_raqami,message):
    Videos=videos_ochish()
    if nomi in Videos and fasl in Videos[nomi] and video_raqami in Videos[nomi][fasl]:
        try:
           try:
            for video_id,caption in Videos[nomi][fasl][video_raqami].items():
               await bot.send_video(chat_id=message.from_user.id, video=video_id, caption=caption)
           except:
                           for video_id,caption in Videos[nomi][fasl][video_raqami].items():
                               await  bot.send_document(chat_id=message.from_user.id, document=video_id, caption=caption)

        except :
          try:
            video_id=Videos[nomi][fasl][video_raqami]
            await bot.send_video(chat_id=message.from_user.id, video=video_id, protect_content=True)
          except:
            video_id=Videos[nomi][fasl][video_raqami]
            await bot.send_document(chat_id=message.from_user.id, document=video_id, protect_content=True)  
    else:
        return None
    
async def video_id_yuborish(content,fasl,raqami):
    Videos=videos_ochish()
    if content in Videos and fasl in Videos[content] and raqami in Videos[content][fasl]:
        video_id=Videos[content][fasl][raqami].keys()
        return video_id
    else:
        return None
