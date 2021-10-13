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
Устанавливаем pip install flask-migrate
-------
Требуется:
1. Прописать фильтры для вендоров (VP е определяются)
-------
1. Модели должны добавлены вручную перед тем как будем загружать список devices из файла. Так как модели будут сравниваться со списком моделей
2. Модели вносяться без вендора!
-------
** (дополнительные модули - не реализованные)
- Добавление файла "накладной"  для "устройств"
- При выгрузке файла из программы, ЕСЛИ ужесуществуют данные, предлагаю выгружать их. Иначе файл пусть будет исходный файл
- Проверка ID при загрузке из файла на соответствие формату

-------
ERROR:
1. При добавлении Device из файла, на странице "статус" , панели и накладная отображаются перепутанные