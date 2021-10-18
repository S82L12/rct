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


------
Allembic
https://youtu.be/KFj3VhMTAdk
1. Инициируем
!!! flask db init
2. Настриваем файлы (путь и файл с моделями)   КОПИРУЮ ПУТЬ из своего файла config_ins.py
!!! 3.1. по видео на ютубе                      alembic revision --message="Initial" --autogenerate
3.2. По документации                        flask db migrate -m "Initial migration."  не работает
Проверяем созданную миграцию (В частности, Alembic в настоящее время не может обнаруживать изменения имени таблицы, изменения имени столбца или ограничения с анонимными именами)
4.1 !!! alembic upgrade head  youtube
4.2. flask db upgrade  документациия не работает
ПРименяем миграцию
