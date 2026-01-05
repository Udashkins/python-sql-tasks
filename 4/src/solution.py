import psycopg2
from psycopg2.extras import DictCursor


conn = psycopg2.connect('postgresql://postgres:@localhost:5432/test_db')


# BEGIN (write your solution here)
def get_order_sum(conn, month):
    """
    Возвращает строку с общей суммой заказов каждого покупателя за указанный месяц.
    
    Args:
        conn: соединение с БД
        month: номер месяца (1-12)
    
    Returns:
        str: отформатированная строка с результатами
    """
    result_lines = []
    
    # SQL запрос для получения суммы заказов по покупателям за указанный месяц
    query = """
    SELECT 
        c.customer_name,
        COALESCE(SUM(o.total_amount), 0) as total_sum
    FROM customers c
    LEFT JOIN orders o ON c.customer_id = o.customer_id
        AND EXTRACT(MONTH FROM o.order_date) = %s
    GROUP BY c.customer_id, c.customer_name
    HAVING COALESCE(SUM(o.total_amount), 0) > 0
    ORDER BY c.customer_name  -- Изменено: сортировка по имени покупателя
    """
    
    try:
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(query, (month,))
            rows = cursor.fetchall()
            
            for row in rows:
                customer_name = row['customer_name']
                total_sum = row['total_sum']
                result_lines.append(f"Покупатель {customer_name} совершил покупок на сумму {int(total_sum)}")
        
        return "\n".join(result_lines)
        
    except Exception as e:
        print(f"Ошибка при выполнении запроса: {e}")
        return ""
    
# END
