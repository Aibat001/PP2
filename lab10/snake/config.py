import psycopg2

# Параметры подключения
params = {
    "host": "localhost",
    "port": 5432,
    "database": "snake",
    "user": "postgres",
    "password": "Aizat7203&",
    "options": "-c client_encoding=utf8"
}

try:
    # Устанавливаем соединение с базой данных
    conn = psycopg2.connect(**params)
    print("Подключение к базе данных установлено")

    # Дальнейший код работы с базой данных
    # ...

except (Exception, psycopg2.Error) as error:
    print("Ошибка при подключении к PostgreSQL:", error)
