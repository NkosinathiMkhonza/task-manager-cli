# task-manager-cli

A command-line task manager built with Python and SQLite — with a terminal-style web interface powered by Flask.

---

## Features

- Add tasks with priority levels (low, medium, high)
- List all tasks or filter by status
- Mark tasks as complete
- Delete individual tasks
- Persistent storage with SQLite
- REST API built with Flask
- Terminal-style web interface to demo the app in the browser

---

## Requirements

- Python 3.8+
- Flask

---

## Installation
```bash
git clone https://github.com/NkosinathiMkhonza/task-manager-cli.git
cd task-manager-cli
pip install -r requirements.txt
```

---

## Running the Web Interface
```bash
python app.py
```

Then open your browser at `http://127.0.0.1:5000`

---

## CLI Usage
```bash
# Add a task
python manage.py add "Finish portfolio"
python manage.py add "Study Django REST Framework" --priority high

# List all tasks
python manage.py list

# Filter by status
python manage.py list --status pending
python manage.py list --status complete

# Mark complete
python manage.py complete 1

# Delete a task
python manage.py delete 2
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/tasks` | Get all tasks |
| GET | `/api/tasks?status=pending` | Filter by status |
| POST | `/api/tasks` | Add a new task |
| PATCH | `/api/tasks/<id>/complete` | Mark task complete |
| DELETE | `/api/tasks/<id>` | Delete a task |

---

## Project Structure
```
task-manager-cli/
├── manage.py          # Core CLI — CRUD functions and argument parser
├── app.py             # Flask REST API
├── static/
│   └── index.html     # Terminal-style web interface
├── requirements.txt   # Dependencies
├── tasks.db           # SQLite database (auto-created)
└── README.md
```

---

## Author

**Nkosinathi Mkhonza** — [github.com/NkosinathiMkhonza](https://github.com/NkosinathiMkhonza)# task-manager-cli

A command-line task manager built with Python and SQLite. Manage your tasks directly from the terminal — add, list, complete, and delete tasks with a clean CLI interface.

---

## Features

- Add tasks with priority levels (low, medium, high)
- List all tasks or filter by status
- Mark tasks as complete
- Delete individual tasks
- Persistent storage with SQLite — tasks survive between sessions
- Zero external dependencies — pure Python standard library

---

## Requirements

- Python 3.8+

---

## Installation
```bash
git clone https://github.com/NkosinathiMkhonza/task-manager-cli.git
cd task-manager-cli
```
---

## Usage
```bash
# Add a task
python manage.py add "Finish portfolio"
python manage.py add "Study Django REST Framework" --priority high

# List all tasks
python manage.py list

# Filter by status
python manage.py list --status pending
python manage.py list --status complete

# Mark complete
python manage.py complete 1

# Delete a task
python manage.py delete 2
```

---

## Example Output
```
$ python manage.py list

ID    Title                               Status       Priority   Created
--------------------------------------------------------------------------------
1     Finish portfolio                    ○ pending    high       2026-03-15 10:00
2     Study DRF                           ○ pending    medium     2026-03-15 10:01

$ python manage.py complete 1
[✓] Task 1 marked as complete.
```

---

## Project Structure
```
task-manager-cli/
├── manage.py    # CLI entry point — all commands and database logic
├── tasks.db     # SQLite database (auto-created on first run)
└── README.md
```

---

## Author

**Nkosinathi Mkhonza** — [github.com/NkosinathiMkhonza](https://github.com/NkosinathiMkhonza)
