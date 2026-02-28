import asyncio
from openn import *
from tekshir import *
from funksiyalar import *
from aiogram import types
from aiogram import BaseMiddleware, Bot, Dispatcher, F
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from keyboards import *
from classes import *
import uuid


import os
TOKEN = os.getenv("BOT_TOKEN")
video=videos_ochish()
videos_uuid=uuid_ochish()
Videolar1={}
bot = Bot(token)
dp = Dispatcher()
kontent_ochirish = Kontent_ochirish()
yangi_kontent = Yangi_kontent()

def get_channels():
    try:
        with open("kanallar.txt", "r") as f:
            return [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        return []

class CheckSubscription(BaseMiddleware):
    async def __call__(self, handler, event: Message, data):
        if event.text and event.text.startswith("/start"): # Startda har doim tekshirish
            pass 
        
        channels = get_channels()
        not_joined = []

        for channel in channels:
            try:
                member = await event.bot.get_chat_member(chat_id=channel, user_id=event.from_user.id)
                if member.status not in ["member", "administrator", "creator"]:
                    not_joined.append(channel)
            except Exception:
                continue 
        if not_joined:
            buttons = []
            for ch in not_joined:
                url = f"https://t.me/{ch[1:]}" if ch.startswith("@") else "https://t.me/c/1234567" # ID uchun taxminiy
                buttons.append([InlineKeyboardButton(text="Kanalga a'zo bo'lish", url=url)])
            
            buttons.append([InlineKeyboardButton(text="Tekshirish âœ…", callback_data="check")])
            markup = InlineKeyboardMarkup(inline_keyboard=buttons)
            
            return await event.answer("Botdan foydalanish uchun quyidagi kanallarga obuna bo'ling:", reply_markup=markup)
        
        return await handler(event, data)
    
@dp.callback_query(F.data == "check")
async def check_callback(callback: types.CallbackQuery):
    # Bu yerda qaytadan tekshirish ham mumkin, hozircha shunchaki startga yo'llaymiz
    await callback.message.delete()
    await callback.message.answer("Rahmat! Endi qaytadan /start buyrug'ini yuboring.")

async def main():
    dp.message.outer_middleware(CheckSubscription())
    await dp.start_polling(bot)

@dp.message(Command("start"))
async def start(message: Message, state: FSMContext):
    await state.clear()
    if message.content_type == "text" :
        args = message.text.split()

        if len(args) > 1:
           for id ,caption in videos_uuid.get(args[1], {}).items():
              try:
                 await bot.send_video(chat_id=message.from_user.id, video=id, caption=caption,protect_content=True)
              except:
                 await bot.send_document(chat_id=message.from_user.id, document=id, caption=caption,protect_content=True)
        else:
         await message.answer("Salom ðŸ‘‹")
    User_idni_saqlash(message.from_user.id)
    await start_all(message)

@dp.message(F.text == "Orqaga")
async def orqaga2(message: Message):
    
    await start_all(message)

@dp.message(F.text == "ðŸŽ¬ Kontent")
async def kontent(message: Message):
   if ownermi(message.from_user.id) or adminmi(message.from_user.id):
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Yangi kontent qo'shish")],
            [KeyboardButton(text="Mavjud kontentga qo'shish")],
            [KeyboardButton(text="Kontentlar ro'yxati")],
            [KeyboardButton(text="Orqaga")]
        ],
        resize_keyboard=True
    )

    await message.answer(
        "Kerakli boâ€˜limni tanlang:",
        reply_markup=markup
    )

@dp.message(F.text == "Mavjud kontentga qo'shish")
async def mavjud_kontentga_qoshish(message: Message,state: FSMContext):
    await state.set_state(mavjud_content.nomi1)
    await message.answer("Kontent nomini kiriting:",reply_markup=await contents())
@dp.message(mavjud_content.nomi1)
async def mavjud_kontent_nomi_olish(message: Message, state: FSMContext):
    if ownermi(message.from_user.id) or adminmi(message.from_user.id):
        if message.text == "Orqaga":
            await start_all(message)
            state.clear()
        else:
            if message.from_user.id not in Videolar1:
                Videolar1[message.from_user.id] = {}
            Videolar1[message.from_user.id]["nomi"] = message.text
            await state.set_state(mavjud_content.fasl1)
            await message.answer("Fasl raqamini kiriting:",reply_markup=await Mavsumlar_main(message.text))
