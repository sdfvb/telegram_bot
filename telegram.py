# -*- coding: cp1251 -*-
import asyncio

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
db = SQLighter('db.db')


# @dp.message_handler()
# async def echo(message: types.Message):
#     await message.answer(message.text)


def tecon_speak():
    URL = 'https://office.ivtecon.ru'
    SIGN_IN_URL = 'https://office.ivtecon.ru/login'
    LOGIN_URL = 'https://office.ivtecon.ru/login'
    session = requests.Session()
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

    last_page = []
    for ind in range(1):
        answ_bs = BS(session.get(f"https://office.ivtecon.ru/issues?page={ind}").content, 'html.parser')

        for stri in answ_bs.select('.subject'):
            last_page.append(stri.getText() if stri.getText() != '����' else f'page = {ind}')
    return last_page


@dp.message_handler(commands=['get_last_page'])
async def echo(message: types.Message):
    last_page = tecon_speak()
    await message.answer(str('\n' + '-' * 60 + '\n').join(last_page))


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


# ��������� ������� ����� ��� � ������ ��������
async def scheduled(wait_for):
    while True:
        await asyncio.sleep(wait_for)

        await bot.send_message(753110279, '���', disable_notification=True)


# ��������� ���� �������
if __name__ == '__main__':
    # dp.loop.create_task(scheduled(10))  # ���� ��� ������� 10 ������ (� �������� �����)

    executor.start_polling(dp, skip_updates=True)