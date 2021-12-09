#!/usr/bin/python
# -*- coding: utf-8 -*-

import asyncio
import logging
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import state
from aiogram.types import User
from aiogram.types import message
from aiogram.utils import executor
from aiogram.utils.emoji import emojize
from aiogram.types.message import ContentType
from aiogram.utils.markdown import text, bold, italic, code, pre
from aiogram.types import ParseMode, InputMediaPhoto, InputMediaVideo, ChatActions
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from config import TOKEN
from config import PARKING_CHAT_ID
from messages import MESSAGES, TgAddresses
import keyboards as kb
from dbhelper import DBHelper
from stateflow import TestStates
from validator import Valid
from parkmap import ParkMap

logging.basicConfig(format=u'%(filename)+13s [ LINE:%(lineno)-4s] %(levelname)-8s [%(asctime)s] %(message)s',
                    level=logging.DEBUG)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())
taddr = TgAddresses()
taddr.tg_ids = {}
taddr_reply = TgAddresses()
taddr_reply.tg_ids = {}

@dp.message_handler(commands=['start'], state='*')
async def process_start_command(message: types.Message):

    logging.info("Chat ID = " + str(message.chat.id)) 
    try:
        user_channel_status = await bot.get_chat_member(chat_id=PARKING_CHAT_ID, user_id=message.from_user.id)
        logging.info(user_channel_status)

        if user_channel_status["status"] != 'left':
            logging.info("================= THIS IS OUR USER!=====================")
        else:
            logging.info("================= UNNOWN USER!=====================")
            await bot.send_message(message.from_user.id, MESSAGES['need_invite'])
            return None

        if str(message.chat.id) == str(PARKING_CHAT_ID): 
            await bot.send_message(message.chat.id, "Нене, {mn} приходи в личку, в общем чатике не разговариваю!".format(mn=message.from_user.mention))
            return None
        
    except Exception as e:
        logging.error(f"The error '{e}' occurred")   
        return None

    if str(message.chat.id) == str(PARKING_CHAT_ID): 
            await bot.send_message(message.chat.id, "Нене, {mn} приходи в личку, в общем чатике не разговариваю!".format(mn=message.from_user.mention))
            return None

    db = DBHelper()
    db_usr = await db.check_user(message.from_user, message.chat.id)
    if not db_usr:
        await message.reply(MESSAGES['nlo'])
        return None
    del db
    
    await TestStates.START_STATE.set()
    await message.reply(MESSAGES['start'], reply_markup=kb.meet_btn_markup)

@dp.message_handler(commands=['help'], state='*')
async def process_help_command(message: types.Message, state: FSMContext):
    taddr.tg_ids = {}
    if message.chat.id == PARKING_CHAT_ID:
            await bot.send_message(message.chat.id, "Нене, {} приходи в личку, в общем чатике не разговариваю!".format(message.from_user.mention))
            return None

    current_state = await state.get_state()
    if current_state is None:
        await message.reply(MESSAGES['nlo'])
        return None
    logging.info('Finish state %r', current_state)
    await state.finish()
    await TestStates.START_STATE.set()
    await bot.send_message(message.from_user.id, MESSAGES['help'])
    await bot.send_message(message.from_user.id, "Выберите пункт меню!", reply_markup=kb.meet_btn_markup)

@dp.callback_query_handler(lambda c: c.data == 'help_btn', state='*')
async def process_callback_home_btn(callback_query: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await TestStates.START_STATE.set()
    taddr.tg_ids = {}
    await bot.send_message(callback_query.from_user.id, MESSAGES['help'])
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, f"Идем в начало. Выберите пункт меню:", reply_markup=kb.meet_btn_markup)

@dp.callback_query_handler(lambda c: c.data == 'home_btn', state='*')
async def process_callback_home_btn(callback_query: types.CallbackQuery):
    await TestStates.START_STATE.set()
    taddr.tg_ids = {}
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, f"Идем в начало. Выберите действие:", reply_markup=kb.meet_btn_markup)

@dp.message_handler(lambda msg: not (hasattr(msg, 'callback_data')), state = TestStates.START_STATE)
async def process_name_start(message: types.Message, state: FSMContext):
    await message.reply("Выберите пункт меню!")
    