@dp.message(mavjud_content.fasl1)
async def mavjud_kontent_fasl_raqami_olish(message: Message, state: FSMContext):
    if ownermi(message.from_user.id) or adminmi(message.from_user.id):
        if message.text == "Orqaga":
            await start_all(message)
            state.clear()
            Videolar1.pop(message.from_user.id, None)
        else:
            Videolar1[message.from_user.id]["fasl_raqami"]=message.text
            await state.set_state(mavjud_content.video_id1)
            await message.answer("Videoni yuboring:",reply_markup=await videolar_main(Videolar1[message.from_user.id]["nomi"],Videolar1[message.from_user.id]["fasl_raqami"]))
@dp.message(mavjud_content.video_id1)
async def mavjud_kontent_video_id_olish(message: Message, state: FSMContext):
    if ownermi(message.from_user.id) or adminmi(message.from_user.id):
        if message.text == "Orqaga":
            await start_all(message)
            state.clear()
            Videolar1.pop(message.from_user.id, None)
        yangi_kontent.video_qoshish(message)
        await state.set_state(mavjud_content.video_id1)

@dp.message(F.text == "Kontentlar ro'yxati")
async def kontentlar_royxati(message: Message,state: FSMContext):
        await message.answer("Kontentlar ro'yxati:",reply_markup=await contents())
        await state.set_state(Kontent_upload_step.nomi2)
@dp.message(Kontent_upload_step.nomi2)
async def kontent_nomi_olish(message: Message, state: FSMContext):
 if ownermi(message.from_user.id) or adminmi(message.from_user.id):
  if message.text == "Orqaga":
    await start_all(message)
  else:
    yangi_kontent.videos_tanlash["nomi"]=message.text
    await state.set_state(Kontent_upload_step.fasl_raqami2)
    await message.answer("Fasl raqamini kiriting:",reply_markup=await Mavsumlar_main(message.text))
@dp.message(Kontent_upload_step.fasl_raqami2)
async def kontent_fasl_raqamini_olish(message: Message, state: FSMContext):
  if ownermi(message.from_user.id) or adminmi(message.from_user.id):
   if message.text == "Orqaga":
    await start_all(message)
   else:
    yangi_kontent.videos_tanlash["fasl_raqami"]=message.text
    await state.set_state(Kontent_upload_step.video_raqami2)
    await message.answer("Video raqamini kiriting:",reply_markup= await videolar_main(yangi_kontent.videos_tanlash["nomi"],yangi_kontent.videos_tanlash["fasl_raqami"]))
@dp.message(Kontent_upload_step.video_raqami2)
async def kontent_video_raqamini_olish(message: Message, state: FSMContext):
  if ownermi(message.from_user.id) or adminmi(message.from_user.id):
   if message.text == "Orqaga":
    await start_all(message)
   else:
    yangi_kontent.videos_tanlash["video_raqami"]=message.text
    await message.answer("Videolar",reply_markup=orqaga1())
    await video_yuborish(yangi_kontent.videos_tanlash["nomi"],yangi_kontent.videos_tanlash["fasl_raqami"],yangi_kontent.videos_tanlash["video_raqami"],message)


@dp.message(F.text == "Yangi kontent qo'shish" )
async def yangi_kontent_qoshish(message: Message,state: FSMContext):
    await state.set_state(videos_add_step.nomi)
    await yangi_kontent.boshlash(message)
@dp.message(videos_add_step.nomi)
async def kontent_nomi_qoshish(message: Message, state: FSMContext):
    await yangi_kontent.kontent_qoshish(message)
    await state.set_state(videos_add_step.fasl_raqami)
@dp.message(videos_add_step.fasl_raqami)
async def kontent_fasl_raqami_qoshish(message: Message, state: FSMContext):
    await yangi_kontent.fasl_raqami_qoshish(message)
    await state.set_state(videos_add_step.video_id)
@dp.message(videos_add_step.video_id)
async def kontent_video_qoshish(message: Message, state: FSMContext):
   if ownermi(message.from_user.id) or adminmi(message.from_user.id):
    if message.text == "Orqaga":
        await start_all(message)
        await state.clear()
    else:
        await yangi_kontent.video_qoshish(message)
        await state.set_state(videos_add_step.video_id)

@dp.message(F.text=="ðŸ—‘ Kontent o'chirish")
async def kontent_ochirishsh(message: Message,state: FSMContext):
  if ownermi(message.from_user.id) or adminmi(message.from_user.id):
    await message.answer("O'chirish uchun kontent nomini kiriting:",reply_markup=await contents())
    await state.set_state(kontent_ochirish.nomi)
