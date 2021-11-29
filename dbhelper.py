
#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import logging

from aiogram.types import chat
from dbdriver import DBDriver
from aiogram import Bot, types
from aiogram.dispatcher import FSMContext
import hashlib
from datetime import datetime

class DBHelper:

    dbdriver = None
    from_user = None

    def __init__(self):
        self.dbdriver = DBDriver()

        if not self.dbdriver:
            logging.info("DBDriver was not created")
            return None

    def __del__(self):
        if self.dbdriver:
            del self.dbdriver
    
    async def check_user(self, from_user: types.User, chat_id: int):

        if not from_user:
            logging.error("NO USER!")
            return None

        logging.info("***check_user***")
        logging.info(from_user) 

        if getattr(from_user, 'mention') is None:
            logging.info('hide user') 
            from_user.mention = ""

        if from_user.is_bot:
            logging.error("THIS IS BOT!")
            return None

        self.from_user = from_user

        if not self.dbdriver:
            logging.error("DB DRIVER IS NOT FOUND!")
            return None

        select_id_query = "SELECT * FROM users WHERE tg_user_id = {id}".format(id = self.from_user.id)
        logging.info("FIND USER: " + str(select_id_query)) 
        user_row = self.dbdriver.select_query(query=select_id_query, qtype='all')
        logging.info(user_row) 

        if not user_row:
            insert_user_query = "INSERT INTO users (tg_user_id, first_name, last_name, is_in_chat, tg_mention, tg_chat_id) " + \
                " VALUES ({tg_user_id}, '{first_name}', '{last_name}', '{is_in_chat}', '{tg_mention}', {tg_chat_id}) ON CONFLICT DO NOTHING" \
                .format(tg_user_id = from_user.id, \
                    first_name = from_user.first_name, \
                    last_name = from_user.last_name, \
                    is_in_chat = True, \
                    tg_mention = from_user.mention, \
                    tg_chat_id = chat_id
                    )
            logging.info(str(insert_user_query)) 
            self.dbdriver.insert_query(insert_user_query)   
            user_row = self.dbdriver.select_query(query=select_id_query, qtype='all')
        else:
            logging.info("USER " + str(from_user.mention) + ", id=" + str(user_row[0]['id'])) 
            #TODO: проверку хеша и апдейт данных в базе
            user_row = self.dbdriver.select_query(query=select_id_query, qtype='all')
            # if user_row[0]['tg_chat_id'] is None:
            #     update_user_query = "UPDATE users SET tg_chat_id = {tg_chat_id} WHERE tg_user_id = {tg_user_id}" \
            #         .format(tg_chat_id = chat_id, tg_user_id = from_user.id)
            #     logging.info(str(update_user_query)) 
            #     self.dbdriver.update_query(update_user_query)   
            #     user_row = self.dbdriver.select_query(query=select_id_query, qtype='all')

        #logging.info("USER IN DB WITH ID = " + str(user_row['id'])) 
        return user_row

    ################# CONTACTS #################
    async def change_contacts(self, from_user: types.User, phone: str, crud: str):

        logging.info("mention " + str(from_user.mention))

        if not from_user:
            logging.error("NO USER!")
            return None

        if from_user.is_bot:
            logging.error("THIS IS BOT!")
            return None

        self.from_user = from_user

        if not self.dbdriver:
            logging.error("DB DRIVER IS NOT FOUND!")
            return None

        contact_query = None
        if crud == 'add':
            contact_query = "INSERT INTO contacts (tg_user_id, phone) VALUES ({tg_user_id}, '{phone}') ON CONFLICT DO NOTHING" \
                    .format(tg_user_id = self.from_user.id, phone = phone)
            logging.info(str(contact_query)) 
            self.dbdriver.insert_query(contact_query)   
        if crud == 'del':
            contact_query = "DELETE FROM contacts WHERE tg_user_id='{tg_user_id}' AND phone='{phone}'" \
                    .format(tg_user_id = self.from_user.id, phone = phone)
            logging.info(str(contact_query)) 
            self.dbdriver.delete_query(contact_query)  

        all_data = await self.get_all_data(from_user=from_user, datatype='contacts')
        return all_data

    async def add_contact(self, from_user: types.User, phone: str):
        return await self.change_contacts(from_user=from_user, phone=phone, crud='add')

    async def del_contact(self, from_user: types.User, phone: str):
        return await self.change_contacts(from_user=from_user, phone=phone, crud='del')

    async def get_users_phone(self, phone: str):

        dbdata = {}

        if not self.dbdriver:
            logging.error("DB DRIVER IS NOT FOUND!")
            return None

        select_id_query = "SELECT p.tg_user_id as tg_user_id, u.tg_mention as tg_mention " + \
            "FROM contacts AS p LEFT JOIN users AS u on p.tg_user_id = u.tg_user_id " + \
            "WHERE phone = '{phone}'".format(phone = phone)
            
        user_row = self.dbdriver.select_query(query=select_id_query, qtype='all')
        dbdata['contacts'] = user_row

        return dbdata    
    

    ################## MM #######################
    async def change_mm(self, from_user: types.User, park_mm: str, crud: str):

        logging.info("mention " + str(from_user.mention))

        if not from_user:
            logging.error("NO USER!")
            return None

        if from_user.is_bot:
            logging.error("THIS IS BOT!")
            return None

        self.from_user = from_user

        if not self.dbdriver:
            logging.error("DB DRIVER IS NOT FOUND!")
            return None

        contact_query = None
        if crud == 'add':
            contact_query = "INSERT INTO park_mm (tg_user_id, park_mm) VALUES ({tg_user_id}, '{park_mm}') ON CONFLICT DO NOTHING" \
                    .format(tg_user_id = self.from_user.id, park_mm = park_mm)
            logging.info(str(contact_query)) 
            self.dbdriver.insert_query(contact_query)   
        if crud == 'del':
            contact_query = "DELETE FROM park_mm WHERE tg_user_id='{tg_user_id}' AND park_mm='{park_mm}'" \
                    .format(tg_user_id = self.from_user.id, park_mm = park_mm)
            logging.info(str(contact_query)) 
            self.dbdriver.delete_query(contact_query)  

        all_data = await self.get_all_data(from_user=from_user, datatype='park_mm')
        return all_data

    async def add_mm(self, from_user: types.User, park_mm: str):
        return await self.change_mm(from_user=from_user, park_mm=park_mm, crud='add')

    async def del_mm(self, from_user: types.User, park_mm: str):
        return await self.change_mm(from_user=from_user, park_mm=park_mm, crud='del')

    async def get_users_mm(self, park_mm: str):

        dbdata = {}

        if not self.dbdriver:
            logging.error("DB DRIVER IS NOT FOUND!")
            return None

        select_id_query = "SELECT p.tg_user_id as tg_user_id, u.tg_mention as tg_mention " + \
            "FROM park_mm AS p LEFT JOIN users AS u on p.tg_user_id = u.tg_user_id " + \
            "WHERE park_mm = {mm}".format(mm = park_mm)

        user_row = self.dbdriver.select_query(query=select_id_query, qtype='all')
        dbdata['contacts'] = user_row

        return dbdata

    ################## AUTO #######################
    async def change_auto(self, from_user: types.User, car_number: str, crud: str):

        logging.info(car_number)

        if not from_user:
            logging.error("NO USER!")
            return None

        if from_user.is_bot:
            logging.error("THIS IS BOT!")
            return None

        self.from_user = from_user

        if not self.dbdriver:
            logging.error("DB DRIVER IS NOT FOUND!")
            return None

        contact_query = None
        if crud == 'add':
            contact_query = "INSERT INTO cars (tg_user_id, car_number) VALUES ({tg_user_id}, '{car_number}') ON CONFLICT DO NOTHING" \
                    .format(tg_user_id = self.from_user.id, car_number = car_number.upper())
            logging.info(str(contact_query)) 
            self.dbdriver.insert_query(contact_query)   
        if crud == 'del':
            contact_query = "DELETE FROM cars WHERE tg_user_id='{tg_user_id}' AND car_number='{car_number}'" \
                    .format(tg_user_id = self.from_user.id, car_number = car_number.upper())
            logging.info(str(contact_query)) 
            self.dbdriver.delete_query(contact_query)  

        all_data = await self.get_all_data(from_user=from_user, datatype='cars')
        return all_data

    async def add_auto(self, from_user: types.User, car_number: str):
        return await self.change_auto(from_user=from_user, car_number=car_number, crud='add')

    async def del_auto(self, from_user: types.User, car_number: str):
        return await self.change_auto(from_user=from_user, car_number=car_number, crud='del')

    async def get_users_auto(self, car_number: str):

        dbdata = {}

        if not self.dbdriver:
            logging.error("DB DRIVER IS NOT FOUND!")
            return None

        select_id_query = "SELECT p.tg_user_id as tg_user_id, u.tg_mention as tg_mention " + \
            "FROM cars AS p LEFT JOIN users AS u on p.tg_user_id = u.tg_user_id " + \
            "WHERE p.car_number = '{carnumber}'".format(carnumber = car_number)
        logging.info(select_id_query)
        user_row = self.dbdriver.select_query(query=select_id_query, qtype='all')
        dbdata['contacts'] = user_row
        logging.info(user_row)
        return dbdata    

    ############# all data ######################
    async def get_all_data(self, from_user: types.User, datatype = 'all'):

        tg_user_id = from_user.id
        logging.info("INFO FOR USER " + str(tg_user_id))

        dbdata = dict()

        if not self.dbdriver:
            logging.error("DB DRIVER IS NOT FOUND!")
            return None

        if datatype in ['users','all']:
            select_id_query = "SELECT * FROM users WHERE tg_user_id = {tg_user_id}".format(tg_user_id = tg_user_id)
            user_row = self.dbdriver.select_query(query=select_id_query, qtype='one')

            if not user_row:
                logging.info("USER " + str(tg_user_id) + " NOT FOUND") 
                return None
                
            logging.info(user_row) 
            dbdata['users'] = user_row

        if datatype in ['contacts','all']: 

                select_contacts_query = "SELECT * FROM contacts WHERE tg_user_id = {tg_user_id}".format(tg_user_id = tg_user_id)
                contacts_row = self.dbdriver.select_query(query=select_contacts_query, qtype='all')
                logging.info(contacts_row) 
                dbdata['contacts'] = contacts_row

        if datatype in ['park_mm','all']: 

                select_park_mm_query = "SELECT * FROM park_mm WHERE tg_user_id = {tg_user_id}".format(tg_user_id = tg_user_id)
                park_mm_row = self.dbdriver.select_query(query=select_park_mm_query, qtype='all')
                logging.info(park_mm_row) 
                dbdata['park_mm'] = park_mm_row

        if datatype in ['cars','all']: 

                select_cars_query = "SELECT * FROM cars WHERE tg_user_id = {tg_user_id}".format(tg_user_id = tg_user_id)
                cars_row = self.dbdriver.select_query(query=select_cars_query, qtype='all')
                logging.info(cars_row) 
                dbdata['cars'] = cars_row

        logging.info(dbdata) 
        return dbdata

    async def get_users_chat(self, tg_user_id):

        if not self.dbdriver:
            logging.error("DB DRIVER IS NOT FOUND!")
            return None

        select_id_query = "SELECT tg_chat_id FROM users WHERE tg_user_id = {tg_user_id}".format(tg_user_id = tg_user_id)

        user_row = self.dbdriver.select_query(query=select_id_query, qtype='all')

        if isinstance(user_row[0]['tg_chat_id']):
            return user_row[0]['tg_chat_id']
        else:
            return None

    async def get_common_data(self, datatype = 'all'):

        logging.info("GET INFO " + str(datatype))

        dbdata = dict()

        if not self.dbdriver:
            logging.error("DB DRIVER IS NOT FOUND!")
            return None

        if datatype in ['users','all']:
            select_user_count_query = "SELECT COUNT(*) as CNT FROM users "
            user_cnt_row = self.dbdriver.select_query(query=select_user_count_query, qtype='one')

            if not user_cnt_row:
                logging.error("Cannot fetch data") 
                return None
                
            logging.info(user_cnt_row) 
            dbdata['users'] = user_cnt_row

        if datatype in ['contacts','all']: 

                select_contacts_cnt_query = "SELECT COUNT(*) as CNT FROM contacts"
                contacts_cnt_row = self.dbdriver.select_query(query=select_contacts_cnt_query, qtype='one')
                logging.info(contacts_cnt_row) 
                dbdata['contacts'] = contacts_cnt_row

        if datatype in ['park_mm','all']: 

                select_park_mm_cnt_query = "SELECT COUNT(*) as CNT FROM park_mm "
                park_mm_cnt_row = self.dbdriver.select_query(query=select_park_mm_cnt_query, qtype='all')
                logging.info(park_mm_cnt_row) 
                dbdata['park_mm'] = park_mm_cnt_row

        if datatype in ['cars','all']: 

                select_cars_cnt_query = "SELECT COUNT(*) as CNT FROM cars "
                cars_cnt_row = self.dbdriver.select_query(query=select_cars_cnt_query, qtype='all')
                logging.info(cars_cnt_row) 
                dbdata['cars'] = cars_cnt_row

        logging.info(dbdata) 
        return dbdata

    ############# messages ######################
    async def change_dialog(self, from_tg_user_id: int, to_tg_user_id: int,
                    chat_type: str, dialog_state: str, message_text = ""):

        logging.info("change_dialog " + str(from_tg_user_id) + " <-> " + str(to_tg_user_id) + " (" + chat_type + ":" + dialog_state + ")")

        if not self.dbdriver:
            logging.error("DB DRIVER IS NOT FOUND!")
            return None

        select_from_id_query = "SELECT tg_user_id FROM users WHERE tg_user_id = {id}".format(id = from_tg_user_id)
        logging.info("FIND FROM USER: " + str(select_from_id_query)) 
        user_from_row = self.dbdriver.select_query(query=select_from_id_query, qtype='one')
        logging.info(user_from_row) 

        if not user_from_row:
            logging.error("NO FROM USER!")
            return None

        select_to_id_query = "SELECT tg_user_id FROM users WHERE tg_user_id = {id}".format(id = from_tg_user_id)
        logging.info("FIND TO USER: " + str(select_to_id_query)) 
        user_to_row = self.dbdriver.select_query(query=select_to_id_query, qtype='one')
        logging.info(user_to_row) 

        if not user_to_row:
            logging.error("NO TO USER!")
            return None

        hash_object = hashlib.sha1(str(from_tg_user_id + to_tg_user_id))
        hex_dig = hash_object.hexdigest()

        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

        dialog_from_query = "INSERT INTO messages (from_tg_user_id, to_tg_user_id, chat_type, dialog_state, message)" + \
            " VALUES ({from_tg_user_id}, {to_tg_user_id}, '{hex_dig}', '{chat_type}', '{dialog_state}', '{message}') " + \
            " ON CONFLICT (hex_dig) " + \
            " DO UPDATE " + \
            " SET from_tg_user_id = {from_tg_user_id}, " + \
            "    to_tg_user_id = {to_tg_user_id}, " + \
            "    hex_dig = '{hex_dig}', " + \
            "    chat_type = '{chat_type}', " + \
            "    dialog_state = '{dialog_state}', " + \
            "    message = CONCAT(message, '=>{dt_string}::', '{message}') " \
                .format(from_tg_user_id = from_tg_user_id, to_tg_user_id = to_tg_user_id, \
                    chat_type = chat_type, dialog_state = dialog_state, dt_string = dt_string, message = message_text)
        logging.info(dialog_from_query)
        self.dbdriver.insert_query(dialog_from_query)   
        dialog_state = await self.get_dialog_state(from_tg_user_id: int, to_tg_user_id: int)
        return dialog_state

    async def get_dialog_state(self, from_tg_user_id: int, to_tg_user_id: int):

        hash_object = hashlib.sha1(str(from_tg_user_id + to_tg_user_id))
        hex_dig = hash_object.hexdigest()
        logging.info("get_dialog_state " + str(hex_dig))       

        if not self.dbdriver:
            logging.error("DB DRIVER IS NOT FOUND!")
            return None

        select_hex_dig_query = "SELECT dialog_state FROM messages WHERE hex_dig = {hex_dig}".format(hex_dig = hex_dig)
        logging.info("hex_dig_row: " + str(select_hex_dig_query)) 
        hex_dig_row = self.dbdriver.select_query(query=select_hex_dig_query, qtype='one')
        logging.info(hex_dig_row) 

        if not hex_dig_row:
            logging.error("NO hex_dig found!")
            return None

        return hex_dig_row[0]['dialog_state']

