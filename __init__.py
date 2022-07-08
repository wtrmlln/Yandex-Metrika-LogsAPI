import tkinter as tk
from functions import cancel_report_preparing, clearout_prepared_report, get_report_status, downloading
from data import sites_dict
from user_input_functions import get_sites, get_target, get_dates

class SiteNumberWindow():
    def __init__(self):
        self.text = tk.Text(height=40, width=25, wrap= tk.NONE)
        self.text.grid(column=1, row=5)
        self.text.insert(tk.END, '\n'.join(sites_dict.keys()))
        
        self.label = tk.Label(text='Номера счетчиков сайтов', 
                                             width=30, 
                                             justify=tk.LEFT)
        self.label.grid(column=0, row=4)

class SiteNamesWindow():
    def __init__(self):
        self.text = tk.Text(height=40, width=25,wrap=tk.NONE)
        self.text.insert(tk.END, '\n'.join(sites_dict.values()))
        
        self.label = tk.Label(text='Названия сайтов', 
                                            width=30, 
                                            justify=tk.LEFT)
        
        self.text.grid(column=0, row=5)
        self.label.grid(column=1, row=4)

class OutputWindow():
    def __init__(self):
        self.label = tk.Label(text='Окно вывода', 
                              width=30, 
                              justify=tk.LEFT)
        self.text = tk.Text(height=40, width=30, wrap=tk.WORD)
        self.scrollbar = tk.Scrollbar(orient=tk.VERTICAL, command=self.text.yview, width=50)
        self.scrollbar.place(x=705, y=200, relheight=0.65)
        self.text['yscrollcommand'] = self.scrollbar.set
        
        self.label.grid(column=2, row=4)
        self.text.grid(column=2, row=5)
    
    def get_text(self):
        return self.text

class Button():
    def __init__(self, text, command, column_grid, row_grid):
        self.button = tk.Button(text=text, command=command)
        self.button.grid(column=column_grid, row=row_grid)
        
class Checkbox():
    def __init__(self, text, variable, command, onvalue, offvalue, column_grid, row_grid):
        self.checkbox = tk.Checkbutton(text=text, 
                                       variable=variable, 
                                       command=command, 
                                       onvalue=onvalue, 
                                       offvalue=offvalue)
        self.checkbox.grid(column=column_grid, row=row_grid)

class InputWindow():
    def __init__(self, text, label_column_grid, label_row_grid, window_column_grid, window_row_grid):
        self.label = tk.Label(text=text, 
                              width=30, 
                              justify=tk.LEFT, 
                              wraplength=200)
        self.label.grid(column=label_column_grid, row=label_row_grid)
        
        self.window = tk.Entry(width=30)
        self.window.grid(column=window_column_grid, row=window_row_grid)
        
    def get_value(self):
        return self.window.get()
        
class MainInterface(tk.Tk):
    
    def __init__(self, *args, **kwargs): 
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry("1000x600")   
        self.title('Yandex-Metrika-LogsAPI')
        self.sitenumberwindow = SiteNumberWindow()
        self.sitenameswindow = SiteNamesWindow()
        self.outputwindow = OutputWindow()
        
        AUTO_MODE = tk.StringVar()
        self.checkbox = Checkbox(text='Выгрузить все сайты?', 
                                 variable=AUTO_MODE, 
                                 command=lambda:checkbox_changed(AUTO_MODE), 
                                 onvalue='да', 
                                 offvalue='нет',
                                 column_grid=1, 
                                 row_grid=2)
        
        self.label_help = tk.Label(text='Если не копируется название/номер, переключите раскладку на клавиатуре', 
                                   wraplength=200, 
                                   justify=tk.LEFT)
        self.label_help.grid(column=0, row=2)
        
        self.site_inputwindow = InputWindow(text='Введите название сайта для получения статуса, либо введите название(я) сайта(ов) через запятую для выгрузки:',
                                      label_column_grid=2,
                                      label_row_grid=0,
                                      window_column_grid=2,
                                      window_row_grid=1)
        
        self.date1_inputwindow = InputWindow(text='Введите первую дату интервала формата YYYY-MM-DD для выгрузки:',
                                      label_column_grid=3,
                                      label_row_grid=0,
                                      window_column_grid=3,
                                      window_row_grid=1)
        
        self.date2_inputwindow = InputWindow(text='Введите вторую дату интервала формата YYYY-MM-DD для выгрузки:',
                                      label_column_grid=3,
                                      label_row_grid=2,
                                      window_column_grid=3,
                                      window_row_grid=3)
        
        self.target_inputwindow = InputWindow(text='Введите цель выгрузки (Просмотры/Визиты):',
                                      label_column_grid=2,
                                      label_row_grid=2,
                                      window_column_grid=2,
                                      window_row_grid=3)
        
        self.cancel_report_button = Button(text='Очистить неподготовленный репорт', 
                                           command=lambda:cancel_report_preparing(self.site_inputwindow.get_value(), self.outputwindow.get_text()), 
                                           column_grid=0,
                                           row_grid=0)
        
        self.clearout_prepared_report_button = Button(text='Очистить подготовленный репорт', 
                                                      command=lambda:clearout_prepared_report(self.site_inputwindow.get_value(), self.outputwindow.get_text()),
                                                      column_grid=0,
                                                      row_grid=1)
        
        self.get_status_button = Button(text='Получить статусы выполнения', 
                                        command=lambda:get_report_status(self.site_inputwindow.get_value(), self.outputwindow.get_text()), 
                                        column_grid=1,
                                        row_grid=0)
        
        self.download_button = Button(text='Выгрузить', 
                                      command=lambda:downloading(list(sites_dict.keys()) if AUTO_MODE.get() == 'да' else get_sites(self.site_inputwindow.get_value(), self.outputwindow.get_text(), self),
                                                                 get_target(self.target_inputwindow.get_value(), self.outputwindow.get_text(), self), 
                                                                 get_dates(self.date1_inputwindow.get_value(), self.date2_inputwindow.get_value(), self.outputwindow.get_text(), self)),
                                      column_grid=1,
                                      row_grid=1)
        self.mainloop() 
        
def checkbox_changed(toggle):
    return toggle.get()
    
def main():
    app = MainInterface()
    
if __name__ == '__main__':
    main()