############################## SETTINGS ################################
@dp.callback_query_handler(lambda c: c.data == 'settings_btn', state='*')
async def process_callback_settings_btn(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, f"Привет {callback_query.from_user.mention}, Какие данные будем добавлять/править? ", reply_markup=kb.settings_btn_markup)
    await TestStates.SETTINGS_STATE.set()
    db = DBHelper()
    db_usr = await db.check_user(callback_query.from_user, callback_query.message.chat.id)
    contacts = await db.get_all_data(from_user=callback_query.from_user, datatype='all')
    del db
    info_message = await prepare_info_for_message(contacts, callback_query.from_user.mention)
    await bot.send_message(callback_query.from_user.id, info_message)
   
@dp.message_handler(lambda msg: not (hasattr(msg, 'callback_data')), state = TestStates.SETTINGS_STATE)
async def process_name_settings(message: types.Message, state: FSMContext):
    await message.reply("Нажмите кнопку")

###### CHANGE CONTACTS #####################
@dp.callback_query_handler(lambda c: c.data == 'my_settings_btn', state = TestStates.SETTINGS_STATE)
async def process_callback_my_settings_btn(callback_query: types.CallbackQuery):
    await TestStates.SETTINGS_STATE_MY.set()
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, f"Что хотите сделать со своими контактами? ", reply_markup=kb.my_info_btn_markup)

@dp.message_handler(lambda msg: not (hasattr(msg, 'callback_data')), state = TestStates.SETTINGS_STATE_MY)
async def process_name_my_settings(message: types.Message, state: FSMContext):
    await message.reply("Выберите что будем делать с контактами!")

########## add
@dp.callback_query_handler(lambda c: c.data == 'add_phon_btn', state = TestStates.SETTINGS_STATE_MY)
async def process_callback_my_settings_add_phone_btn(callback_query: types.CallbackQuery):
    await TestStates.ADD_PHONE_STATE.set()
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, f"Введите номер телефона в формате +79998887766")

@dp.message_handler(lambda msg: not Valid.is_phone(msg.text), state = TestStates.ADD_PHONE_STATE)
async def process_name_phone_not_valid(message: types.Message, state: FSMContext):
    await message.reply(f"Введите номер телефона в формате +79998887766 или отмените ввод", reply_markup=kb.home_btn_markup)

@dp.message_handler(lambda msg: Valid.is_phone(msg.text), state = TestStates.ADD_PHONE_STATE)
async def process_name_valid_phone(message: types.Message, state: FSMContext):
    db = DBHelper()
    await db.add_contact(message.from_user, message.text)
    await TestStates.SETTINGS_STATE.set()
    await message.reply(f"Вы сохранили/обновили номер как свой контакт: \n\n☎️ " + message.text, reply_markup=kb.settings_btn_markup)
    contacts = await db.get_all_data(from_user=message.from_user)
    info_message = await prepare_info_for_message(contacts, message.from_user.mention)
    del db
    await bot.send_message(message.from_user.id, info_message)
    #logging.debug(contacts['contacts'])

########## del
@dp.callback_query_handler(lambda c: c.data == 'del_phon_btn', state = TestStates.SETTINGS_STATE_MY)
async def process_callback_my_settings_btn(callback_query: types.CallbackQuery):
    await TestStates.DEL_PHONE_STATE.set()
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, f"Введите номер телефона для удаления в формате +79998887766")

@dp.message_handler(lambda msg: not Valid.is_phone(msg.text), state = TestStates.DEL_PHONE_STATE)
async def process_name_del_phone_not_valid(message: types.Message, state: FSMContext):
    await message.reply(f"Введите номер телефона в формате +79998887766 или отмените ввод", reply_markup=kb.home_btn_markup)

@dp.message_handler(lambda msg: Valid.is_phone(msg.text), state = TestStates.DEL_PHONE_STATE)
async def process_name_del_valid_phone(message: types.Message, state: FSMContext):
    db = DBHelper()
    await db.del_contact(message.from_user, message.text)
    await TestStates.SETTINGS_STATE.set()
    await message.reply(f"Вы удалили номер из своих контактов: \n\n☎️ " + message.text, reply_markup=kb.settings_btn_markup)
    contacts = await db.get_all_data(from_user=message.from_user)
    info_message = await prepare_info_for_message(contacts, message.from_user.mention)
    del db
    await bot.send_message(message.from_user.id, info_message)

