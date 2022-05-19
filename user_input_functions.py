import metrika_token
from data import sites_dict
from datetime import datetime

AUTO_MODE = True

# Получить токен с пользовательского ввода
def get_token():
    return str(input('Введите токен аутентификации для Яндекс.Метрика: '))

# Получить список необходимых сайтов для выгрузки с пользовательского ввода
def get_sites():
    print('Список доступных сайтов для выгрузки (наименование /// id сайта):')
    for site_id, site_name in sites_dict.items():
        print(site_name + ' /// ' + site_id)  
    print()
    while True:
        try:
            results_list = []
            sites_list = input('Введите через запятую наименования необходимых сайтов для выгрузки').strip().split(',')
            if len(sites_list) > 0:
                for input_site_name in sites_list:
                    for site_id, site_name in sites_dict.items():
                        if input_site_name.strip() == site_name:
                            results_list.append(site_id)
                return results_list
            else:
                print('Ввод не может быть пустым значением')
        except:
            pass

# Получить даты интервала для выгрузки с пользовательского ввода
def get_dates():
    while True:
        try:            
            date1 = str(input('Введите первую дату для интервала выгрузки формата YYYY-MM-DD: ')).lower().strip()
            date2 = str(input('Введите вторую дату для интервала выгрузки формата YYYY-MM-DD: ')).lower().strip()
            
            datetime.strptime(date1, '%Y-%m-%d')
            datetime.strptime(date2, '%Y-%m-%d')
            if (datetime.strptime(date2, "%Y-%m-%d") - datetime.strptime(date1, "%Y-%m-%d")).days <= 0:
                print('В интервал должен входить хотя бы один день.')
            elif (datetime.strptime(date2, "%Y-%m-%d") - datetime.strptime(date1, "%Y-%m-%d")).days >= 365:
                print('Ширина интервала не должна превышать год.')
            else:
                print('Интервал успешно выбран.')
                return [date1, date2]
        except:
            print("Некорректный формат даты, должен быть YYYY-MM-DD.")

# Получить цель выгрузки (Просмотры/Визиты) с пользовательского ввода
def get_target():
    while True:
        try:
            target = str(input('Введите цель выгрузки (Просмотры/Визиты): ')).lower().strip()
            if target == 'просмотры' or target == 'визиты':
                return target
            else:
                print('Некорректно введена цель, должна быть "Просмотры" или "Визиты"')
        except:
            pass

# Выгружает только необходимые сайты
if AUTO_MODE == False:
    token = get_token()
    required_sites = get_sites()
# Выгружает все сайты из sites_dict
elif AUTO_MODE == True: 
    token = metrika_token.token
    required_sites = list(sites_dict.keys())

date1, date2 = get_dates()
target = get_target()

sites_list = []
for key in sites_dict.keys():
    if key in required_sites:
        sites_list.append(key)