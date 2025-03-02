import sqlite3
import datetime

DATABASE = 'blog.db'  # Name of the SQLite database file

def get_db():
    """Gets a database connection."""
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

def init_db():
    """Initializes the database with necessary tables."""
    db = get_db()
    with open('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()

def get_all_posts():
    """Retrieves all blog posts from the database."""
    db = get_db()
    posts = db.execute('SELECT * FROM posts ORDER BY timestamp DESC').fetchall()
    db.close()
    return [dict(row) for row in posts]

def get_post_by_id(post_id):
    """Retrieves a single blog post by its ID."""
    db = get_db()
    post = db.execute('SELECT * FROM posts WHERE post_id = ?', (post_id,)).fetchone()
    replies = db.execute('SELECT * FROM replies WHERE post_id = ? ORDER BY timestamp DESC', (post_id,)).fetchall()
    db.close()
    if post:
        post_dict = dict(post)
        post_dict['replies'] = [dict(row) for row in replies]
        return post_dict
    return None

def create_new_post(content):
    """Creates a new blog post."""
    db = get_db()
    now = datetime.datetime.now()
    db.execute('INSERT INTO posts (content, timestamp) VALUES (?, ?)', (content, now))
    db.commit()
    db.close()

def create_new_reply(post_id, content):
    """Adds a reply to a blog post."""
    db = get_db()
    now = datetime.datetime.now()
    db.execute('INSERT INTO replies (post_id, content, timestamp) VALUES (?, ?, ?)', (post_id, content, now))
    db.commit()
    db.close()

def delete_post(self, post_id):
    with self.get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM posts WHERE id = ?', (post_id,))
        conn.commit()

# Initialize the database when data.py is imported
# Comment this line if you already have the db created.
init_db()

class data_manager: # the class is required for app.py to work correctly.
    pass
data_manager.get_all_posts = get_all_posts
data_manager.get_post_by_id = get_post_by_id
data_manager.create_new_post = create_new_post
data_manager.create_new_reply = create_new_reply
