from flask import Flask, render_template, request, redirect, url_for, jsonify

from data import data_manager  # Corrected line, we are not using from data manager

app = Flask(__name__,
    static_url_path='/static',  # Update static path
    static_folder='static',
    template_folder='templates'
)

# Sample data to simulate a database (replace with a real database in a production app)
tasks = []
task_id_counter = 1

@app.route('/objective')
def objective():
    """
    Renders the Our Objective page.
    """
    return render_template('objective.html')

@app.route('/chat')
def chat():
   return render_template('chat.html')

@app.route('/chat_endpoint', methods=['POST'])
def chat_endpoint():
    user_prompt = request.json.get('prompt')
    gemini_response = {"reply": "This is a simulated response from Google Gemini."} #replace w gemini api
    return jsonify(gemini_response)

@app.route("/blog", methods=["GET", "POST"])
def blog_posts():
    """
    Displays and handles blog posts.
    """
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        if title and content:
            # Default author for now
            data_manager.create_new_post(content, title, "Anonymous")
            return redirect(url_for("blog_posts"))
    
    posts = data_manager.get_all_posts()
    return render_template("blog_posts.html", posts=posts)

# Added routes for creating and viewing posts
@app.route("/blog/create", methods=["GET", "POST"])
def create_post():
    """
    Handles creating a new blog post.
    """
    if request.method == "POST":
        content = request.form.get("content")
        if content:
            data_manager.create_new_post(content) # you need to use data_manager.create_new_post
            return redirect(url_for("blog_posts"))
    return render_template("create_post.html")

@app.route("/blog/post/<int:post_id>", methods=["GET", "POST"])
def view_post(post_id):
    post = data_manager.get_post_by_id(post_id)
    if not post:
        return "Post not found", 404
    
    if request.method == "POST":
        reply_content = request.form.get("reply_content")
        if reply_content:
            data_manager.create_new_reply(post_id, reply_content)
            return redirect(url_for("view_post", post_id=post_id))
    
    return render_template("view_post.html", post=post)

@app.route('/')
def index():
    return redirect(url_for('objective'))

@app.route('/add', methods=['POST'])
def add_task():
    """
    Adds a new task to the list.
    """
    global task_id_counter
    task_content = request.form.get('task')
    if task_content:
        tasks.append({'id': task_id_counter, 'content': task_content, 'completed': False})
        task_id_counter +=1
    return redirect(url_for('index'))

@app.route('/complete/<int:task_id>')
def complete_task(task_id):
  """
  Marks a task as complete by changing it's status
  """
  for task in tasks:
      if task['id'] == task_id:
        task['completed'] = True
        break
  return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    """
    Deletes a task from the list.
    """
    global tasks
    tasks = [task for task in tasks if task['id'] != task_id]
    return redirect(url_for('index'))

@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
  """
  Edits an existing task
  """
  task = next((task for task in tasks if task['id'] == task_id), None)

  if not task:
      return redirect(url_for('index'))

  if request.method == 'POST':
    new_content = request.form.get('new_task')
    if new_content:
        task['content'] = new_content
        return redirect(url_for('index'))

  return render_template('edit.html', task=task)

if __name__ == '__main__':
    app.run(debug=True)