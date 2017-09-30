# listats
Скрипт для считывания данных со счетчиков посещаемости сервиса LiveInternet


## Установка

```sh
$ python setup.py install
```


## Использование

```sh
$ python -m listats
```

Пример вывода:  
```
{'avito.ru': {'pageviews': {'24-hours': '962920',
                            'month': '14334857',
                            'online': '16002',
                            'today': '905309',
                            'week': '4356382'},
              'visitors': {'24-hours': '2480373',
                           'month': '69369026',
                           'online': '42540',
                           'today': '2264344',
                           'week': '15524892'}},
 'gazeta.ru': {'pageviews': {'24-hours': '962920',
                             'month': '14334857',
                             'online': '16002',
                             'today': '905309',
                             'week': '4356382'},
               'visitors': {'24-hours': '2480373',
                            'month': '69369026',
                            'online': '42540',
                            'today': '2264344',
                            'week': '15524892'}}}
```
