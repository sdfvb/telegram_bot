# -*- coding: cp1251 -*-
import asyncio
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
import aiohttp
from aiogram import Bot, Dispatcher, executor, types
import re
import sys
from bs4 import BeautifulSoup as BS
import requests
from sqlighter import SQLighter
from aiogram.bot import api

pached_url = "https://telegg.ru/orig/bot{token}/{method}"
setattr(api, 'API_URL', pached_url)

bot = Bot(token='1005395522:AAH_Mz2DUbMfJ5J9gVvMkEO6xO2tFUhcz-E')
dp = Dispatcher(bot)
# �������������� ���������� � ��
db = SQLighter()
session = requests.Session()



button_subscribe = KeyboardButton('����������')
button_unsubscribe = KeyboardButton('����������')
button_get_last = KeyboardButton('�������� ��������� �������')




greet_kb = ReplyKeyboardMarkup()
greet_kb.add(button_subscribe)
greet_kb.add(button_unsubscribe)
greet_kb.add(button_get_last)


def login():
    URL = 'https://office.ivtecon.ru'
    SIGN_IN_URL = 'https://office.ivtecon.ru/login'
    LOGIN_URL = 'https://office.ivtecon.ru/login'

    sign_in_page = str(session.get(SIGN_IN_URL).content)
    for l in sign_in_page.split('\n'):
        m = re.search('name="authenticity_token" value="([^"]+)"', l)
        if m:
            break
    token = None
    if m:
        token = m.group(1)

    if not token:
        print('Unable to find the authenticity token')
        sys.exit(1)
    data = {'username': 'PuchkovaAC',
            'password': 'f,hfrflf,hf666/13',
            'authenticity_token': token,
            'autologin': '1'}
    r = session.post(LOGIN_URL, data=data)
    if r.status_code != 200:
        print('Failed to log in')
        sys.exit(1)
    answ_bs = BS(r.content, 'html.parser')


def tecon_speak():
    last_page = []
    update_page = []
    for ind in range(1):
        answ_bs = BS(
            session.get(f"https://office.ivtecon.ru/projects/support_ga/issues?page={ind + 1}&query_id=91").content,
            'html.parser')
        for stri in answ_bs.select('.subject'):
            last_page.append(stri.getText() if stri.getText() != '����' else f'page = {ind + 1}')

        for stri in answ_bs.select('.updated_on'):
            update_page.append(stri.getText() if stri.getText() != '����' else f'page = {ind + 1}')

    return last_page, update_page


@dp.message_handler(commands=['get_last_page'])
async def echo(message: types.Message):
    login()
    last_page, update_page = tecon_speak()
    answer = []
    last, date = db.get_last_field(message.chat.id)
    for topic in last_page:
        if topic == last:
            break
        answer.append(topic)
    await bot.send_message(message.chat.id, str('\n' + '-' * 60 + '\n').join(answer))

async def get_last_page(wait_for):
    while True:
        await asyncio.sleep(wait_for)
        await send_message()


async def send_message():
    login()
    last_page = tecon_speak()

    list_subs = db.get_subscriptions()

    for id, status, last_topic in list_subs:
        answer = []
        for topic in last_page:
            if topic == last_topic:
                break
            answer.append(topic)

        if len(answer) > 1:
            db.add_last_me(id, last_page[1])
            await bot.send_message(id, str('\n' + '-' * 60 + '\n').join(answer), disable_notification=True)


# ������� ��������� ��������
@dp.message_handler(commands=['subscribe'])
async def subscribe(message: types.Message):
    if not db.subscriber_exists(message.from_user.id):
        # ���� ����� ��� � ����, ��������� ���
        db.add_subscriber(message.from_user.id)
    else:
        # ���� �� ��� ����, �� ������ ��������� ��� ������ ��������
        db.update_subscription(message.from_user.id, True)

    await message.answer(
        "�� ������� ����������� �� ��������!\n�����, ����� ������ ����� ������ � �� ������� � ��� ������� =)")
    await message.reply("������!", reply_markup=greet_kb)
    # await send_message()

# ������� �������
@dp.message_handler(commands=['unsubscribe'])
async def unsubscribe(message: types.Message):
    if not db.subscriber_exists(message.from_user.id):
        # ���� ����� ��� � ����, ��������� ��� � ���������� ��������� (����������)
        db.add_subscriber(message.from_user.id, False)
        await message.answer("�� ���� �� ���������.")
    else:
        # ���� �� ��� ����, �� ������ ��������� ��� ������ ��������
        db.update_subscription(message.from_user.id, False)
        await message.answer("�� ������� �������� �� ��������.")
    db.add_last_me(message.from_user.id, '')




# ��������� ���� �������
if __name__ == '__main__':
    dp.loop.create_task(get_last_page(1800))  # ���� ��� ������� 10 ������ (� �������� �����)
    executor.start_polling(dp, skip_updates=True)
