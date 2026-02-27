from aiogram.fsm.state import StatesGroup, State
from openn import * 
from tekshir import *
from funksiyalar import *
Videos=videos_ochish()
class videos_add_step(StatesGroup):
    nomi = State()
    fasl_raqami = State()
    video_raqami = State()
    video_id = State()
class Kontent_upload_step(StatesGroup):
    nomi2 = State()
    fasl_raqami2= State()
    video_raqami2 = State()
    video_id2 = State()
class Yangi_kontent():
    def __init__(self):
        self.video_data = {}
        self.step = {}
        self.step_video = {}
        self.videos_tanlash={}
    async def boshlash(self, message: Message):
        user_id = message.from_user.id
        self.step[user_id] = 1
        await message.answer("Yangi kontent qo'shish jarayoni boshlandi.\nKontent nomini kiriting:", reply_markup=orqaga1())
    async def kontent_qoshish(self, message: Message):
      if message.text == "Orqaga":
        user_id = message.from_user.id
        self.step[user_id] = 0
        self.video_data.pop(user_id, None)
        await start_all(message)
        await message.answer("Orqaga qaytildi.", reply_markup=await start_all(message))
        
      elif message.content_type == "text" and self.step.get(message.from_user.id) == 1:
        user_id = message.from_user.id
        self.step[user_id] = 2
        self.video_data[user_id] = {"nomi": message.text}
        await message.answer("Fasl raqamini kiriting:", reply_markup=orqaga1())
      else:
        await message.answer("Iltimos, kontent nomini matn formatida kiriting.")
    async def fasl_raqami_qoshish(self, message: Message):
      if message.text == "Orqaga":
        user_id = message.from_user.id
        self.step[user_id] = 0
        self.video_data.pop(user_id, None)
        await message.answer("Orqaga qaytildi.", reply_markup=await start_all(message))
      elif  self.step.get(message.from_user.id) == 2:
       
       if intmi(message.text):
        user_id = message.from_user.id
        self.step[user_id] = 3
        self.video_data[user_id]["fasl_raqami"] = message.text
        await message.answer("Videoni yuboring:", reply_markup=orqaga1())
       else:
            await message.answer("Iltimos, fasl raqamini butun son formatida kiriting.")
      else:
        await message.answer("Iltimos, fasl raqamini butun son formatida kiriting.")
    async def video_qoshish(self, message: Message):
      if message.text == "Orqaga":
        user_id = message.from_user.id
        self.step[user_id] = 0
        self.video_data.pop(user_id, None)
        await message.answer("Orqaga qaytildi.", reply_markup=await start_all(message))
      if self.step.get(message.from_user.id) == 3 and (message.content_type == "video" or message.content_type=="document"):
        user_id = message.from_user.id
        video_id = message.video.file_id if message.content_type == "video" else message.document.file_id
        message_caption = message.caption if message.caption else ""
        nomi=self.video_data[user_id]["nomi"]
        fasl_raqami=self.video_data[user_id]["fasl_raqami"]
        if nomi not in Videos:
            Videos[nomi]={}
        if fasl_raqami not in Videos[nomi]:
            Videos[nomi][fasl_raqami]={}
            video_raqami=len(Videos[nomi][fasl_raqami].keys())+1 
        else:
            video_raqami=len(Videos[nomi][fasl_raqami].keys())+1
        if video_raqami not in Videos[nomi][fasl_raqami]:
            Videos[nomi][fasl_raqami][video_raqami]={}
        Videos[nomi][fasl_raqami][video_raqami][video_id]=message_caption
        videos_saqlash(Videos)
        await message.answer("Video muvaffaqiyatli qo'shildi!", reply_markup=orqaga1())
class Kontent_ochirish(StatesGroup):
    def __init__(self):
       self.tanlash={}
    nomi = State()
    fasl_raqami = State()
    video_raqami = State()
class Broadcast_step(StatesGroup):
    xabar = State()
class Post_qoshish(StatesGroup):
    rasm = State()
    post = State()
    content=State()
    fasl=State()
    qismlar=State()
    post1={}
class Admin_upload(StatesGroup):
    admin_id = State()
class Majburiy_obunalar(StatesGroup):
    kanal_nomi=State()
class Majburiy_obunalar_ochirish(StatesGroup):
    kanal_nomi=State()
class mavjud_content(StatesGroup):
    nomi1=State()
    fasl1=State()
    video_raqami1=State()
    video_id1=State()
