# Домашнее задание к лекции «Flask»


Проект REST API (backend) для сайта объявлений.
В качестве фреймворка использован Flask.

## Документация по проекту

Для запуска проекта необходимо:

Переопределить переменные окружения через параметр -e в строке запуска контейнера:
DB_USER  
DB_PASSWORD  
DB_HOST   
DB_PORT   
DB_NAME   
secret_key

Собрать image при помощи команды:

`docker build -t flask-app .`

Запустить контейнер при помощи команды:

`docker run --network host --rm --name flask-app -d  flask-app:latest`


Перейти на соответствующий эндпоинт в соответствии с описанием API-сервиса:

`http://127.0.0.1:5000/login`  
`http://127.0.0.1:5000/api/v1/user`  
`http://127.0.0.1:5000/api/v1/advertisement`