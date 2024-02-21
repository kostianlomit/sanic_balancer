# Сервис-балансировщик видео-трафика

JSON API сервис, который позволяет обрабатывать входящие запросы и переходит на другой CDN сервер при N запросе. 

## Используемый стек

- [Sanic](https://sanic.dev/en/) Молниеносный асинхронный веб-фреймворк Python для создания API.
- [MySQL](https://www.mysqltutorial.org/) — сшироко используемая система управления реляционными базами данных (СУБД).
- [Uvicorn](https://www.uvicorn.org/) реализация веб-сервера ASGI для Python.
- [Alembic](https://alembic.sqlalchemy.org/en/latest/) облегченный инструмент миграции баз данных для использования с SQLAlchemy.
- [Pytest](https://docs.pytest.org/en/7.4.x/contents.html) полнофункциональный инструмент тестирования на Python
- [Docker](https://docs.docker.com/get-started/overview/) открытая платформа для разработки, доставки и запуска приложений.
- [Docker compose](https://docs.docker.com/compose/) инструмент для определения и запуска многоконтейнерных приложений Docker. 


## Установка 
ВНИМАНИЕ! Для проведения установки необходимо, чтобы пользователь от которого выполняются действия находился в группе `sudo`
### Порядок действий:
1. Установите Docker по [инструкции с сайта Docker](https://docs.docker.com/engine/install/ubuntu/)
2. Установите ”make”
    ```bash
    sudo apt install make
    ```
2. Склонируйте репозиторий на сервер, например, в директорию: `/home/<user>/`:

    ```bash
    sudo git clone 
    ```
3. Перейдите в каталог с сервисом:

    ```bash
    cd sanic_balancer
    ```
4. При необходимости измените параметры в `Makefile` и `docker-compose.yml`
5. Отредактируйте файл `.env-non-dev`
   ```bash
   DB_HOST=db #хост продакшн-базы 
   DB_PORT=5432 #порт продакшн-базы 
   DB_NAME=mysql #название продакшн-базы 
   DB_USER=mysql #имя пользователя продакшн-базы 
   DB_PASS=mysql #пароль пользователя продакшн-базы 
   
   Mysql_DB=mysql 
   Mysql_USER=mysql 
   Mysql_PASSWORD=mysql 
    ```
6. Выполните команду:

    ```bash
    sudo make container
    ```

7. Запустите сервис с помощью Docker Compose:

    ```bash
    sudo docker compose -p sanic_balancer \
                -f docker-compose.yml \
                up -d
    ```
8. Проверьте работоспособность сервиса в соответствии с настройками

## Остановка сервиса

Для остановки сервиса выполните следующую команду:

   ```bash
   sudo docker compose -p sanic_balancer  stop
   ```

## Работа сервиса
Сервис имеет один эндпоинт:

- `GET /origin` принимает на вход url, ведущий на сервер и перенаправляет на CDN_server
- при N запросе.
  Пример отправки HTTP-запроса:
  ```bash
  curl -X 'GET' \
  'http://0.0.0.0:8000/origin' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{ "'http://balancer-domain/?video=http://s1.origin-cluster/video/1488/xcg2djHcka
d.m3u8'"}'

- `GET /origin` последующие запросы редиректятся на '/CDN_server'
  Пример отправки HTTP-запроса:
  ```bash
  curl -X 'GET' \
  'http://0.0.0.0:8000/origin' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{ "'http://{app.config.CDN_HOST}/s1/video/1488/xcg2djHckad.m3u8'"}'

  ```


Подробная документация доступна по эндпоинту : `GET <sanic>/docs/swagger` 

## Тестирование
Выполните команду 
```python3
sudo docker exec sanic_balancer pytest test/conftest.py
```

unit
## Версия

23.10
