#!/usr/bin/env python
# coding: utf-8

import requests
import json
import pandas as pd
import os
import warnings
import datetime
import time
warnings.filterwarnings('ignore')

input_start = input('Input start YYYY-MM-DD ')
input_end = input('Input end YYYY-MM-DD ')
input_folder = input('Input folder ')

START_DATE = datetime.datetime.strptime(input_start, '%Y-%m-%d').date()
END_DATE = datetime.datetime.strptime(input_end, '%Y-%m-%d').date()
folder = input_folder

url = 'https://www.okx.com/api/v5/support/announcements'

response = requests.get(url)
data = response.json()
total_pages = int(data['data'][0].get('totalPage'))

results = []
break_out_flag = False
for i in range(0, total_pages):
    time.sleep(0.5)
    params = {'page':i+1}
    response = requests.get(url, params=params)
    data = response.json()
    announcements = data['data'][0].get('details')
    for announcement in announcements:
        date = int(announcement.get('pTime')[:10])
        date = datetime.datetime.fromtimestamp(date).date()
        if (START_DATE <= date <= END_DATE):
            results.append([announcement.get('annType'), date, announcement.get('title'), announcement.get('url')])
        elif ((START_DATE > date) or (date > END_DATE)) and (len(results) > 0):
            break_out_flag = True
            break
    if break_out_flag:
        break

df = pd.DataFrame(results, columns=['type','date','title','url'])
filename = f'{START_DATE}-{END_DATE}.csv'
path = os.path.join(folder, filename)
try: 
    df.to_csv(path, index=False)
    print('Data saved successfully. Have a nice day.')
except:
    print('Something went wrong. Try again later.')

