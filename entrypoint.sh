#!/bin/bash
set -e

echo "⌛ Ожидаем базу данных..."
sleep 3

echo "⚙ Применяем миграции..."
python run_migrations.py

echo "🚀 Запускаем бота..."
python main.py