@dp.message(kontent_ochirish.nomi)
async def kontent_ochirish_nomi(message: Message, state: FSMContext):
   if ownermi(message.from_user.id) or adminmi(message.from_user.id):
    if message.text == "Orqaga":
        await start_all(message)
    else:
        kontent_ochirish.tanlash[message.from_user.id]={"nomi":message.text}
        await message.answer("O'chirish uchun fasl raqamini kiriting:",reply_markup=await Mavsumlar_main(message.text))
        await state.set_state(kontent_ochirish.fasl_raqami)
@dp.message(kontent_ochirish.fasl_raqami)
async def kontent_ochirish_fasl_raqami(message: Message, state: FSMContext):
   if ownermi(message.from_user.id) or adminmi(message.from_user.id):
    if message.text == "Orqaga":
        await start_all(message)
        await state.clear()
        kontent_ochirish.tanlash.pop(message.from_user.id, None)
    else:
        kontent_ochirish.tanlash[message.from_user.id]["fasl_raqami"]=message.text
        await message.answer("O'chirish uchun video raqamini kiriting:",reply_markup=await videolar_main(kontent_ochirish.tanlash[message.from_user.id]["nomi"],message.text))
        await state.set_state(kontent_ochirish.video_raqami)
@dp.message(kontent_ochirish.video_raqami)
async def kontent_ochirish_video_raqami(message: Message, state: FSMContext):
   if ownermi(message.from_user.id) or adminmi(message.from_user.id):
    if message.text == "Orqaga":
        await start_all(message)
        await state.clear()
        kontent_ochirish.tanlash.pop(message.from_user.id, None)
    else:
        kontent_ochirish.tanlash[message.from_user.id]["video_raqami"]=message.text
        Videos=videos_ochish()
        nomi=kontent_ochirish.tanlash[message.from_user.id]["nomi"]
        fasl=kontent_ochirish.tanlash[message.from_user.id]["fasl_raqami"]
        video_raqami=kontent_ochirish.tanlash[message.from_user.id]["video_raqami"]
        if nomi in Videos and fasl in Videos[nomi] and video_raqami in Videos[nomi][fasl]:
            del Videos[nomi][fasl][video_raqami]
            Videos=videos_ochish()
            videos_saqlash(Videos)
            await state.clear()
            await message.answer("Video muvaffaqiyatli o'chirildi!", reply_markup=await start_all(message))
        else:
            await message.answer("Kechirasiz, bunday kontent topilmadi.", reply_markup=await start_all(message))

@dp.message(F.text=="ðŸ“¢ Broadcast")
async def broadcast(message: Message, state: FSMContext):
    if ownermi(message.from_user.id) or adminmi(message.from_user.id):
        await message.answer("Yuboriladigan xabarni kiriting:")
        await state.set_state(Broadcast_step.xabar)
@dp.message(Broadcast_step.xabar)
async def broadcast_xabar(message: Message, state: FSMContext):
    if ownermi(message.from_user.id) or adminmi(message.from_user.id):
        broadcast_list =user_idlarni_ochish()
        for user_id in broadcast_list:
            try:
                if message.content_type == "text":
                    await bot.send_message(chat_id=user_id, text=message.text)
                elif message.content_type == "photo":
                    await bot.send_photo(chat_id=user_id, photo=message.photo[-1].file_id, caption=message.caption if message.caption else "")
                elif message.content_type == "video":
                    await bot.send_video(chat_id=user_id, video=message.video.file_id, caption=message.caption if message.caption else "")
                elif message.content_type == "document":
                    await bot.send_document(chat_id=user_id, document=message.document.file_id, caption=message.caption if message.caption else "")
            except Exception:
                continue
        await message.answer("Xabar muvaffaqiyatli yuborildi!")
        await state.clear()

@dp.message(F.text=="ðŸ“¦ Postlar")
async def qostlar(message: Message, state: FSMContext):
    if ownermi(message.from_user.id) or adminmi(message.from_user.id):
        Post_qoshish.post1[message.from_user.id] = {}
        await message.answer("Rasm yuboring:")
        await state.set_state(Post_qoshish.rasm)
@dp.message(Post_qoshish.rasm)
async def qostlar_rasm(message: Message, state: FSMContext):
    if message.text == "Orqaga":
        await start_all(message)
        await state.clear()
    if ownermi(message.from_user.id) or adminmi(message.from_user.id):
        if message.content_type == "photo":
            photo_id = message.photo[-1].file_id
            Post_qoshish.post1[message.from_user.id]["rasm"] = photo_id
            await state.set_state(Post_qoshish.post)
            await message.answer("Soz kiriting:")
        else:
            await message.answer("Iltimos, rasm yuboring.")
