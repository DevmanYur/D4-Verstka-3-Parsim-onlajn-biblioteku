# Скрипт по скачиванию книг

## Описание работы скрипта
Данный скрипт позволяет скачивать книги с сайта [tululu.org](https://tululu.org)
в зависимости от заданных страниц


## Как установить
1. Python3 должен быть уже установлен. 
2. Используйте `pip` для установки зависимостей:

```
pip install -r requirements.txt
```

3. Запустите скрипт из терминала командой:

```
python parse_tululu.py start_id end_id
```
Где:

      start_id - номер страницы с которой начать скачивание
      end_id - номер страницы по которую закончить скачивание



4. Пример запуска скрипта из терминала командой:
``` python
python parse_tululu.py 2 11
```
Где:

      2 - номер страницы с которой начать скачивание
      11 - номер страницы по которую закончить скачивание