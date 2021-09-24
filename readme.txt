python -m pip install -U transliterate
https://docs-python.ru/packages/modul-transliterate-python/
модуль translate
>>> from transliterate import translit
>>> ru_text = 'Лорем ипсум долор сит амет'
>>> text = translit(ru_text, language_code='ru', reversed=True)
>>> text
# 'Lorem ipsum dolor sit amet'

>>> ru_text = 'Михаил, Юлия, София, Андрей'
>>> text = translit(ru_text, language_code='ru', reversed=True)
>>> text
# 'Mihail, Julija, Sofija, Andrej'

устанавливаем pip install flask-wtf
---
добавление адреса ОК
создание выпадающего списка OK
добавление vlan OK
Настройка выгрузки файла OK
type OK
backref OK
настройка загрузки файла и из файла vlan OK
настройка загрузки файла и из файла address OK
Добавление поля translate в адресс OK
Добавление функции translate в адресс OK
добавления WTFORM location OK
vlan+IPnet OK
