from openn import *
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
def adminmi(admin):
    return str(admin) in admins()
def ownermi(owner):
    return str(owner) in owners()
