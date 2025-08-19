from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)
DB_PATH = 'tasks.db'

# DB接続
def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# DB初期化
def init_db():
    if not os.path.exists(DB_PATH):
        conn = get_conn()
        c = conn.cursor()
        # 日付カラム date 追加
        c.execute('CREATE TABLE tasks (id INTEGER PRIMARY KEY, title TEXT, list_name TEXT, date TEXT)')
        conn.commit()
        conn.close()

# トップページ
@app.route('/')
def index():
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT * FROM tasks")
    tasks = c.fetchall()
    conn.close()
    lists = ['To Do', 'In Progress', 'Done']
    return render_template('index.html', tasks=tasks, lists=lists)

# タスク追加
@app.route('/add', methods=['POST'])
def add():
    title = request.form['title']
    list_name = request.form['list_name']
    date = request.form.get('date', '')  # 日付取得
    conn = get_conn()
    conn.execute("INSERT INTO tasks (title, list_name, date) VALUES (?, ?, ?)", (title, list_name, date))
    conn.commit()
    conn.close()
    return redirect('/')

# タスク削除
@app.route('/delete/<int:task_id>')
def delete(task_id):
    conn = get_conn()
    conn.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()
    conn.close()
    return redirect('/')

# タスク移動
@app.route('/move/<int:task_id>/<new_list>')
def move(task_id, new_list):
    conn = get_conn()
    conn.execute("UPDATE tasks SET list_name=? WHERE id=?", (new_list, task_id))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
