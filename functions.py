from data import sites_dict, sites_goals_dict, visits_columns_dict, hits_columns_dict

import pandas as pd
from functools import partial
from datetime import datetime
from tapi_yandex_metrika import YandexMetrikaLogsapi

from user_input_functions import token, target, date1, date2

def get_ym_data(site_id):
    print(token)
    client = YandexMetrikaLogsapi(token=token, default_url_params={'counterId': site_id})
    
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

    # Если запрос подготовлен - скачать и обработать в датафрейм
    # В ином случае - ячейка выполняется до тех пор пока не будет подготовлен запрос
    while True:
        info = client.info(requestId=request_id).get()
        if info['log_request']['status'] == 'processed':
            filename = str('YaMetrika ' + target + ' ' + sites_dict[site_id] + ' ' + datetime.datetime.now().strftime('%Y-%m-%d') + '.csv')
            print(filename + ' подготовлен к скачиванию')
            part = client.download(requestId=request_id, partNumber=0).get()
            data = part.data
            data = [x.split('\t') for x in data.split('\n')[:-1]]
            df_ym = pd.DataFrame(data[1:], columns=data[0])
            df_ym = df_ym.rename(columns=lambda x: x.strip())
            
            if target == 'visits':
                df_ym = df_ym.rename(columns = visits_columns_dict)
            elif target == 'hits':
                df_ym = df_ym.rename(columns = hits_columns_dict)
            break
        else:
            pass
    #Преобразовывает числовые идентификаторы в текст и скачивает таблицу в формате xlsx    
    
    df_ym['Идентификаторы достигнутых целей'] = df_ym['Идентификаторы достигнутых целей'].apply(partial(get_id_names, site_id=site_id))
    print(filename + ' успешно обработан в DataFrame')
    return [df_ym, filename]

# Переводит числовые идентификаторы (219152671) целей в текстовые (Клик по кнопке "Прямой эфир")
def get_id_names(text, site_id):
    new_text = ''
    text = text.replace('[', '')
    text = text.replace(']', '')
    id_array = text.split(sep = ',')
    if '' == id_array[0]:
        return None
    for id in id_array:
        temptext = sites_goals_dict[site_id][id]
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
    client = YandexMetrikaLogsapi(token=token, default_url_params={'counterId': site_id})
    result = client.allinfo().get()
    for report in result['requests']:
        if report['status'] == 'processed':
            request_id = report['request_id']
            new_result = client.clean(requestId=request_id).post()
    print(result)
    

