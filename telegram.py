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
# инициализируем соединение с БД
db = SQLighter()
session = requests.Session()


# @dp.message_handler()
# async def echo(message: types.Message):
#     await message.answer(message.text)

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
    for ind in range(1):
        answ_bs = BS(
            session.get(f"https://office.ivtecon.ru/projects/support_ga/issues?page={ind + 1}&query_id=91").content,
            'html.parser')
        for stri in answ_bs.select('.subject'):
            last_page.append(stri.getText() if stri.getText() != 'Тема' else f'page = {ind}')
    return last_page


@dp.message_handler(commands=['get_last_page'])
async def echo(message: types.Message):
    last_page = tecon_speak()
    answer = []
    last = db.get_last_field(message.chat.id)
    for topic in last_page:
        if topic == last:
            break
        answer.append(topic)


async def get_last_page(wait_for):

    while True:
        await asyncio.sleep(wait_for)
        last_page = tecon_speak()
        answer = []
        last = db.get_last_field(824893928)
        for topic in last_page:
            if topic == last:
                break
            answer.append(topic)

        db.add_last_me(824893928, last_page[1])
        await bot.send_message(824893928, str('\n' + '-' * 60 + '\n').join(answer), disable_notification=True)





# Команда активации подписки
@dp.message_handler(commands=['subscribe'])
async def subscribe(message: types.Message):
    if not db.subscriber_exists(message.from_user.id):
        # если юзера нет в базе, добавляем его
        db.add_subscriber(message.from_user.id)
    else:
        # если он уже есть, то просто обновляем ему статус подписки
        db.update_subscription(message.from_user.id, True)

    await message.answer(
        "Вы успешно подписались на рассылку!\nЖдите, скоро выйдут новые обзоры и вы узнаете о них первыми =)")


# Команда отписки
@dp.message_handler(commands=['unsubscribe'])
async def unsubscribe(message: types.Message):
    if not db.subscriber_exists(message.from_user.id):
        # если юзера нет в базе, добавляем его с неактивной подпиской (запоминаем)
        db.add_subscriber(message.from_user.id, False)
        await message.answer("Вы итак не подписаны.")
    else:
        # если он уже есть, то просто обновляем ему статус подписки
        db.update_subscription(message.from_user.id, False)
        await message.answer("Вы успешно отписаны от рассылки.")


# проверяем наличие новых игр и делаем рассылки
async def scheduled(wait_for):
    while True:
        await asyncio.sleep(wait_for)

        await bot.send_message(753110279, 'Ого', disable_notification=True)


# запускаем лонг поллинг
if __name__ == '__main__':
    dp.loop.create_task(get_last_page(10))  # пока что оставим 10 секунд (в качестве теста)
    login()
    executor.start_polling(dp, skip_updates=True)
