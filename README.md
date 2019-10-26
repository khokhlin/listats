# listats
Скрипт для считывания данных со счетчиков посещаемости сервиса LiveInternet

## Установка

```sh
$ python setup.py install
```

## Использование

Создайте файл со списком доменов:

```text
avito.ru
gazeta.ru
```

По умолчанию используется файл `domains.txt` в текущей директории.

```sh
$ python -m listats --domains=~/listats_domains.txt
```

Пример вывода:  
```
avito.ru
            visitors     pageviews
     month: 38868365     2032294331  
      week: 10039        475006      
  24-hours: 1773         58472       
     today: 36           421         
    online: 33           705         
----------------------------------------
gazeta.ru
            visitors     pageviews
     month: 13741019     67963555    
      week: 4171184      15136760    
  24-hours: 582065       1657493     
     today: 11849        19091       
    online: 10396        34289       
----------------------------------------
```

###  Использование в своих скриптах

```python
from listats import get_stats
data = get_stats(("avito.ru", "gazeta.ru"))
print(data)
```
Будет выведен словарь:

```sh
{'avito.ru': {'visitors': {'today': '72', 'online': '12', 'month': '38868365', '24-hours': '1780', 'week': '10039'}, 'pageviews': {'today': '1505', 'online': '590', 'month': '2032294331', '24-hours': '58590', 'week': '475006'}}, 'gazeta.ru': {'visitors': {'today': '39872', 'online': '10448', 'month': '13469833', '24-hours': '588709', 'week': '4127541'}, 'pageviews': {'today': '75942', 'online': '29711', 'month': '66975984', '24-hours': '1664686', 'week': '15112392'}}}
```
