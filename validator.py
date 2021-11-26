
#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import logging

class Valid:

    @staticmethod
    def cyrillic2latin(input):

        symbols = (u"АВЕКМНОРСТУХ",
                   u"ABEKMHOPCTYX")

        tr = {ord(a): ord(b) for a, b in zip(*symbols)}
        logging.info(input.translate(tr))
        return input.translate(tr)

    @staticmethod
    def prepare_number(number):
        number = str(number).strip().upper()
        number = Valid.cyrillic2latin(number)
        return number

    @staticmethod
    def is_phone(phone_string):
        phone_string = str(phone_string).strip()
        logging.info(phone_string)
        phone_pattern = re.compile("^(\+7)?[0-9]{10}$")
        
        return phone_pattern.match(phone_string)

    @staticmethod
    def is_mm(mm):
        logging.info(mm)

        if not mm.isdigit():
            return False

        if (1 <= int(mm) <= 318):
            return True

        return False

    @staticmethod
    def is_auto(auto):

        auto = Valid.prepare_number(auto)

        logging.info("################## NUMBER: " + str(auto) + " ########################")

        auto_pattern = re.compile("^[ABEKMHOPCTYXАВЕКМНОРСТУХ]\d{3}[ABEKMHOPCTYXАВЕКМНОРСТУХ]{2}\d{2,3}$")
        
        return auto_pattern.match(auto)