@dp.message(Post_qoshish.post)
async def qostlar_post(message: Message, state: FSMContext):
    if message.text == "Orqaga":
        await start_all(message)
        await state.clear()
        Post_qoshish.post1.pop(message.from_user.id, None)
    if ownermi(message.from_user.id) or adminmi(message.from_user.id):
        Post_qoshish.post1[message.from_user.id]["post"] = message.text
        await state.set_state(Post_qoshish.content)
        await message.answer("Content kiriting:",reply_markup=await contents())
@dp.message(Post_qoshish.content)
async def qostlar_content(message: Message, state: FSMContext):
    if ownermi(message.from_user.id) or adminmi(message.from_user.id):
        if message.text == "Orqaga":
            await start_all(message)
            await state.clear()
            Post_qoshish.post1.pop(message.from_user.id, None)
        Post_qoshish.post1[message.from_user.id]["content"] = message.text
        await state.set_state(Post_qoshish.fasl)
        await message.answer("Fasl kiriting:",reply_markup=await Mavsumlar_main(Post_qoshish.post1[message.from_user.id]["content"]))
@dp.message(Post_qoshish.fasl)
async def qostlar_fasl(message: Message, state: FSMContext):
    if ownermi(message.from_user.id) or adminmi(message.from_user.id):
        Post_qoshish.post1[message.from_user.id]["fasl"] = message.text
        await state.set_state(Post_qoshish.qismlar)
        await message.answer("Qismni kiriting:",reply_markup=await videolar_main    (Post_qoshish.post1[message.from_user.id]["content"],message.text))
@dp.message(Post_qoshish.qismlar)
async def qostlar_qismlar(message: Message, state: FSMContext):
    if ownermi(message.from_user.id) or adminmi(message.from_user.id):
        post_qismi=message.text
        post_rasmi=Post_qoshish.post1[message.from_user.id]["rasm"]
        post_sozi=Post_qoshish.post1[message.from_user.id]["post"]
        Videos=videos_ochish()
        uuid_str = str(uuid.uuid4())[:8] 
        for video_id,caption in Videos[Post_qoshish.post1[message.from_user.id]["content"]][Post_qoshish.post1[message.from_user.id]["fasl"]][post_qismi].items():
           try:
              videos_uuid[uuid_str][video_id]=caption
           except:
              videos_uuid[uuid_str]={video_id:caption}
        uuid_saqlash(videos_uuid)
        await bot.send_photo(chat_id=message.from_user.id, photo=post_rasmi, caption=f'<a href="https://t.me/Anivoz_3D_rasmiy_bot?start={uuid_str}">{post_sozi}</a>', parse_mode="HTML")
        await message.answer(f"https://t.me/Anivoz_3D_rasmiy_bot?start={uuid_str}")

@dp.message(F.text=="ðŸ‘® Adminlar")
async def adminlar(message: Message):
    if ownermi(message.from_user.id):
        markup = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Adminlar ro'yxati")],
            [KeyboardButton(text="Admin qo'shish")],
            [KeyboardButton(text="Admin o'chirish")],
            [KeyboardButton(text="Orqaga")]
        ],
        resize_keyboard=True)
        await message.answer("Kerakli boâ€˜limni tanlang:", reply_markup=markup)        
@dp.message(F.text=="Admin qo'shish")
async def admin_qoshish(message: Message, state: FSMContext):
    if ownermi(message.from_user.id):
        await message.answer("Qo'shmoqchi bo'lgan adminning ID sini kiriting:", reply_markup=orqaga1())
        await state.set_state(Admin_upload.admin_id)
@dp.message(Admin_upload.admin_id)
async def admin_qoshish_id(message: Message, state: FSMContext):
    if ownermi(message.from_user.id):
        if message.text == "Orqaga":
            await start_all(message)
            await state.clear()
        else:
            try:
                admin_id = int(message.text)
                admin_idni_saqlash(admin_id)
                await message.answer(f"Admin ID {admin_id} muvaffaqiyatli qo'shildi!", reply_markup=await start_all(message))
                await state.clear()
            except ValueError:
                await message.answer("Iltimos, to'g'ri ID formatida kiriting.")
@dp.message(F.text=="Admin o'chirish")
async def admin_ochirish(message: Message, state: FSMContext):
    if ownermi(message.from_user.id):
        await message.answer("O'chirmoqchi bo'lgan adminning ID sini kiriting:", reply_markup=orqaga1())
        await state.set_state(Admin_upload.admin_id)