###### CHANGE MM #####################
@dp.callback_query_handler(lambda c: c.data == 'mm_settings_btn', state = TestStates.SETTINGS_STATE)
async def process_callback_mm_settings_btn(callback_query: types.CallbackQuery):
    await TestStates.SETTINGS_STATE_MM.set()
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, f"Что нужно сделать с данными машиноместа?", reply_markup=kb.mm_info_btn_markup)

@dp.message_handler(lambda msg: not (hasattr(msg, 'callback_data')), state = TestStates.SETTINGS_STATE_MM)
async def process_name_mm_settings(message: types.Message, state: FSMContext):
    await message.reply("Выберите что будем делать с данными машиномест!")

########## add
@dp.callback_query_handler(lambda c: c.data == 'add_mm_btn', state = TestStates.SETTINGS_STATE_MM)
async def process_callback_mm_settings_add_btn(callback_query: types.CallbackQuery):
    await TestStates.ADD_MM_STATE.set()
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, f"Введите номер машиноместа (от 1 до 318))")

@dp.message_handler(lambda msg: not Valid.is_mm(msg.text), state = TestStates.ADD_MM_STATE)
async def process_name_mm_not_valid(message: types.Message, state: FSMContext):
    await message.reply(f"Введите номер машиноместа (от 1 до 318) или отмените ввод", reply_markup=kb.home_btn_markup)

@dp.message_handler(lambda msg: Valid.is_mm(msg.text), state = TestStates.ADD_MM_STATE)
async def process_name_valid_mm(message: types.Message, state: FSMContext):
    db = DBHelper()
    await db.add_mm(message.from_user, message.text)
    await TestStates.SETTINGS_STATE.set()
    await message.reply(f"Вы сохранили новое машиноместо: \n\n🅿️ " + message.text, reply_markup=kb.settings_btn_markup)
    park_mm_info = await db.get_all_data(from_user=message.from_user)
    info_message = await prepare_info_for_message(park_mm_info, message.from_user.mention)
    db_mm_list = await db.get_mm_list()
    del db

    await bot.send_message(message.from_user.id, info_message)
    #update html
    pm = ParkMap()
    await pm.draw_map(db_mm_list)  
    del pm

########## del
@dp.callback_query_handler(lambda c: c.data == 'del_mm_btn', state = TestStates.SETTINGS_STATE_MM)
async def process_callback_mm_del_settings_btn(callback_query: types.CallbackQuery):
    await TestStates.DEL_MM_STATE.set()
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, f"Введите номер машиноместа (от 1 до 318))")

@dp.message_handler(lambda msg: not Valid.is_mm(msg.text), state = TestStates.DEL_MM_STATE)
async def process_name_del_mm_not_valid(message: types.Message, state: FSMContext):
    await message.reply(f"Введите номер машиноместа (от 1 до 318)) или отмените ввод", reply_markup=kb.home_btn_markup)

@dp.message_handler(lambda msg: Valid.is_mm(msg.text), state = TestStates.DEL_MM_STATE)
async def process_name_del_valid_mm(message: types.Message, state: FSMContext):
    db = DBHelper()
    await db.del_mm(message.from_user, message.text)
    await TestStates.SETTINGS_STATE.set()
    await message.reply(f"⛔️ Вы удалили машиноместо: \n\n🅿️ " + message.text, reply_markup=kb.settings_btn_markup)
    park_mm_info = await db.get_all_data(from_user=message.from_user)
    info_message = await prepare_info_for_message(park_mm_info, message.from_user.mention)
    db_mm_list = await db.get_mm_list()
    del db
    await bot.send_message(message.from_user.id, info_message)
    #update html
    pm = ParkMap()
    await pm.draw_map(db_mm_list)  
    del pm

###### CHANGE AUTO #####################
@dp.callback_query_handler(lambda c: c.data == 'auto_settings_btn', state = TestStates.SETTINGS_STATE)
async def process_callback_auto_settings_btn(callback_query: types.CallbackQuery):
    await TestStates.SETTINGS_STATE_AU.set()
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, f"Что нужно сделать с данными автомобиля?", reply_markup=kb.auto_info_btn_markup)

