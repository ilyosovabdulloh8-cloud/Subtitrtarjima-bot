import sqlite3
import json
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram import Bot, Dispatcher


def token_edit(token):
    with open("token.txt","w") as f:
        f.write(token)
    return
def admin_qosh(admin):
    with open("admins.txt","r") as f:
        admins=f.read()
        if admin in admins:
            print("bu admin bor")
        else:
            with open("admins.txt","a") as f:
                f.write(f"{admin}\n")
            print("qoshildi")
    return
def commond_ochir(admin):
    with open("admins.txt","r") as f:
        admins=f.read()
        if admin in admins:
            with open("admins.txt","w") as f:
                for i in admins:
                   if admin!=i:
                        f.write("{i}\n")
                   else:
                       print("ochdi")
        else:
            print("bunday admin yoq")
    return
def admins():
    with open("admins.txt","r") as f:
        admins=f.read()
        return admins
def owners():
    with open("owners.txt","r") as f:
        owner=f.read()
        return owner
def video_lists(txt,son):
    ulash=sqlite3.connect("videolar.db")
    cs=ulash.cursor()
    cs.execute("CREATE TABLE IF NOT EXISTS video (video TEXT,id INTEGER)")
    cs.execute("INSERT INTO video (video,id) VALUES (?,?)",(txt,son,))
    ulash.commit()
    """ cs.execute("SELECT * FROM video")
    print(cs.fetchall()) """
    return
def video_upload():
    ulash=sqlite3.connect("videolar.db")
    cs=ulash.cursor()
    cs.execute("SELECT * FROM video")
    return cs.fetchall()
def videos_saqlash(videos):
    with open("videos.json","w",encoding="utf-8") as f:
        json.dump(videos,f,ensure_ascii=False, indent=4)
def videos_ochish():
  try:
    with open("videos.json","r",encoding="utf-8") as f:
        videos=json.load(f)
        return videos
  except :
              return {}

def user_idlarni_ochish():
    try:
        with open("user_ids.txt", "r") as file:
            user_ids = [line.strip() for line in file]
        return user_ids
    except FileNotFoundError:
        return []

users=user_idlarni_ochish()

def User_idni_saqlash(user_id):
  users=user_idlarni_ochish()
  user_id=str(user_id)
  if user_id not in users:
    with open("user_ids.txt", "a") as file:

        file.write(str(user_id) + "\n")

def uuid_saqlash(dict):
    with open("uuids.json", "w", encoding="utf-8") as f:
        json.dump(dict, f, ensure_ascii=False, indent=4)
def uuid_ochish():
    try:
        with open("uuids.json", "r", encoding="utf-8") as f:
            uuids = json.load(f)
            return uuids
    except :
        return {}

def admin_idlarni_ochish():
    try:
        with open("admins.txt", "r") as file:
            admin_ids = [line.strip() for line in file]
        return admin_ids
    except FileNotFoundError:
        return []
def admin_idni_saqlash(admin_id):
  admin_ids=admin_idlarni_ochish()
  admin_id=str(admin_id)
  if admin_id not in admin_ids:
    with open("admins.txt", "a") as file:

        file.write(str(admin_id) + "\n")  
def kanallar_ochish():
    try:
        with open("kanallar.txt", "r") as file:
            kanallar = [line.strip() for line in file]
        return kanallar
    except FileNotFoundError:
        return []
