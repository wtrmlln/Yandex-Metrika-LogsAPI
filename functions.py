from secrets import token_urlsafe
from data import sites_dict, visits_columns_dict, hits_columns_dict

import pandas as pd
from functools import partial
from datetime import datetime
from tapi_yandex_metrika import YandexMetrikaLogsapi
from tapi_yandex_metrika import YandexMetrikaManagement

from user_input_functions import token, target, date1, date2

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

def get_ym_data(site_id):
    client = YandexMetrikaLogsapi(access_token=token, default_url_params={'counterId': site_id}, wait_report=True)
    
    visits_fields_ym = ",".join(list(visits_columns_dict.keys()))
    hits_fields_ym = ",".join(list(hits_columns_dict.keys()))

    #Создаем запрос
    if target == 'визиты':
        params={"date1":date1,
                "date2":date2,
                "fields": visits_fields_ym,
                "source":"visits"}
    elif target == 'просмотры':
        params={"date1":date1,
                "date2":date2,
                "fields": hits_fields_ym,
                "source":"hits"}
    result = client.create().post(params=params)
    request_id = result["log_request"]["request_id"]
    part = client.download(requestId=request_id, partNumber=0).get()
    data = part.data
    data = [x.split('\t') for x in data.split('\n')[:-1]]
    df_ym = pd.DataFrame(data[1:], columns=data[0])
    df_ym = df_ym.rename(columns=lambda x: x.strip())
    
    if target == 'визиты':
        df_ym = df_ym.rename(columns = visits_columns_dict)
    elif target == 'просмотры':
        df_ym = df_ym.rename(columns = hits_columns_dict)
#Преобразовывает числовые идентификаторы в текст и скачивает таблицу в формате xlsx    
    goals_dict = get_goals_dict(site_id)
    df_ym['Цели'] = df_ym['Цели'].apply(partial(get_id_names, goals_dict=goals_dict))
    filename = str('YaMetrika ' + target + ' ' + sites_dict[site_id] + ' ' + datetime.now().strftime('%Y-%m-%d') + '.csv')
    print(filename + ' успешно обработан в DataFrame')
    return [df_ym, filename]

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

def get_status_all_reports(site_id):
    client = YandexMetrikaLogsapi(token=token, default_url_params={'counterId': site_id}) 
    print(client.allinfo().get())

# Очистить все подготовленные репорты.
def clearout_all_reports(site_id):
    client = YandexMetrikaLogsapi(access_token=token_urlsafe, default_url_params={'counterId': site_id})
    result = client.allinfo().get()
    for report in result['requests']:
        if report['status'] == 'processed':
            request_id = report['request_id']
            new_result = client.clean(requestId=request_id).post()
            print('Запрос по сайту ' + sites_dict[str(report['counter_id'])] + ' с интервалом ' + report['date1'] + ' - ' + report['date2'] + ' успешно очищен' )
    

