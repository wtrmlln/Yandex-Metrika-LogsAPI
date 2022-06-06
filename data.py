# Визиты - https://yandex.ru/dev/metrika/doc/api2/logs/fields/visits.html
visits_columns_dict = {'ym:s:clientID': 'ID посетителя',
                       'ym:s:visitID': 'Идентификатор визита', 
                       'ym:s:startURL': 'Страница входа',
                       'ym:s:endURL': 'Страница выхода',
                       'ym:s:pageViews': 'Глубина просмотра (детально)',
                       'ym:s:goalsID': 'Идентификаторы достигнутых целей',
                       'ym:s:visitDuration': 'Время на сайте (детально)',
                       'ym:s:lastTrafficSource': 'Источник трафика',
                       'ym:s:regionCountry': 'Страна (ISO)',
                       'ym:s:regionCity': 'Город (английское название)',
                       'ym:s:bounce': 'Отказность',
                       'ym:s:isNewUser': 'Первый визит посетителя',
                       'ym:s:operatingSystemRoot': 'Группа операционных систем',
                       'ym:s:lastSearchEngineRoot':'Поисковая система',
                       'ym:s:lastSearchEngine': 'Поисковая система (детально)',
                       'ym:s:lastSearchPhrase': 'Последняя значимая поисковая фраза',
                       'ym:s:browser': 'Браузер',
                       'ym:s:isNewUser': 'Первый визит посетителя'}

# Просмотры - https://yandex.ru/dev/metrika/doc/api2/logs/fields/hits.html
hits_columns_dict = {'ym:pv:clientID': 'Идентификатор пользователя на сайте',
                     'ym:pv:watchID': 'Идентификатор просмотра',
                     'ym:pv:date': 'Дата события', 
                     'ym:pv:title': 'Заголовок страницы',
                     'ym:pv:URL': 'Адрес страницы',
                     'ym:pv:deviceCategory': 'Тип устройства',
                     'ym:pv:regionCity': 'Город (английское название)',
                     'ym:pv:regionCountry': 'Страна (ISO)',
                     'ym:pv:isPageView': 'Просмотр страницы. Принимает значение 0, если хит не нужно учитывать как просмотр',
                     'ym:pv:link': 'Переход по ссылке',
                     'ym:pv:download': 'Загрузка файла',
                     'ym:pv:notBounce': 'Специальное событие «неотказ» (для точного показателя отказов)',
                     'ym:pv:httpError': 'Код ошибки',
                     'ym:pv:UTMContent': 'UTM Content',
                     'ym:pv:goalsID': 'Идентификаторы достигнутых целей'}

sites_dict = {'56483272': 'Торуда',
              '50151718': 'Шведские стенки'}