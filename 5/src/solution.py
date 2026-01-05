import psycopg2
from psycopg2.extras import DictCursor


conn = psycopg2.connect('postgresql://postgres:@localhost:5432/test_db')


# BEGIN (write your solution here)
def create_post(connection, post_data):
    """Создает новый пост и возвращает его id."""
    query = """
        INSERT INTO posts (title, content, author_id)
        VALUES (%s, %s, %s)
        RETURNING id;
    """
    with connection.cursor() as cursor:
        cursor.execute(query, (post_data['title'], post_data['content'], post_data['author_id']))
        post_id = cursor.fetchone()[0]
        connection.commit()
    return post_id

def add_comment(connection, comment_data):
    """Добавляет новый комментарий и возвращает его id."""
    query = """
        INSERT INTO comments (post_id, author_id, content)
        VALUES (%s, %s, %s)
        RETURNING id;
    """
    with connection.cursor() as cursor:
        cursor.execute(query, (comment_data['post_id'], comment_data['author_id'], comment_data['content']))
        comment_id = cursor.fetchone()[0]
        connection.commit()
    return comment_id

def get_latest_posts(connection, n):
    """Возвращает n последних постов с комментариями."""
    # Получаем последние n постов
    posts_query = """
        SELECT id, title, content, author_id, created_at
        FROM posts
        ORDER BY created_at DESC
        LIMIT %s;
    """
    
    with connection.cursor(cursor_factory=DictCursor) as cursor:
        cursor.execute(posts_query, (n,))
        posts = cursor.fetchall()
        
        result = []
        for post in posts:
            # Для каждого поста получаем его комментарии
            comments_query = """
                SELECT id, author_id, content, created_at
                FROM comments
                WHERE post_id = %s
                ORDER BY created_at ASC;
            """
            cursor.execute(comments_query, (post['id'],))
            comments = cursor.fetchall()
            
            # Преобразуем пост в словарь
            post_dict = dict(post)
            
            # Добавляем комментарии в формате списка словарей
            post_dict['comments'] = [dict(comment) for comment in comments]
            
            result.append(post_dict)
        
    return result

# END
