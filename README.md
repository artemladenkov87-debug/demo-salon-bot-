# 💇 Demo: Бот записи для салона красоты

Telegram-бот для записи клиентов. Демо-проект для портфолио.

**Попробовать:** [ссылка на бота]

## Возможности

- Запись на 4 услуги к 3 мастерам
- Выбор даты (5 ближайших дней) и свободного времени
- Защита от двойной записи на одного мастера
- Уведомление администратора при каждой записи

## Запуск локально

pip install -r requirements.txt
cp .env.example .env
# Заполнить BOT_TOKEN и ADMIN_ID в .env
python main.py

## Деплой на Railway

1. railway.app → New Project → Deploy from GitHub
2. Settings → Variables → добавить BOT_TOKEN, ADMIN_ID, SALON_NAME
3. `railway up` или автодеплой при пуше

## Настройка под клиента

Все параметры в `config.py`:
- `SALON_NAME` — название
- `SERVICES` — услуги, цены, длительность
- `MASTERS` — имена мастеров
- `TIME_SLOTS` — временные слоты
