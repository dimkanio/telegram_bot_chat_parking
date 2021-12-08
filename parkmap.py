import pandas as pd
from os import remove
import re
from config import HOME_URL
import logging

class ParkMap:

    park_data = []
    asc_columns = [4,7,10,13,16,19,22]
    desc_columns = [5,8,11,14,17,20]
    blank_columns = [3,6,9,12,15,18,21]
    HTML_FILE = 'map.html'

    parking = list(range(1,319,1))
    last_num = 0

    def _build_map(self):
        for col in range(3,23,1):
            for row in range(1,12,1):
                if col in self.asc_columns:
                    mm_cell = {}
                    mm_cell['row'] = row
                    mm_cell['column'] = col
                    last_num = self.parking.pop(0)
                    mm_cell['parking'] = last_num
                    mm_cell['busy'] = 0
                    mm_cell['rent'] = 0
                    self.park_data.append(mm_cell)
                if col in self.desc_columns:
                    mm_cell = {}
                    mm_cell['row'] = 12 - row
                    mm_cell['column'] = col
                    last_num = self.parking.pop(0)
                    mm_cell['parking'] = last_num
                    mm_cell['busy'] = 0
                    mm_cell['rent'] = 0
                    self.park_data.append(mm_cell)

        for col in range(24,3,-1):
            for row in range(14,25,1):
                if col in self.asc_columns:
                    mm_cell = {}
                    mm_cell['row'] = row
                    mm_cell['column'] = col
                    last_num = self.parking.pop(0)
                    mm_cell['parking'] = last_num
                    mm_cell['busy'] = 0
                    mm_cell['rent'] = 0
                    self.park_data.append(mm_cell)
                if col in self.desc_columns:
                    mm_cell = {}
                    mm_cell['row'] = 38 - row
                    mm_cell['column'] = col
                    last_num = self.parking.pop(0)
                    mm_cell['parking'] = last_num
                    mm_cell['busy'] = 0
                    mm_cell['rent'] = 0
                    self.park_data.append(mm_cell)

        for row in range(24,6,-1):
            for col in range(2,0,-1):
                if row in [12,13]:
                    continue

                mm_cell = {}
                mm_cell['row'] = row
                mm_cell['column'] = col
                last_num = self.parking.pop(0)
                mm_cell['parking'] = last_num
                mm_cell['busy'] = 0
                mm_cell['rent'] = 0
                self.park_data.append(mm_cell)
                    
        for col in range(1,23,1):
            for row in range(0,26,1):
                mm_cell = {}
                #first blanks
                if row in [0]:
                    if col in [2,9,18]:
                        mm_cell['parking'] = '||||__||||'
                    else:
                        mm_cell['parking'] = '||||||||||'
                    mm_cell['column'] = col
                    mm_cell['row'] = row
                    self.park_data.insert(0, mm_cell)
                elif (col in [1,2]) and (row in [1,2,3,4,5,6]):
                    if row in [1,2]:
                        mm_cell['parking'] = '.'
                    elif row in [3,4]:
                        mm_cell['parking'] = '<=' 
                    else:
                        mm_cell['parking'] = '=>' 
                    mm_cell['column'] = col
                    mm_cell['row'] = row
                    self.park_data.append(mm_cell)
                elif ((col in self.blank_columns) and row != 25):
                    mm_cell['parking'] = '.'
                    mm_cell['column'] = col
                    mm_cell['row'] = row
                    self.park_data.append(mm_cell)
                elif row in [12,13]:
                    mm_cell['parking'] = ' . '
                    mm_cell['column'] = col
                    mm_cell['row'] = row
                    self.park_data.append(mm_cell)
                elif row in [25]:
                    if col in [2,9,18]:
                        mm_cell['parking'] = '||||__||||'
                    else:
                        mm_cell['parking'] = '||||||||||'
                    mm_cell['column'] = col
                    mm_cell['row'] = row
                    self.park_data.append(mm_cell)

    @staticmethod
    def is_mm_number(row_string):
        row_string = str(row_string).strip()
        mm_pattern = re.compile(r'^<td.*background-color.*white.*>\d+<\/td>')  
        return mm_pattern.match(row_string)

    @staticmethod
    def __get_mm_number(row_string):
        mm_pattern = re.compile(r'<td.*background-color.*white.*>(\d+)<\/td>')  
        found_num = mm_pattern.search(row_string).group(1)
        return int(found_num)

    @staticmethod
    def highlight_mm_number(html_string):

        found_num = ''
        try:
            mm_pattern = re.compile(r'<td.*background-color.*white.*>(\d+)<\/td>')  
            found_num = mm_pattern.search(html_string).group(1)
            html_string = re.sub("white\">" + found_num + "</td>", "cyan\">" + found_num + "</td>", html_string)
        except AttributeError:
            found_num = '' 

        return html_string

    def draw_map(self, dataset):
        self._build_map()

        logging.info("MAP WAS BUILDED")
        
        df = pd.DataFrame(data=self.park_data)
        df.pivot(index='row',columns='column', values='parking') \
            .rename_axis(None, axis=1) \
                .to_html('tmp_' + self.HTML_FILE, header=False, index=False) 

        with open(self.HTML_FILE ,'w') as new_file:
            with open('tmp_' + self.HTML_FILE) as old_file:
                for line in old_file:
                    line = line.replace('border="1"','border="0"')
                    line = line.replace('<td>','<td style="width:30;background-color: white">')  
                    if ParkMap.is_mm_number(line):
                        if ParkMap.__get_mm_number(line) in dataset:
                            line = ParkMap.highlight_mm_number(line)
                    new_file.write(line)
                    
        #Remove original file
        remove('tmp_' + self.HTML_FILE)

        logging.info("map file was created")

        return HOME_URL + "index.php"

