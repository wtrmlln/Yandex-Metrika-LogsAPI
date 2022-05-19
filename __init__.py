from token import token
from data import sites_dict
from functions import get_ym_data
from user_input_functions import get_target, get_dates, get_sites, get_token

def main():
    global token, required_sites, date1, date2, target
    AUTO_MODE = False

    # Выгружает только необходимые сайты
    if AUTO_MODE == False:
        token = get_token()
        required_sites = get_sites()
    # Выгружает все сайты из sites_dict
    elif AUTO_MODE == True: 
        token = token.token
        required_sites = list(sites_dict.keys())

    date1, date2 = get_dates()
    target = get_target()

    sites_list = []
    results_list = []
    for key, value in sites_dict.items():
        if value in required_sites:
            sites_list.append(key)
    from multiprocessing.dummy import Pool as ThreadPool
    pool = ThreadPool(len(sites_list) if len(sites_list) < 3 else 3)
    results_list.append(pool.map(get_ym_data, sites_list))

    for site in results_list:
        for df, filename in site:
            df.to_csv(filename)
    
if __name__ == '__main__': 
    main()