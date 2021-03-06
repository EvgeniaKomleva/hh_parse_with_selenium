import pandas as pd
import datetime
from configparser import ConfigParser
import sys
import numpy as np
import os


current_datetime = str(datetime.datetime.now())
time = str(datetime.datetime.now().time())
time_str = time[0:2] + time[3:5]
current_day = current_datetime[0:4] + current_datetime[5:7] + current_datetime[8:11] + time_str

data = pd.read_csv('data/data.csv')

#data["href"] = 'https://hh.ru' + data["href"]
count_company = data["last_work_place"].value_counts()
df_count_company = pd.DataFrame({'last_work_place': count_company.index, 'count': count_company.values})
df_count_company = df_count_company[
    df_count_company.last_work_place != 'Индивидуальное предпринимательство / частная практика / фриланс']
df_count_company = df_count_company[df_count_company.last_work_place != 'фриланс']
df_count_company = df_count_company[df_count_company.last_work_place != 'Фриланс']
df_count_company = df_count_company[df_count_company.last_work_place != "Freelance"]
df_count_company = df_count_company[df_count_company.last_work_place != "-"]

df_count_company.to_csv('resume/{}_{}_count_company.csv'.format('config', current_day), sep=';', index=False,
                        encoding='utf-8-sig')

data_with_count = data.set_index('last_work_place').join(df_count_company.set_index('last_work_place'))
sorted_data = data_with_count.sort_values(by=["count"], ascending=False)
sorted_data.drop(["Индивидуальное предпринимательство / частная практика / фриланс"], inplace=True, errors='ignore')
sorted_data.drop(["Фриланс"], inplace=True, errors='ignore')
sorted_data.drop(["Freelance"], inplace=True, errors='ignore')
sorted_data.drop(["фриланс"], inplace=True, errors='ignore')
#sorted_data = sorted_data[((sorted_data.citizenship == 'Россия') | (sorted_data.citizenship == 'Белaрусь'))]

sorted_data.reset_index(inplace=True)
sorted_data = sorted_data.fillna(0)
sorted_data["count"] = sorted_data["count"].astype(int)
#sorted_data = sorted_data[sorted_data.match_count != 0]

#sorted_data = sorted_data[sorted_data['all_jobs'].str.contains(config['parametrs']['intersted_company'])]

#sorted_data.drop_duplicates(subset ="href", keep = False, inplace = True)

#sorted_data["href"] = sorted_data["href"].astype(str).str[0:59].astype(np.str)
#sorted_data["href"] = sorted_data["href"].astype(str).str[0:59].astype(np.str)
sorted_data["href"].replace(r".query=.*", '', regex=True, inplace = True)
sorted_data.to_csv('resume/{}_{}_data_sort.csv'.format('config', current_day), sep=';', index=False,
                   encoding='utf-8-sig')
# os.remove("data/data.json")
# print(auth)
