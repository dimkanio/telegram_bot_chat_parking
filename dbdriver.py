#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import sqlite3
from sqlite3 import Error
import logging
from config import DBPATH
import os.path


class DBDriver:

    connection = None
    dbpath = ''

    def __init__(self):
        if not os.path.exists(DBPATH):
                raise ValueError("db not found: " + str(DBPATH))
        self.dbpath = DBPATH
        self.connection = self._create_connection()
        if self.connection:
            self.connection.row_factory = sqlite3.Row
            self.cursor = self.connection.cursor()
            

    def __del__(self):
        self.path = ''
        if self.connection:
            self.connection.close()

    def _create_connection(self):
        try:
            self.connection = sqlite3.connect(self.dbpath)
            logging.info("Connection to SQLite DB successful:" +  self.dbpath)
        except Error as e:
            logging.error(f"The error '{e}' occurred")

        return self.connection

    def _execute_query(self, query):
        if self.connection is not None:
            try:
                self.cursor.execute(query)
                logging.info("Query executed successfully")
            except Error as e:
                logging.error(f"The error '{e}' occurred")
        else:
            logging.error(f"Connection is empty!")

    def dict_factory(self, rows):
        d = {}
        for idx, col in enumerate(self.cursor.description):
            d[col[0]] = rows[idx]
        return d

    def select_query(self, query, qtype =  'all'):

        out_list = []
        self._execute_query(query)

        if qtype == 'all':
            results = self.cursor.fetchall()
            if results:
                for r in results:
                    logging.info(dict(r))
                    out_list.append(dict(r))
            else:
                logging.error(f"fetchall RESULTS ARE EMPTY") 
                logging.error(results) 
            
        if qtype == 'one':
            results = self.cursor.fetchone()
            
            if results:
                out_list.append(dict(results))
            else:
                logging.error(f"fetchone RESULTS ARE EMPTY") 
                logging.error(results) 

        logging.info(out_list)
        return out_list

    def insert_query(self, query):
        self._execute_query(query)
        self.connection.commit()

    def delete_query(self, query):
        self._execute_query(query)
        self.connection.commit()

    def update_query(self, query):
        self._execute_query(query)
        self.connection.commit()

        