@dp.message_handler(lambda msg: not (hasattr(msg, 'callback_data')), state = TestStates.SETTINGS_STATE_AU)
async def process_name_au_settings(message: types.Message, state: FSMContext):
    await message.reply("Выберите что будем делать с номером авто!")

########## add
@dp.callback_query_handler(lambda c: c.data == 'add_auto_btn', state = TestStates.SETTINGS_STATE_AU)
async def process_callback_au_settings_add_btn(callback_query: types.CallbackQuery):
    await TestStates.ADD_AUTO_STATE.set()
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, f"Введите номер автомобиля в формате А123ВС999 (одной строкой без пробелов, язык английский или русский)")

@dp.message_handler(lambda msg: not Valid.is_auto(msg.text), state = TestStates.ADD_AUTO_STATE)
async def process_name_au_not_valid(message: types.Message, state: FSMContext):
    await message.reply(f"Введите номер автомобиля в формате А123ВС999 (одной строкой без пробелов, язык английский или русский) или отмените ввод", reply_markup=kb.home_btn_markup)

@dp.message_handler(lambda msg: Valid.is_auto(msg.text), state = TestStates.ADD_AUTO_STATE)
async def process_name_valid_au(message: types.Message, state: FSMContext):
    db = DBHelper()
    await db.add_auto(message.from_user, Valid.cyrillic2latin(message.text))
    await TestStates.SETTINGS_STATE.set()
    await message.reply(f"Вы сохранили новый автомобиль: \n\n🚗 " + Valid.cyrillic2latin(message.text), reply_markup=kb.settings_btn_markup)
    auto_info = await db.get_all_data(from_user=message.from_user)
    info_message = await prepare_info_for_message(auto_info, message.from_user.mention)
    del db
    await bot.send_message(message.from_user.id, info_message)

########## del
@dp.callback_query_handler(lambda c: c.data == 'del_auto_btn', state = TestStates.SETTINGS_STATE_AU)
async def process_callback_au_del_settings_btn(callback_query: types.CallbackQuery):
    await TestStates.DEL_AUTO_STATE.set()
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, f"Введите номер автомобиля в формате Х123XX777 (одной строкой без пробелов, язык английский или русский)")

@dp.message_handler(lambda msg: not Valid.is_auto(msg.text), state = TestStates.DEL_AUTO_STATE)
async def process_name_del_auto_not_valid(message: types.Message, state: FSMContext):
    await message.reply(f"Введите номер автомобиля в формате А123ВС999 (одной строкой без пробелов, язык английский или русский) или отмените ввод", reply_markup=kb.home_btn_markup)

@dp.message_handler(lambda msg: Valid.is_auto(msg.text), state = TestStates.DEL_AUTO_STATE)
async def process_name_del_valid_auto(message: types.Message, state: FSMContext):
    db = DBHelper()
    await db.del_auto(message.from_user, message.text)
    await TestStates.SETTINGS_STATE.set()
    await message.reply(f"🚶 Вы удалили номер автомобиля: \n\n🚗 " + message.text, reply_markup=kb.settings_btn_markup)
    auto_info = await db.get_all_data(from_user=message.from_user)
    info_message = await prepare_info_for_message(auto_info, message.from_user.mention)
    del db
    await bot.send_message(message.from_user.id, info_message)

############################## MESSAGES ################################
@dp.callback_query_handler(lambda c: c.data == 'messages_btn', state='*')
async def process_callback_messages_btn(callback_query: types.CallbackQuery):
    await TestStates.SEND_MESSAGE_STATE.set()
    taddr.tg_ids = {}
    db = DBHelper()
    db_usr = await db.check_user(callback_query.from_user, callback_query.message.chat.id)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, f"Выберите по какому признаку искать адресата:", reply_markup=kb.messages_types_btn_markup)

@dp.message_handler(lambda msg: not (hasattr(msg, 'callback_data')), state = TestStates.SEND_MESSAGE_STATE)
async def process_name_message_settings(message: types.Message, state: FSMContext):
    await message.reply("Нажимайте кнопки!")

