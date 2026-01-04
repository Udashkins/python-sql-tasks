import psycopg2

conn = psycopg2.connect('postgresql://postgres:@localhost:5432/test_db')


# BEGIN (write your solution here)
def make_cars_table(connection):
    """Создает таблицу cars в базе данных"""
    with connection.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cars (
                id SERIAL PRIMARY KEY,
                brand VARCHAR(255) NOT NULL,
                model VARCHAR(255) NOT NULL
            )
        """)
    connection.commit()


def populate_cars_table(connection, cars):
    """Добавляет автомобили в таблицу cars"""
    with connection.cursor() as cursor:
        # Используем execute_batch для эффективной вставки нескольких записей
        for car in cars:
            cursor.execute(
                "INSERT INTO cars (brand, model) VALUES (%s, %s)",
                car
            )
    connection.commit()


def get_all_cars(connection):
    """Возвращает все автомобили из таблицы cars, отсортированные по марке"""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT * FROM cars 
            ORDER BY brand ASC
        """)
        return cursor.fetchall()
# END