@dp.message(Admin_upload.admin_id)
async def admin_ochirish_id(message: Message, state: FSMContext):
    if ownermi(message.from_user.id):
        if message.text == "Orqaga":
            await start_all(message)
            await state.clear()
        else:
            try:
                admin_id = int(message.text)
                admin_idni_ochir(admin_id)
                await message.answer(f"Admin ID {admin_id} muvaffaqiyatli o'chirildi!", reply_markup=await start_all(message))
                await state.clear()
            except ValueError:
                await message.answer("Iltimos, to'g'ri ID formatida kiriting.")
@dp.message(F.text=="Adminlar ro'yxati")
async def adminlar_royxati(message: Message):
    if ownermi(message.from_user.id):
        await message.answer("Adminlar ro'yxati:",reply_markup=await adminlar_upload())

@dp.message(F.text=="âš™ï¸ Majburiy obunalar")
async def majburiy_obunalar(message: Message, state: FSMContext):
    if ownermi(message.from_user.id):
        markup= ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="Obuna bo'lishi kerak bo'lgan kanalni ko'rish")],
            [KeyboardButton(text="Majburiy obuna qo'shish")],
            [KeyboardButton(text="Majburiy obuna o'chirish")],
            [KeyboardButton(text="Orqaga")]],
        resize_keyboard=True)
        await message.answer("Kerakli boâ€˜limni tanlang:", reply_markup=markup)
@dp.message(F.text=="Obuna bo'lishi kerak bo'lgan kanalni ko'rish")
async def majburiy_obunalar_royxati(message: Message):
    if ownermi(message.from_user.id):
        kanallar=kanallar_ochish()
        if kanallar:
            keyboard=ReplyKeyboardBuilder()
            for kanal in kanallar:
                keyboard.button(text=f"@{kanal}")
            keyboard.adjust(2)
            keyboard.row(KeyboardButton(text="Orqaga"))
            await message.answer(f"Majburiy obunalar ro'yxati:", reply_markup=keyboard.as_markup(resize_keyboard=True))
        else:
            await message.answer("Hozircha majburiy obunalar ro'yxati bo'sh.", reply_markup=orqaga1())
@dp.message(F.text=="Majburiy obuna qo'shish")
async def majburiy_obunalar_qoshish(message: Message, state: FSMContext):
    if ownermi(message.from_user.id):
        await message.answer("Obuna bo'lishi kerak bo'lgan kanalmi yuboring", reply_markup=orqaga1())
        await state.set_state(Majburiy_obunalar.kanal_nomi)
@dp.message(Majburiy_obunalar.kanal_nomi)
async def majburiy_obunalar_kanal(message: Message, state: FSMContext   ):
    if ownermi(message.from_user.id):
        if message.text == "Orqaga":
            await start_all(message)
            await state.clear()
        else:
            kanal_nomi = message.text.strip()
            if kanal_nomi.startswith("@"):
                kanal_nomi = kanal_nomi[1:]
            with open("kanallar.txt", "a") as f:
                f.write(kanal_nomi + "\n")
            await message.answer(f"Kanal @{kanal_nomi} majburiy obunalar ro'yxatiga qo'shildi!", reply_markup=await start_all(message))
            await state.clear()     
@dp.message(F.text=="Majburiy obuna o'chirish")
async def majburiy_obunalar_ochirish(message: Message, state: FSMContext):
    if ownermi(message.from_user.id):
        await message.answer("Obuna bo'lishi kerak bo'lmagan kanalmi yuboring", reply_markup=orqaga1())
        await state.set_state(Majburiy_obunalar_ochirish.kanal_nomi)
@dp.message(Majburiy_obunalar_ochirish.kanal_nomi)
async def majburiy_obunalar_ochirish_kanal(message: Message, state: FSMContext   ):

    if ownermi(message.from_user.id):
        if message.text == "Orqaga":
            await start_all(message)
            await state.clear()
        else:
            kanal_nomi = message.text.strip()
            if kanal_nomi.startswith("@"):
                kanal_nomi = kanal_nomi[1:]
            Majburiy_obunalar_ochir(kanal_nomi)
            await message.answer(f"Kanal @{kanal_nomi} majburiy obunalar ro'yxatidan o'chirildi!", reply_markup=await start_all(message))
            await state.clear()


async def main():
    # Middlewareni ulash
    dp.message.outer_middleware(CheckSubscription())
    
    # Pollingni boshlash
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot to'xtatildi")