###### MM ###########
@dp.callback_query_handler(lambda c: c.data == 'mm_message_btn', state = TestStates.SEND_MESSAGE_STATE)
async def process_callback_mm_message_btn(callback_query: types.CallbackQuery):
    await TestStates.SEND_MESSAGE_STATE_MM.set()
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, f"Введите номер машиноместа (от 1 до 318))")

@dp.message_handler(lambda msg: not Valid.is_mm(msg.text), state = TestStates.SEND_MESSAGE_STATE_MM)
async def process_name_mm_not_valid(message: types.Message, state: FSMContext):
    await message.reply(f"Введите номер машиноместа (от 1 до 318) или отмените ввод", reply_markup=kb.home_btn_markup)

@dp.message_handler(lambda msg: Valid.is_mm(msg.text), state = TestStates.SEND_MESSAGE_STATE_MM)
async def process_message_valid_mm(message: types.Message, state: FSMContext):
    await TestStates.GET_DIALOG_MESSAGE_STATE.set()
    db = DBHelper()
    all_tg_ids = await db.get_users_mm(message.text)
    logging.info(all_tg_ids)
    info_message = await prepare_tg_info_for_message("ММ №" + message.text, all_tg_ids)
    del db
    if "Не найдено" in info_message:
        await message.reply(info_message, reply_markup=kb.cancel_btn_markup)
        await TestStates.SEND_MESSAGE_STATE.set()
    else:
        await message.reply(info_message, reply_markup=kb.message_btn_markup)
    taddr.tg_ids = all_tg_ids

#COMMON
@dp.message_handler((lambda c: (c.data != 'anonym_btn') and (c.data != 'direct_btn') and (c.data != 'cancel_dialog')), state = TestStates.GET_DIALOG_MESSAGE_STATE)
async def process_message_chose_valid_dialog(message: types.Message, state: FSMContext):
    await message.reply(f"Выберите вариант общения или отмените!", reply_markup=kb.message_btn_markup)

@dp.callback_query_handler(lambda c: c.data == 'anonym_btn', state = TestStates.GET_DIALOG_MESSAGE_STATE) #COMMON
async def process_callback_anonim_message_btn_send(callback_query: types.CallbackQuery):
    await TestStates.DIALOG_MESSAGE_STATE.set()
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, f"Введите текст анонимного сообщения:")

@dp.message_handler(state = TestStates.DIALOG_MESSAGE_STATE) #COMMON
async def process_message_valid_anon_continue(message: types.Message):

    if taddr.tg_ids:
        for tg_user in taddr.tg_ids['contacts']:
            logging.info(tg_user['tg_user_id'])
            db = DBHelper()
            #to_chat_id = await db.get_users_chat(tg_user['tg_user_id'])
            to_chat_id = tg_user['tg_user_id']
            logging.info(to_chat_id)

            if to_chat_id:
                await bot.send_message(tg_user['tg_user_id'], f"🕶 Вам анонимное сообщение:\n\n" + message.text)
                await bot.send_message(to_chat_id, f"Хотите ответить?", reply_markup=kb.message_anon_dialog_btn_markup)
                dialog_state = await db.change_dialog(message.chat.id, to_chat_id, 'direct', "OPEN", "from " + message.from_user.mention)
            else:
                await bot.send_message(message.from_user.id, "Не могу переслать сообщение, не нашел чат с пользователем.", reply_markup=kb.cancel_btn_markup)
            del db
 
        await message.reply(f"Передал анонимно. Пишите еще или останавливайте пересылку.", reply_markup=kb.cancel_btn_markup)
    else:
        await bot.send_message(message.from_user.id, "Не удалось отправить! Не найдены контакты.", reply_markup=kb.cancel_btn_markup)

@dp.callback_query_handler(lambda c: c.data == 'reply_anonym_btn', state = "*") #COMMON
async def process_callback_anonim_reply_message_btn_send(callback_query: types.CallbackQuery):
    await TestStates.DIALOG_MESSAGE_STATE_REPLY.set()
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, f"Пишите ответ:")

