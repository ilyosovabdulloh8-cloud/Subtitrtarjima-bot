from openn import *
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from openn import *
bot = Bot(token=token())
def adminmi(admin):
    return str(admin) in admins()
def ownermi(owner):
    return str(owner) in owners()
