import psycopg2
from psycopg2.extras import execute_values

conn = psycopg2.connect('postgresql://postgres:@localhost:5432/test_db')


# BEGIN (write your solution here)
def batch_insert(conn, products):
    """
    Массово добавляет товары в базу данных.
    
    Args:
        conn: соединение с базой данных
        products: список словарей с товарами, где каждый словарь содержит
                  ключи 'name', 'price', 'quantity'
    """
    # Подготавливаем данные для вставки
    values = [(product['name'], product['price'], product['quantity']) 
              for product in products]
    
    # SQL запрос с плейсхолдерами
    sql = """
        INSERT INTO products (name, price, quantity)
        VALUES %s
    """
    
    # Выполняем массовую вставку
    with conn.cursor() as cursor:
        execute_values(cursor, sql, values)
    conn.commit()


def get_all_products(conn):
    """
    Возвращает все товары из базы данных, отсортированные по цене по убыванию.
    
    Args:
        conn: соединение с базой данных
        
    Returns:
        Список кортежей с данными товаров
    """
    sql = """
        SELECT id, name, price, quantity
        FROM products
        ORDER BY price DESC
    """
    
    with conn.cursor() as cursor:
        cursor.execute(sql)
        result = cursor.fetchall()
    
    return result

# END
