from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Sample data to simulate a database (replace with a real database in a production app)
tasks = []
task_id_counter = 1

@app.route('/objective')
def objective():
    """
    Renders the Our Objective page.
    """
    return render_template('objective.html')

@app.route('/')
def index():
    """
    Redirects to the Our Objective page.
    """
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
