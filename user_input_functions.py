import metrika_token
from data import sites_dict
from datetime import datetime

def get_automode():
    return str(input('Выгрузить все доступные сайты? (Да/Нет): '))

# Получить список необходимых сайтов для выгрузки с пользовательского ввода
def get_sites():
    print('Список доступных сайтов для выгрузки (наименование /// id сайта): ')
    for site_id, site_name in sites_dict.items():
        print(site_name.ljust(25) + ' /// ' + site_id)  
    print()
    while True:
        try:
            results_list = []
            sites_list = input('Введите через запятую наименования необходимых сайтов для выгрузки: ').strip().split(',')
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
            
            if (datetime.strptime(date2, "%Y-%m-%d") - datetime.strptime(date1, "%Y-%m-%d")).days <= 0:
                print('В интервал должен входить хотя бы один день.')
            elif (datetime.strptime(date2, "%Y-%m-%d") - datetime.strptime(date1, "%Y-%m-%d")).days >= 365:
                print('Ширина интервала не должна превышать год.')
            elif date1 == datetime.now().strftime("%Y-%m-%d") or date2 == datetime.now().strftime("%Y-%m-%d"):
                print('Дата не должна быть равна сегодняшней.')
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

AUTO_MODE = str.lower(get_automode()).replace(' ', '')
if AUTO_MODE == 'нет':
    required_sites = get_sites()
# Выгружает все сайты из sites_dict
elif AUTO_MODE == 'да': 
    required_sites = list(sites_dict.keys())

token = metrika_token.token
date1, date2 = get_dates()
target = get_target()

sites_list = []
for key in sites_dict.keys():
    if key in required_sites:
        sites_list.append(key)