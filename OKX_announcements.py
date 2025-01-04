#!/usr/bin/env python
# coding: utf-8

# In[10]:


import requests
import json
import pendulum
import pandas as pd
import os
import warnings
import datetime
import time
import streamlit as st
warnings.filterwarnings('ignore')


# In[17]:


input_start = input('Input start YYYY-MM-DD ')
input_end = input('Input end YYYY-MM-DD ')
input_folder = input('Input folder ')

START_DATE = datetime.datetime.strptime(input_start, '%Y-%m-%d').date()
END_DATE = datetime.datetime.strptime(input_end, '%Y-%m-%d').date()
folder = input_folder
# r'C:\Users\mvsav\OneDrive\Рабочий стол\OKX_announcements'

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
        date = pendulum.from_timestamp(date).date()
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
df.to_csv(path, index=False)