@dp.message_handler(state = TestStates.DIALOG_MESSAGE_STATE_REPLY)   #COMMON
async def process_message_valid_anon_continue_reply(message: types.Message):

    db = DBHelper()
    to_chat_id = await db.get_open_user_dialog(message.chat.id)

    if to_chat_id:
        await bot.send_message(to_chat_id, f"🕶 Вам анонимное сообщение:\n\n" + message.text)
        await bot.send_message(to_chat_id, f"Хотите ответить?", reply_markup=kb.message_direct_dialog_btn_markup)
        dialog_state = await db.change_dialog(message.chat.id, to_chat_id, 'direct', "OPEN", "from " + message.from_user.mention)
        await message.reply(f"Отправлено. Пишите еще или останавливайте пересылку.", reply_markup=kb.cancel_btn_markup)
    else:
        await bot.send_message(message.from_user.id, "Не могу переслать сообщение, не нашел открытый чат с пользователем. Попробуйте заново найти его и открыть диалог", reply_markup=kb.cancel_btn_markup)
    del db


@dp.callback_query_handler(lambda c: c.data == 'direct_btn', state = TestStates.GET_DIALOG_MESSAGE_STATE) #COMMON
async def process_callback_forward_message_btn_send_direct(callback_query: types.CallbackQuery):
    await TestStates.DIALOG_MESSAGE_STATE_FORWARD.set()
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, f"Введите текст сообщения (перешлю от вашего имени):")

@dp.message_handler(state = TestStates.DIALOG_MESSAGE_STATE_FORWARD)   #COMMON
async def process_message_valid_direct_continue(message: types.Message):

    if taddr.tg_ids:
        for tg_user in taddr.tg_ids['contacts']: 
            logging.info(tg_user['tg_user_id'])
            db = DBHelper()
            #to_chat_id = await db.get_users_chat(tg_user['tg_user_id'])
            to_chat_id = tg_user['tg_user_id']
            logging.info(to_chat_id)
            
            if to_chat_id:
                await bot.forward_message(to_chat_id, message.chat.id, message.message_id, False)

                await bot.send_message(to_chat_id, f"Хотите ответить?", reply_markup=kb.message_direct_dialog_btn_markup)
                dialog_state = await db.change_dialog(message.chat.id, to_chat_id, 'direct', "OPEN", "from " + message.from_user.mention)
            else:
                await bot.send_message(message.from_user.id, "Не могу переслать сообщение, не нашел чат с пользователем. Пробуйте анонимку.", reply_markup=kb.cancel_btn_markup)
            del db

        await message.reply(f"Переслал ваше сообщение. Пишите еще или останавливайте пересылку.", reply_markup=kb.cancel_btn_markup)
    else:
        await bot.send_message(message.from_user.id, "Не удалось отправить! Не найдены контакты.", reply_markup=kb.cancel_btn_markup)

@dp.callback_query_handler(lambda c: c.data == 'cancel_dialog', state='*')
async def process_callback_cancel_dialog_btn(callback_query: types.CallbackQuery):
    await TestStates.SEND_MESSAGE_STATE.set()
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, f"Выберите как искать адресата:", reply_markup=kb.messages_types_btn_markup)
    if taddr.tg_ids:
        for tg_user in taddr.tg_ids['contacts']: 
            logging.info(tg_user['tg_user_id'])
            db = DBHelper()
            to_chat_id = tg_user['tg_user_id']
            dialog_state = await db.change_dialog(callback_query.message.chat.id, to_chat_id, 'cancel', "CLOSED", "close " + callback_query.from_user.mention)
            del db
    taddr.tg_ids = {}

@dp.callback_query_handler(lambda c: c.data == 'reply_direct_btn', state = "*") #COMMON
async def process_callback_reply_direct_message_btn_send(callback_query: types.CallbackQuery):
    await TestStates.DIALOG_MESSAGE_STATE_FORWARD_REPLY.set()
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, f"Пишите ответ:")

@dp.message_handler(state = TestStates.DIALOG_MESSAGE_STATE_FORWARD_REPLY)   #COMMON
async def process_message_valid_direct_continue_reply(message: types.Message):

    db = DBHelper()
    to_chat_id = await db.get_open_user_dialog(message.chat.id)

    if to_chat_id:
        await bot.forward_message(to_chat_id, message.chat.id, message.message_id, False)

        await bot.send_message(to_chat_id, f"Хотите ответить?", reply_markup=kb.message_direct_dialog_btn_markup)
        dialog_state = await db.change_dialog(message.chat.id, to_chat_id, 'direct', "OPEN", "from " + message.from_user.mention)
        await message.reply(f"Переслал ваше сообщение. Пишите еще или останавливайте пересылку.", reply_markup=kb.cancel_btn_markup)
    else:
        await bot.send_message(message.from_user.id, "Не могу переслать сообщение, не нашел открытый чат с пользователем. Попробуйте заново найти его и открыть диалог", reply_markup=kb.cancel_btn_markup)
    del db

