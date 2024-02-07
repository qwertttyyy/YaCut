# YaCut

## Описание проекта

YaCut - это сервис укорачивания ссылок, предназначенный для создания коротких версий длинных URL-адресов. Это удобный инструмент для деления ссылок в интернете, позволяющий пользователю либо предложить свой вариант короткой ссылки, либо воспользоваться автоматически сгенерированным сервисом.

### Ключевые возможности:

- Генерация коротких ссылок, ассоциированных с исходными длинными URL.
- Переадресация на исходный адрес при обращении к короткой ссылке.
- Пользовательский интерфейс с формой для ввода длинного URL и (необязательно) предложенного варианта короткой ссылки.

### Технологии:

- Python
- Flask
- SQLAlchemy
- SQLite

## API

YaCut API позволяет создавать и получать короткие ссылки через HTTP-запросы. Сервис поддерживает следующие эндпоинты:

- `POST /api/id/` для создания новой короткой ссылки.
- `GET /api/id/<short_id>/` для получения оригинальной ссылки по короткому идентификатору.

Для подробной документации по API и примеров использования см. спецификацию `openapi.yml`.

## Установка и запуск

Для запуска проекта выполните следующие шаги:

1. Клонирование репозитория:

```bash
git clone git@github.com:qwertttyyy/yacut.git
```

2. Создать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

3. Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```
4. Инициализация базы данных:
```bash
flask db upgrade
```
5. Запуск сервера Flask:
```bash
flask run
```
После запуска сервера сервис будет доступен по адресу http://localhost:5000.
