import sqlite3
from datetime import datetime

DATABASE = 'blog.db'

def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

def init_db():
    with open('schema.sql', mode='r') as f:
        db = get_db()
        db.cursor().executescript(f.read())
        db.commit()
        db.close()

class DataManager:
    @staticmethod
    def get_all_posts():
        db = get_db()
        posts = db.execute('SELECT post_id, title, content, author, created_at FROM posts ORDER BY created_at DESC').fetchall()
        db.close()
        return [dict(row) for row in posts]

    @staticmethod
    def get_post_by_id(post_id):
        db = get_db()
        post = db.execute('SELECT * FROM posts WHERE post_id = ?', (post_id,)).fetchone()
        db.close()
        if post:
            return dict(post)
        return None

    @staticmethod
    def create_new_post(content, title, author):
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            'INSERT INTO posts (title, content, author) VALUES (?, ?, ?)',
            (title, content, author)
        )
        db.commit()
        post_id = cursor.lastrowid
        db.close()
        return post_id

data_manager = DataManager()

if __name__ == '__main__':
    init_db()