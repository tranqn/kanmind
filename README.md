# Kanmind – Kanban Board API

A RESTful API backend for a Kanban-style project management application, built with Django and Django REST Framework.

## Tech Stack

- Python 3.11+
- Django 4.2
- Django REST Framework 3.14
- Token Authentication
- SQLite (development)

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/tranqn/kanmind.git
cd kanmind
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
# .venv\Scripts\activate    # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply migrations

```bash
python manage.py migrate
```

### 5. Create a superuser (optional, for admin access)

```bash
python manage.py createsuperuser
```

### 6. Run the development server

```bash
python manage.py runserver
```

The API is now available at `http://127.0.0.1:8000/`.

### 7. Launch the frontend

The `frontend/` directory contains a Vanilla JS single-page app. Open it with VS Code's **Live Server** extension (right-click `frontend/index.html` → **Open with Live Server**) while the Django server is running.

## Project Structure

```
kanmind/
├── core/               # Django project config (settings, urls, wsgi)
├── auth_app/           # Authentication: registration, login, email-check
│   └── api/            # serializers, views, urls
├── kanban_app/         # Boards, tasks, comments
│   └── api/            # serializers, views, urls, permissions
├── frontend/           # Vanilla JS frontend (served via Live Server)
├── manage.py
└── requirements.txt
```

## API Endpoints

### Authentication (no token required)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/registration/` | Register new user |
| POST | `/api/login/` | Login and receive token |

### Users (token required)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/email-check/?email=...` | Look up user by email |

### Boards (token required)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/boards/` | List boards (owner or member) |
| POST | `/api/boards/` | Create a new board |
| GET | `/api/boards/{id}/` | Board detail with tasks |
| PATCH | `/api/boards/{id}/` | Update title and members |
| DELETE | `/api/boards/{id}/` | Delete board (owner only) |

### Tasks (token required)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/tasks/assigned-to-me/` | Tasks assigned to me |
| GET | `/api/tasks/reviewing/` | Tasks I'm reviewing |
| POST | `/api/tasks/` | Create a task |
| PATCH | `/api/tasks/{id}/` | Update a task |
| DELETE | `/api/tasks/{id}/` | Delete a task |

### Comments (token required)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/tasks/{id}/comments/` | List comments for a task |
| POST | `/api/tasks/{id}/comments/` | Add a comment |
| DELETE | `/api/tasks/{id}/comments/{comment_id}/` | Delete a comment (author only) |

## Admin

Access the Django admin at `http://127.0.0.1:8000/admin/` using your superuser credentials.

## Notes

- The database file (`db.sqlite3`) is **not** committed to version control.
- Token authentication: include `Authorization: Token <your_token>` in request headers.
- Task status values: `to-do`, `in-progress`, `review`, `done`
- Task priority values: `low`, `medium`, `high`
