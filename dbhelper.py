
#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import logging

from aiogram.types import chat
from dbdriver import DBDriver
from aiogram import Bot, types
from aiogram.dispatcher import FSMContext

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
    
    async def check_user(self, message):

        from_user = message.from_user

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
                    tg_chat_id = message.chat.id
                    )
            logging.info(str(insert_user_query)) 
            self.dbdriver.insert_query(insert_user_query)   
            user_row = self.dbdriver.select_query(query=select_id_query, qtype='all')
        else:
            logging.info("USER " + str(from_user.mention) + ", id=" + str(user_row[0]['id'])) 
            #TODO: проверку хеша и апдейт данных в базе
            user_row = self.dbdriver.select_query(query=select_id_query, qtype='all')
            if not user_row['tg_chat_id']:
                update_user_query = "UPDATE users SET tg_user_id = {tg_user_id}, first_name = '{first_name}', last_name = '{last_name}', " + \
                    " is_in_chat = '{is_in_chat}', tg_mention = '{tg_mention}', tg_chat_id = {tg_chat_id} WHERE tg_user_id = {tg_user_id}" \
                    .format(tg_user_id = from_user.id, \
                        first_name = from_user.first_name, \
                        last_name = from_user.last_name, \
                        is_in_chat = True, \
                        tg_mention = from_user.mention, \
                        tg_chat_id = message.chat.id
                        )
                logging.info(str(update_user_query)) 
                self.dbdriver.update_query(update_user_query)   
                user_row = self.dbdriver.select_query(query=select_id_query, qtype='all')

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
            contact_query = "INSERT INTO cars (tg_user_id, car_number) VALUES ({tg_user_id}, '{car_number}') ON CONFLICT DO NOTHING" \
                    .format(tg_user_id = self.from_user.id, car_number = car_number)
            logging.info(str(contact_query)) 
            self.dbdriver.insert_query(contact_query)   
        if crud == 'del':
            contact_query = "DELETE FROM cars WHERE tg_user_id='{tg_user_id}' AND car_number='{car_number}'" \
                    .format(tg_user_id = self.from_user.id, car_number = car_number)
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
            "WHERE car_number = '{car_number}'".format(car_number = car_number)
            
        user_row = self.dbdriver.select_query(query=select_id_query, qtype='all')
        dbdata['contacts'] = user_row

        return dbdata    

    ############# all data ######################
    async def get_all_data(self, tg_user_id: types.User, datatype = 'all'):

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

        if isinstance(user_row['tg_chat_id']):
            return user_row['tg_chat_id']
        else:
            return None