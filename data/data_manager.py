import json
import os
from datetime import datetime

DATA_FILE = "data/blog_posts.json"

def load_data():
  """Loads data from the JSON file."""
  if not os.path.exists("data"):
      os.makedirs("data")
  if not os.path.exists(DATA_FILE):
      with open(DATA_FILE, "w") as f:
          json.dump([], f)

  with open(DATA_FILE, "r") as file:
      try:
          data = json.load(file)
          return data
      except json.JSONDecodeError:
          return []


def save_data(data):
    """Saves data to the JSON file."""
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

def create_new_post(content):
    """
    Creates a new post, and saves it to the JSON file.
    """
    data = load_data()
    new_post_id = max((post["post_id"] for post in data), default=0) + 1
    new_post = {
        "post_id": new_post_id,
        "content": content,
        "timestamp": datetime.now().isoformat(),
        "replies": []
    }
    data.append(new_post)
    save_data(data)
    return new_post_id

def get_all_posts():
    """Retrieves all blog posts."""
    return load_data()

def get_post_by_id(post_id):
    """Retrieves a post by its ID."""
    data = load_data()
    for post in data:
        if post["post_id"] == post_id:
            return post
    return None

def create_new_reply(post_id, content):
    """
    Adds a new reply to a post.
    """
    data = load_data()
    post = get_post_by_id(post_id)
    if post:
        new_reply_id = max((reply["reply_id"] for reply in post["replies"]), default=0) + 1
        new_reply = {
            "reply_id": new_reply_id,
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
        post["replies"].append(new_reply)
        save_data(data)
        return new_reply_id
    return None