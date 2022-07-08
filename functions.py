import os
from data import sites_dict, visits_columns_dict, hits_columns_dict
import pandas as pd
import tkinter as tk
from functools import partial
from datetime import datetime
from tapi_yandex_metrika import YandexMetrikaLogsapi, YandexMetrikaManagement
from metrika_token import token
from multiprocessing.dummy import Pool as ThreadPool

def get_goals_dict(site_id):
    
    client = YandexMetrikaManagement(access_token=token, default_url_params={'counterId': site_id})
    goals_json = client.goals().get()
    goals_dict = {}

    for goal in goals_json.data['goals']:
        # Если цель составная
        if 'steps' in goal.keys():
            for sub_goal in goal['steps']:
                goals_dict[sub_goal['id']] = sub_goal['name']
        goals_dict[goal['id']] = goal['name']
    
    return goals_dict

# Переводит числовые идентификаторы (219152671) целей в текстовые (Клик по кнопке "Прямой эфир")
def get_id_names(text, goals_dict):
    new_text = ''
    text = text.replace('[', '')
    text = text.replace(']', '')
    id_array = text.split(sep = ',')
    if '' == id_array[0]:
        return None
    for id in id_array:
        temptext = goals_dict[int(id)]
        if new_text == '':
            new_text = temptext
        else:
            new_text = new_text + ',' + temptext
    return new_text

# Получить статус репорта
def get_report_status(site_name, output_window):
    client = YandexMetrikaLogsapi(access_token=token, default_url_params={'counterId': sites_dict[site_name]})
    try:
        result = client.allinfo().get()
        output_window.insert(tk.END, str(result) + '\n')
    except KeyError as e:
        output_window.insert(tk.END, 'Не обнаружено?' + '\n')

# Отметить подготовку репорта
def cancel_report_preparing(site_name, output_window):
    client = YandexMetrikaLogsapi(access_token=token, default_url_params={'counterId': sites_dict[site_name]})
    result = client.allinfo().get()
    if len(result['requests']) > 0:
        for report in result['requests']:
            if report['status'] == 'created':
                client.cancel(requestId=report['request_id']).post()
                for site_name, site_id in sites_dict.items():
                    if str(report['counter_id']) == site_id:
                        output_window.insert(tk.END, 'Запрос ' + str(report['request_id']) + ' по сайту '  + site_name + ' с интервалом ' + report['date1'] + ' - ' + report['date2'] + ' успешно отменен' + '\n')
    else:
        output_window.insert(tk.END, 'Запрошенный репорт не обнаружен' + '\n')        
# Удалить подготовленный репорт
def clearout_prepared_report(site_name, output_window):
    client = YandexMetrikaLogsapi(access_token=token, default_url_params={'counterId': sites_dict[site_name]})
    result = client.allinfo().get()
    if len(result['requests']) > 0:
        for report in result['requests']:
            if report['status'] == 'processed':
                client.clean(requestId=report['request_id']).post()
                for site_name, site_id in sites_dict.items():
                    if str(report['counter_id']) == site_id:
                        output_window.insert(tk.END, 'Запрос ' + str(report['request_id']) +  ' по сайту ' + site_name + ' с интервалом ' + report['date1'] + ' - ' + report['date2'] + ' успешно очищен' + '\n')
    else:
        output_window.insert(tk.END, 'Запрошенный подготовленный репорт не обнаружен' + '\n') 

def downloading(sites_list, target, dates_list):
    
    global params
    
    date1 = dates_list[0]
    date2 = dates_list[1]
    
    visits_fields_ym = ",".join(list(visits_columns_dict.keys()))
    hits_fields_ym = ",".join(list(hits_columns_dict.keys()))
    
    if target == 'визиты':
        params={"date1":date1,
                "date2":date2,
                "fields": visits_fields_ym,
                "source":"visits"
                }
    elif target == 'просмотры':
        params={"date1":date1,
                "date2":date2,
                "fields": hits_fields_ym,
                "source":"hits"
                }
    
    results_list = []
    pool = ThreadPool(len(sites_list) if len(sites_list) < 3 else 3)
    results_list.append(pool.map(get_ym_data, sites_list))

    path_to_upload = 'C:\\Users\\' + os.getlogin() + '\\Desktop\\Яндекс.Метрика выгрузки\\'
    
    try:
        os.makedirs(path_to_upload)
    except FileExistsError:
        pass
    
    for site in results_list:
        for df, filename in site:
            df.to_csv(path_to_upload + filename)  
    
def get_ym_data(site_id):
    client = YandexMetrikaLogsapi(access_token=token, default_url_params={'counterId': site_id}, wait_report=True)
    
    #Создаем запрос

    result = client.create().post(params=params)
    request_id = result["log_request"]["request_id"]
    part = client.download(requestId=request_id, partNumber=0).get()
    data = part.data
    data = [x.split('\t') for x in data.split('\n')[:-1]]
    df_ym = pd.DataFrame(data[1:], columns=data[0])
    df_ym = df_ym.rename(columns=lambda x: x.strip())
    
    if result['log_request']['source'] == 'visits':
        df_ym = df_ym.rename(columns = visits_columns_dict)
    elif result['log_request']['source'] == 'hits':
        df_ym = df_ym.rename(columns = hits_columns_dict)
#Преобразовывает числовые идентификаторы в текст и скачивает таблицу в формате xlsx    
    goals_dict = get_goals_dict(site_id)
    df_ym['Цели'] = df_ym['Цели'].apply(partial(get_id_names, goals_dict=goals_dict))
    for iter_site_name, iter_site_id in sites_dict.items():
        if site_id == iter_site_id:
            filename = str('YaMetrika ' + result['log_request']['source'] + ' ' + iter_site_name + ' ' + datetime.now().strftime('%Y-%m-%d') + '.csv')
            return [df_ym, filename]  