###### AUTO ###########
@dp.callback_query_handler(lambda c: c.data == 'auto_message_btn', state = TestStates.SEND_MESSAGE_STATE)
async def process_callback_auto_message_btn(callback_query: types.CallbackQuery):
    await TestStates.SEND_MESSAGE_STATE_AU.set()
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, f"Введите номер автомобиля в формате А123ВС999 (одной строкой без пробелов, язык английский или русский)")

@dp.message_handler(lambda msg: not Valid.is_auto(msg.text), state = TestStates.SEND_MESSAGE_STATE_AU)
async def process_name_au_message_not_valid(message: types.Message, state: FSMContext):
    await message.reply(f"Введите номер автомобиля в формате А123ВС999 (одной строкой без пробелов, язык английский или русский) или отмените ввод", reply_markup=kb.home_btn_markup)

@dp.message_handler(lambda msg: Valid.is_auto(msg.text), state = TestStates.SEND_MESSAGE_STATE_AU)
async def process_message_valid_mm(message: types.Message, state: FSMContext):
    await TestStates.GET_DIALOG_MESSAGE_STATE.set()
    db = DBHelper()
    logging.info(message.text)
    logging.info(Valid.cyrillic2latin(message.text))
    all_tg_ids = await db.get_users_auto(Valid.cyrillic2latin(message.text))
    logging.info(all_tg_ids)
    info_message = await prepare_tg_info_for_message("AUTO №" + message.text, all_tg_ids)
    del db
    if "Не найдено" in info_message:
        await message.reply(info_message, reply_markup=kb.cancel_btn_markup)
        await TestStates.SEND_MESSAGE_STATE.set()
    else:
        await message.reply(info_message, reply_markup=kb.message_btn_markup)
    taddr.tg_ids = all_tg_ids

###### PHONE ###########
@dp.callback_query_handler(lambda c: c.data == 'phone_message_btn', state = TestStates.SEND_MESSAGE_STATE)
async def process_callback_phone_message_btn(callback_query: types.CallbackQuery):
    await TestStates.SEND_MESSAGE_STATE_MY.set()
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, f"Введите номер телефона в формате +79998887766")

@dp.message_handler(lambda msg: not Valid.is_phone(msg.text), state = TestStates.SEND_MESSAGE_STATE_MY)
async def process_name_phone_not_valid(message: types.Message, state: FSMContext):
    await message.reply(f"Введите номер телефона в формате +79998887766 или отмените ввод", reply_markup=kb.home_btn_markup)

@dp.message_handler(lambda msg: Valid.is_phone(msg.text), state = TestStates.SEND_MESSAGE_STATE_MY)
async def process_message_valid_phone(message: types.Message, state: FSMContext):
    await TestStates.GET_DIALOG_MESSAGE_STATE.set()
    db = DBHelper()
    all_tg_ids = await db.get_users_phone(message.text)
    logging.info(all_tg_ids)
    info_message = await prepare_tg_info_for_message("PHONE №" + message.text, all_tg_ids)
    del db
    if "Не найдено" in info_message:
        await message.reply(info_message, reply_markup=kb.cancel_btn_markup)
        await TestStates.SEND_MESSAGE_STATE.set()
    else:
        await message.reply(info_message, reply_markup=kb.message_btn_markup)
    taddr.tg_ids = all_tg_ids

############################## INFO ################################
@dp.callback_query_handler(lambda c: c.data == 'info_btn', state='*')
async def process_callback_messages_btn(callback_query: types.CallbackQuery):
    await TestStates.INFO_STATE.set()
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, f"Выберите вид статистики:", reply_markup=kb.common_btn_markup)

