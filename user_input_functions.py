from data import sites_dict
from datetime import datetime
import tkinter as tk

# Получить список необходимых сайтов для выгрузки с пользовательского ввода
def get_sites(sites, output_window, userform):
    while True:
        try:
            results_list = []
            sites_list = sites.split(',')
            if len(sites_list) > 0:
                for input_site_name in sites_list:
                    for site_name, site_id in sites_dict.items():
                        if input_site_name.strip() == site_name:
                            results_list.append(site_id)
                return results_list
            else:
                output_window.insert(tk.END, 'Ввод не может быть пустым значением' + '\n')
                userform.mainloop()
        except:
            userform.mainloop()

# Получить даты интервала для выгрузки с пользовательского ввода
def get_dates(date1, date2, output_window, userform):
    while True:
        try:            
            if (datetime.strptime(date2, "%Y-%m-%d") - datetime.strptime(date1, "%Y-%m-%d")).days <= 0:
                output_window.insert(tk.END, 'В интервал должен входить хотя бы один день.' + '\n')
            elif (datetime.strptime(date2, "%Y-%m-%d") - datetime.strptime(date1, "%Y-%m-%d")).days >= 365:
                output_window.insert(tk.END, 'Ширина интервала не должна превышать год.' + '\n')
            elif date1 == datetime.now().strftime("%Y-%m-%d") or date2 == datetime.now().strftime("%Y-%m-%d"):
                output_window.insert(tk.END, 'Дата не должна быть равна сегодняшней.' + '\n')
            else:
                output_window.insert(tk.END, 'Интервал успешно выбран.' + '\n')
                return [date1, date2]
        except:
            output_window.insert(tk.END, 'Некорректный формат даты, должен быть YYYY-MM-DD.' + '\n')
            userform.mainloop()
    
# Получить цель выгрузки (Просмотры/Визиты) с пользовательского ввода
def get_target(target, output_window, userform):
    while True:
        try:
            target = target.lower().strip()
            if target == 'просмотры' or target == 'визиты':
                return target
            else:
                output_window.insert(tk.END, 'Некорректно введена цель, должна быть "Просмотры" или "Визиты"' + '\n')
                userform.mainloop()
        except:
            userform.mainloop()