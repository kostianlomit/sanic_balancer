#!/bin/bash

# Выполнение Alembic миграций
alembic upgrade head

cd src

# Запуск приложения
uvicorn main:app --host 0.0.0.0 --port 8000
