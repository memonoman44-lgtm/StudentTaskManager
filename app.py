
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

DATABASE = "database.db"


# Database connection
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# Create database table
def create_table():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            subject TEXT,
            due_date TEXT,
            status TEXT DEFAULT 'Pending'
        )
    """)

    conn.commit()
    conn.close()


# Display tasks
@app.route("/")
def home():

    conn = get_db()

    tasks = conn.execute(
        "SELECT * FROM tasks ORDER BY id DESC"
    ).fetchall()

    total = len(tasks)

    completed = sum(
        1 for task in tasks
        if task["status"] == "Completed"
    )

    pending = total - completed

    conn.close()

    return render_template(
        "index.html",
        tasks=tasks,
        total=total,
        completed=completed,
        pending=pending
    )


# Add task
@app.route("/add", methods=["POST"])
def add_task():

    title = request.form.get("title", "").strip()
    subject = request.form.get("subject", "").strip()
    due_date = request.form.get("due_date", "")

    if title:

        conn = get_db()

        conn.execute("""
            INSERT INTO tasks (title, subject, due_date)
            VALUES (?, ?, ?)
        """, (title, subject, due_date))

        conn.commit()
        conn.close()

    return redirect(url_for("home"))


# Complete task
@app.route("/complete/<int:task_id>")
def complete_task(task_id):

    conn = get_db()

    conn.execute("""
        UPDATE tasks
        SET status = 'Completed'
        WHERE id = ?
    """, (task_id,))

    conn.commit()
    conn.close()

    return redirect(url_for("home"))


# Delete task
@app.route("/delete/<int:task_id>")
def delete_task(task_id):

    conn = get_db()

    conn.execute(
        "DELETE FROM tasks WHERE id = ?",
        (task_id,)
    )

    conn.commit()
    conn.close()

    return redirect(url_for("home"))


# Run application
if __name__ == "__main__":

    create_table()

    app.run(debug=True)
import sqlite3
from flask import Flask

app = Flask(__name__)

# 1. Database connection
def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


# 2. Create database table
def create_table():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            subject TEXT,
            due_date TEXT,
            status TEXT DEFAULT 'Pending'
        )
    """)

    conn.commit()
    conn.close()


# 3. Continue with your Flask routes
@app.route("/")
def home():
    pass