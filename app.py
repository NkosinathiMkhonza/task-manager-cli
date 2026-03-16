from flask import Flask, jsonify, request
from manage import init_db, add_task, list_tasks, complete_task, delete_task
import sqlite3
import os

app = Flask(__name__)
DB_PATH = os.path.join(os.path.dirname(__file__), "tasks.db")


def get_tasks_as_dict(filter_status=None):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    if filter_status:
        rows = conn.execute(
            "SELECT * FROM tasks WHERE status = ? ORDER BY id", (filter_status,)
        ).fetchall()
    else:
        rows = conn.execute("SELECT * FROM tasks ORDER BY id").fetchall()
    conn.close()
    return [dict(row) for row in rows]


@app.route("/")
def index():
    return app.send_static_file("index.html")


@app.route("/api/tasks", methods=["GET"])
def api_list_tasks():
    status = request.args.get("status")
    tasks = get_tasks_as_dict(status)
    return jsonify(tasks)


@app.route("/api/tasks", methods=["POST"])
def api_add_task():
    data = request.get_json()
    title = data.get("title", "").strip()
    priority = data.get("priority", "medium")
    if not title:
        return jsonify({"error": "Title is required"}), 400
    add_task(title, priority)
    tasks = get_tasks_as_dict()
    return jsonify({"message": f"Task added: {title}", "tasks": tasks}), 201


@app.route("/api/tasks/<int:task_id>/complete", methods=["PATCH"])
def api_complete_task(task_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.execute(
        "UPDATE tasks SET status = 'complete' WHERE id = ?", (task_id,)
    )
    conn.commit()
    conn.close()
    if cursor.rowcount == 0:
        return jsonify({"error": f"No task with ID {task_id}"}), 404
    return jsonify({"message": f"Task {task_id} marked as complete."})


@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def api_delete_task(task_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    if cursor.rowcount == 0:
        return jsonify({"error": f"No task with ID {task_id}"}), 404
    return jsonify({"message": f"Task {task_id} deleted."})


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)