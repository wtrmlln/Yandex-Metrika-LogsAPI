import os
from functions import get_ym_data
from user_input_functions import sites_list
from multiprocessing.dummy import Pool as ThreadPool

if __name__ == '__main__': 
    
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