@dp.callback_query_handler(lambda c: c.data == 'common_cntrs_btn', state = TestStates.INFO_STATE)
async def process_callback_auto_message_btn(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    db = DBHelper()
    db_info = await db.get_common_data()
    logging.info(db_info)
    info_message = await prepare_common_info_for_message(db_info)
    del db

    await bot.send_message(callback_query.from_user.id, info_message, reply_markup=kb.common_btn_markup)

@dp.callback_query_handler(lambda c: c.data == 'common_map_btn', state = TestStates.INFO_STATE)
async def process_callback_auto_message_btn(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    map_link = await prepare_mm_map_for_message()
    await bot.send_message(callback_query.from_user.id, map_link, reply_markup=kb.common_btn_markup)

    # db = DBHelper()
    # db_mm_list = await db.get_mm_list()
    # if db_mm_list:
    #     map_link = await prepare_mm_map_for_message(db_mm_list)
    #     await bot.send_message(callback_query.from_user.id, map_link, reply_markup=kb.common_btn_markup)
    # else:
    #     await bot.send_message(callback_query.from_user.id, 'Что-то пошло не так :(', reply_markup=kb.home_btn_markup)
    # del db

@dp.message_handler(lambda msg: not (hasattr(msg, 'callback_data')), state = TestStates.INFO_STATE)
async def process_name_start(message: types.Message, state: FSMContext):
    await message.reply("Выберите пункт меню!")

######################################################################
# @dp.message_handler()
# async def echo_message(msg: types.Message):
#     await bot.send_message(msg.from_user.id, msg.text)

@dp.callback_query_handler(state = "*")
async def process_callback_default(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, f"Не понял Вас. Попробуйте сначала!")

async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()

############################## INFO ####################################
async def prepare_info_for_message(dataset, user=""):
    if (user == ""):
        user = "@******"
    message = f"Существующие данные {user}:\n\n".format(user)
    if dataset:
        for dtype in dataset:
            #message += "" + dtype + ":\n"
            for arrelem in dataset[dtype]:
                for elem in arrelem:
                    if dtype == "contacts": 
                        if elem == "phone":
                            message += "📞 " + str(arrelem[elem]) + "\n"
                    if dtype == "park_mm": 
                        if elem == "park_mm":
                            message += "🅿️ " + str(arrelem[elem]) + "\n"
                    if dtype == "cars": 
                        if elem == "car_number":
                            message += "🚘 " + str(arrelem[elem]) + "\n"

    return message

async def prepare_common_info_for_message(dataset):
    message = f"Всего зарегистрировано у бота:\n\n"
    if dataset:
        for dtype in dataset:
            #message += "" + dtype + ":\n"
            for arrelem in dataset[dtype]:
                for elem in arrelem:
                    if dtype == "users": 
                        message += "🙍🏼‍♂️ " + str(arrelem[elem]) + " пользователя(-ей)\n"
                    if dtype == "contacts": 
                        message += "📞 " + str(arrelem[elem]) + " номера(-ов)\n"
                    if dtype == "park_mm": 
                        message += "🅿️ " + str(arrelem[elem]) + " мест(-а)\n"
                    if dtype == "cars": 
                        message += "🚘 " + str(arrelem[elem]) + " авто номера(-ов)\n"

    return message

async def prepare_mm_map_for_message():
    message = f"Карта паркинга. Цветом отмечены места, которые зарегистрированы у бота. Им можно написать сообщение по номеру машиноместа.\n\n"
    message += await ParkMap.show_map()  
    return message

async def prepare_tg_info_for_message(key, dataset):
    message = f"Контанты для {key}:\n\n".format(key)
    found = False
    if dataset:
        for dtype in dataset:
            #message += "" + dtype + ":\n"
            for arrelem in dataset[dtype]:
                for elem in arrelem:
                    if dtype == "contacts": 
                        if elem == "tg_mention":
                            if (str(arrelem[elem])) == 'None':
                                message += "▶️ Скрыто настройками безопасности\n"
                            else:
                                message += "▶️ " + str(arrelem[elem]) + "\n"
                            found = True
    if not found:
        message += "Не найдено такой информации у бота."
    else:
        message += "\nМожете написать напрямую, либо отправить сообщение анонимно через бота. Анонимно бот умеет отправлять даже если у пользователя скрыт логин @login, но он зарегистрирован."
    return message

def main():
    executor.start_polling(dp, on_shutdown=shutdown)

if __name__ == '__main__':
    main()