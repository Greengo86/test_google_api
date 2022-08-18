# Сервис Google-Api

Сервис разработан на django rest framework И React-JS

Использую свои креды к сервису Гугла и запушил их в проект. Так, конечно, же делать нельзя, но не могу заставить ревьювера добавлять свои

Ссылка на гугл документ. Будет расшарена для правок, как и указано в ТЗ

````
https://docs.google.com/spreadsheets/d/1lpPGtsooRUJMBk_LIOKVbcGdPzeDdMiAaexn9KhYdME/edit#gid=0
````

Cуществует 2 варианты решения:
````
[master-ветка](https://github.com/Greengo86/test_google_api/tree/master)
- работает быстрее. Все Записи вначале удаляются, и затем массово записываются.
````

````
[Second_Implementation_update_records](https://github.com/Greengo86/test_google_api/tree/Second_Implementation_update_records)
- здесь мы сравниваем объекты из базы данных и из Google Sheets. Если в Sheets нет какого-либо обьекта, то вычислим его и удалим из базы. Остальные массово обновим, если они уже были в базе, если нет - запишем. Таким образом избегаем создание новых объектов базе, а только лишь обновляем
````

## Установка и запуск

1. Склонировать репозиторий с Github:

````
git clone https://github.com/Greengo86/test_google_api.git
````
2. Перейти в директорию проекта

3. Создать виртуальное окружение на python 3.9:

````
python -m venv venv
````

4. Активировать окружение: 

````
source\venv\bin\activate
````

5. В корневой директории создать файл .evn и заполнить необходимые переменные. TG_TOKEN токен чат бота Телеграмма и TG_ID - id пользователя телеграмма (нужно для уведомления о просрочке):
```
TG_TOKEN = '{}'
TG_ID = '{}'
```
 
6. Установка зависимостей:

```
pip install -r requirements.txt
```
7. В setting.py cловарь DATABASES установить настройки подключения к бд POSTGRES. Если таковой нет перейти к пункту -  Установка проекта с помощью docker-compose
8. Создать и применить миграции в базу данных:
```
python manage.py makemigrations
python manage.py migrate
```
8. Запустить сервер
```
python manage.py runserver
```

9. Запустить сервер
```
python manage.py runserver
```

10. Перейти по адресу ниже. Джанго должна ответить - "Run scrap info by Google API" - это значит запушен процесс обновления данных из Google Sheets. Можно изменять их и отслеживать результат
```
http://0.0.0.0:8000/runner/
```

## Подготовка фронтэнд части для отображения результатов на React.JS (Фронт, к сожалению, не завернут в Docker)
1. Установить зависимости npm - 

```
npm install
```

1.9 Возможно нужно будет установить React
```
npm i react react-dom --save-dev
```
1.9.1 Никогда с первого раза не получалось установить что-то с помощью npm =( Возможно придётся поиграться с версиями

2. Для запуска webpack запустите - 
```
npm run dev
```

3. Перейдите по адресу, с "поднятым" Django,  для просмотра таблички с заказами
```
http://0.0.0.0:8000
```

## Установка проекта с помощью docker-compose
1. Склонировать репозиторий с Github
```
git clone https://github.com/Greengo86/test_google_api.git
```
2. Перейти в директорию проекта
3. корневой директории создать файл .evn и заполнить необходимые переменные. TG_TOKEN токен чат бота Телеграмма и TG_ID - id пользователя телеграмма (нужно для уведомления о просрочке):
```
TG_TOKEN = '{}'
TG_ID = '{}'
```

4. Сбилдить и запустить контейнеры
``` 
docker-compose up --build
 ```

5. Перейти по адресу ниже. Джанго должна ответить - "Run scrap info by Google API" - это значит запушен процесс обновления данных из Google Sheets. Можно изменять их и отслеживать результат
```
http://0.0.0.0:8000/runner/
```

![TG](https://github.com/Greengo86/test_google_api/blob/Second_Implementation_update_records/TG%20Notify.png)

![React](https://github.com/Greengo86/test_google_api/blob/Second_Implementation_update_records/React.png)