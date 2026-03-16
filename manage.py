import sqlite3
import os
from datetime import datetime
import argparse

DB_PATH = os.path.join(os.path.dirname(__file__), "tasks.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            title    TEXT NOT NULL,
            status   TEXT NOT NULL DEFAULT 'pending',
            priority TEXT NOT NULL DEFAULT 'medium',
            created  TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def add_task(title, priority="medium"):
    conn = get_connection()
    conn.execute(
        "INSERT INTO tasks (title, priority, created) VALUES (?, ?, ?)",
        (title, priority, datetime.now().strftime("%Y-%m-%d %H:%M"))
    )
    conn.commit()
    conn.close()
    print(f"[+] Task added: \"{title}\" [{priority}]")


def list_tasks(filter_status=None):
    conn = get_connection()
    if filter_status:
        rows = conn.execute(
            "SELECT * FROM tasks WHERE status = ? ORDER BY id", (filter_status,)
        ).fetchall()
    else:
        rows = conn.execute("SELECT * FROM tasks ORDER BY id").fetchall()
    conn.close()

    if not rows:
        print("No tasks found.")
        return

    print(f"\n{'ID':<5} {'Title':<35} {'Status':<12} {'Priority':<10} {'Created'}")
    print("-" * 80)
    for row in rows:
        status_icon = "✓" if row["status"] == "complete" else "○"
        print(f"{row['id']:<5} {row['title']:<35} {status_icon} {row['status']:<10} {row['priority']:<10} {row['created']}")
    print()


def complete_task(task_id):
    conn = get_connection()
    cursor = conn.execute(
        "UPDATE tasks SET status = 'complete' WHERE id = ?", (task_id,)
    )
    conn.commit()
    conn.close()
    if cursor.rowcount == 0:
        print(f"[!] No task found with ID {task_id}")
    else:
        print(f"[✓] Task {task_id} marked as complete.")


def delete_task(task_id):
    conn = get_connection()
    cursor = conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    if cursor.rowcount == 0:
        print(f"[!] No task found with ID {task_id}")
    else:
        print(f"[-] Task {task_id} deleted.")


init_db()

def build_parser():
    parser = argparse.ArgumentParser(
        prog="manage.py",
        description="Task Manager CLI — manage your tasks from the terminal."
    )
    subparsers = parser.add_subparsers(dest="command")

    # add
    p_add = subparsers.add_parser("add", help="Add a new task")
    p_add.add_argument("title", help="Task title")
    p_add.add_argument(
        "--priority", choices=["low", "medium", "high"], default="medium",
        help="Task priority (default: medium)"
    )

    # list
    p_list = subparsers.add_parser("list", help="List all tasks")
    p_list.add_argument(
        "--status", choices=["pending", "complete"],
        help="Filter by status"
    )

    # complete
    p_complete = subparsers.add_parser("complete", help="Mark a task as complete")
    p_complete.add_argument("id", type=int, help="Task ID")

    # delete
    p_delete = subparsers.add_parser("delete", help="Delete a task")
    p_delete.add_argument("id", type=int, help="Task ID")

    return parser


if __name__ == "__main__":
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "add":
        add_task(args.title, args.priority)
    elif args.command == "list":
        list_tasks(args.status)
    elif args.command == "complete":
        complete_task(args.id)
    elif args.command == "delete":
        delete_task(args.id)
    else:
        parser.print_help()