# Аналог сайта Авито на Flask

Сайт выложен на хостинг по адресу https://hodakoov.ru/
## Описание

Проект представляет собой сайт, который является аналогом популярного ресурса Авито. 
Написан на языке Python с использованием фреймворка Flask, а также библиотек Flask Login для аутентификации и авторизации пользователей, 
Flask WTF Form для работы с формами, SQLAlchemy для работы с базой данных и Jinja2 для создания шаблонов страниц.

Сайт позволяет пользователям просматривать, размещать и удалять собственные объявления. 
Для этого пользователи должны будут пройти этап регистрации, чтобы управлять своими объявлениями.

Одной из ключевых задач в проекте был скрапинг раздела с объявлениями о продаже Iphone в г.Москва на сайте Авито. 
Для этой задачи был разработан скрипт скрапинга, использующий библиотеку Selenium.

## Установка и запуск

1. Склонировать репозиторий на свой компьютер

```bash
git clone git@github.com:hodakoov/advertising_site.git
```
или
```bash
git clone https://github.com/hodakoov/advertising_site.git
```

2. Перейти в папку с проектом 
```bash
cd advertising_site
```

3. Создать и активировать виртуальное окружение (для Linux/Mac)
```bash
python3 -m venv venv
source venv/bin/activate
```

4.Установить необходимые зависимости

```bash
   pip install -r requirements.txt
```

5. Запустить проект (для Linux/Mac)
```bash
export FLASK_APP=app && export FLASK_ENV=development && flask run
```

6. Откройте веб-браузер и перейдите по адресу http://127.0.0.1:5000/ или http://localhost:5000.

## Добавление Администратора
Добавление пользователя возможно не только на сайте через форму регистрации, 
но и через скрипт create_user.py. При этом администратора можно создать только с помощью данного скрипта.
1. Потребуется узнать путь до вашей папки. На Linux/Mac путь можно узнать командой `pwd`.
2. Находясь в виртуальном окружении прописать следующую команду
```bash
export PYTHONPATH={путь/из/pwd/безскобок} && python app/create_user.py
```

## Используемые технологии

- `Python 3.10`
- `Flask 2.3.3`
- `Flask Login 0.6.2`
- `Flask WTF Form 1.2.1`
- `Flask SQLAlchemy 2.5.1`
- `SQLAlchemy 1.4.49`
- `Jinja2 3.1.2`
- `Selenium 4.13.0`

### База данных
На данный момент используется `SQLite`, которая поставляется месте с Python.
В будущем планируется перейти на более производительную `PostgreSQL`.

## Планы по развитию

- Добавление фильтрации по группам объявлений
- Расширение возможностей для пользователей
- Улучшение интерфейса и добавление новых функциональных элементов

## Авторы

- [Ходаков Валерий](https://t.me/hodakoov)
- [Старых Семен](https://t.me/LuSP7)

## Благодарности

- Нашему ментору [Синякову Глебу](https://t.me/technogleb) 
- Команде [LearnPython](https://learn.python.ru/)