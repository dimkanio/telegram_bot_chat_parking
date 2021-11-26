#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import logging
from config import DBPATH
import psycopg2
from psycopg2.extras import DictCursor
from psycopg2.extras import NamedTupleCursor
from config import DATABASE_URL


class DBDriver:

    dbpath = ''
    connection = None
    cursor = None

    def __del__(self):
        self.path = ''
        if self.connection is not None:
            self.connection.close()
            logging.info('Database connection closed.')

    def _execute_query(self, query):

        cursor_data = None
        output = []

        try:
            self.connection = psycopg2.connect(DATABASE_URL)
            with self.connection.cursor(cursor_factory=DictCursor) as cur:
                cur.execute(query)
                self.connection.commit()
                logging.info("*************Query executed successfully*************************")
                colnames = [desc[0] for desc in cur.description]
                cursor_data = cur.fetchall()
                
                if cursor_data:
                    logging.info(cursor_data)
                    for row in cursor_data:
                        dictdata = dict()
                        for col in colnames:
                            dictdata[col] = row[col]
                        output.append(dictdata)

        except (Exception, psycopg2.DatabaseError) as error:
            logging.error(f"The error '{error}' occurred")
        finally:
            if self.connection is not None:
                self.connection.close()
                logging.info('Database connection closed.')

        return output

    def select_query(self, query, qtype =  'all'):

        out_list = []
        results = self._execute_query(query)

        logging.info(results)

        if results:
            for r in results:
                out_list.append(r)
        else:
            logging.error(f"fetchall RESULTS ARE EMPTY") 
            logging.error(results) 

        logging.info(out_list)
        return out_list

    def insert_query(self, query):
        self._execute_query(query)

    def delete_query(self, query):
        self._execute_query(query)

    def update_query(self, query):
        self._execute_query(query)


        





