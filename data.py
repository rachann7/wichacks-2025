import sqlite3
from datetime import datetime

DATABASE = 'blog.db'

def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

def init_db():
    db = get_db()
    with open('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()

class DataManager:
    @staticmethod
    def get_all_posts():
        try:
            db = get_db()
            posts = db.execute('''
                SELECT post_id, title, content, author, created_at 
                FROM posts 
                ORDER BY created_at DESC
            ''').fetchall()
            return [dict(row) for row in posts]
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []
        finally:
            db.close()

    @staticmethod
    def create_new_post(content, title, author):
        try:
            db = get_db()
            cursor = db.cursor()
            cursor.execute('''
                INSERT INTO posts (title, content, author)
                VALUES (?, ?, ?)
            ''', (title, content, author))
            db.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            db.rollback()
            return None
        finally:
            db.close()

    @staticmethod
    def get_post_by_id(post_id):
        try:
            db = get_db()
            post = db.execute('''
                SELECT post_id, title, content, author, created_at
                FROM posts 
                WHERE post_id = ?
            ''', (post_id,)).fetchone()
            return dict(post) if post else None
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None
        finally:
            db.close()

data_manager = DataManager()

if __name__ == '__main__':
    init_db()