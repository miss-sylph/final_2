import psycopg2
import time

# Конфигурация подключения к базе данных
DB_CONFIG = {
    "host": "postgres",           # Хост базы данных (имя сервиса PostgreSQL в docker-compose.yml)
    "port": 5432,                 # Порт базы данных
    "dbname": "test_db",          # Имя базы данных
    "user": "postgres",           # Пользователь базы данных
    "password": "password"        # Пароль базы данных
}

def connect_to_db():
    """
    Функция для подключения к базе данных с повторными попытками.
    """
    retries = 5  # Количество попыток подключения
    while retries > 0:
        try:
            # Подключение к базе данных
            conn = psycopg2.connect(**DB_CONFIG)
            print("Подключение к базе данных успешно!")
            return conn
        except psycopg2.OperationalError as e:
            # Обработка ошибки подключения
            print(f"Ошибка подключения к базе данных: {e}")
            retries -= 1
            print(f"Повторная попытка через 5 секунд... Осталось попыток: {retries}")
            time.sleep(5)

    # Если все попытки исчерпаны
    raise Exception("Не удалось подключиться к базе данных после нескольких попыток.")

def create_and_populate_table(conn):
    """
    Создание таблицы и наполнение ее данными.
    """
    try:
        with conn.cursor() as cursor:
            # Создание таблицы
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS employees (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(50) NOT NULL,
                    position VARCHAR(50) NOT NULL,
                    salary INT NOT NULL
                );
            """)
            print("Таблица employees создана или уже существует.")

            # Наполнение таблицы данными
            cursor.execute("""
                INSERT INTO employees (name, position, salary)
                VALUES 
                ('Alice', 'Manager', 100000),
                ('Bob', 'Developer', 90000),
                ('Charlie', 'Analyst', 85000)
                ON CONFLICT DO NOTHING;
            """)
            print("Таблица employees заполнена данными.")
    except Exception as e:
        print(f"Ошибка при создании или заполнении таблицы: {e}")

def fetch_and_print_table_data(conn):
    """
    Получение и вывод данных из таблицы.
    """
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM employees;")
            rows = cursor.fetchall()

            print("Данные из таблицы employees:")
            print("ID | Name    | Position   | Salary")
            print("---------------------------------")
            for row in rows:
                print(f"{row[0]}  | {row[1]} | {row[2]} | {row[3]}")
    except Exception as e:
        print(f"Ошибка при извлечении данных из таблицы: {e}")

def main():
    """
    Основная функция приложения.
    """
    try:
        # Подключение к базе данных
        conn = connect_to_db()

        # Создание таблицы и наполнение ее данными
        create_and_populate_table(conn)

        # Получение и вывод данных из таблицы
        fetch_and_print_table_data(conn)

        # Закрытие соединения
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    main()
