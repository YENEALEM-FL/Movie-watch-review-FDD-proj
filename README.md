# WatchMate Backend API

Backend API service for the Movie Watch Review application built using Django and Django REST Framework.

---

# Overview

WatchMate is a movie watchlist and review backend application that provides REST APIs for:

- User authentication
- Watchlist management
- Movie reviews and ratings
- API pagination
- API throttling
- Permission management

The project uses SQLite as the default database and Django REST Framework for API development.

---

# Technology Stack

| Technology | Purpose |
|---|---|
| Python | Programming Language |
| Django | Web Framework |
| Django REST Framework | REST API Development |
| SQLite | Default Database |
| pip | Dependency Management |

---

# Project Structure

```text
Movie-watch-review-FDD-proj/
│
├── README.md
├── db.sqlite3
├── manage.py
├── requirements.txt
│
├── user_app/
│   ├── api/
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── migrations/
│   ├── models.py
│   └── test.py
│
├── watchlist_app/
│   ├── admin.py
│   ├── api/
│   │   ├── pagination.py
│   │   ├── permissions.py
│   │   ├── serializers.py
│   │   ├── throttling.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── migrations/
│   ├── models.py
│   ├── tests.py
│   └── views.py
│
└── watchmate/
    ├── asgi.py
    ├── settings.py
    ├── urls.py
    └── wsgi.py
```

---

# Features

## User Features

- User registration
- User authentication
- API-based login system

## Watchlist Features

- Create watchlists
- Retrieve watchlists
- Update watchlists
- Delete watchlists

## Review Features

- Add movie reviews
- Rating system
- Average rating calculation

## API Features

- Pagination
- Permissions
- Request throttling
- RESTful endpoints

---

# Prerequisites

Install the following before running the application:

| Software | Version |
|---|---|
| Python | 3.10+ |
| pip | Latest |
| Git | Latest |

---

# Clone Repository

```bash
git clone https://github.com/YENEALEM-FL/Movie-watch-review-FDD-proj.git
```

Navigate into the project:

```bash
cd Movie-watch-review-FDD-proj
```

---

# Create Virtual Environment

## Windows

```bash
python -m venv venv
venv\Scripts\activate
```

## macOS/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

# Install Dependencies

Install all required packages from `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

# Database Setup

Apply database migrations:

```bash
python manage.py migrate
```

---

# Create Superuser

Create an admin account:

```bash
python manage.py createsuperuser
```

Follow the prompts to enter:

- Username
- Email
- Password

---

# Run Development Server

Start the Django development server:

```bash
python manage.py runserver
```

Default server URL:

```text
http://127.0.0.1:8000/
```

---

# API Modules

## user_app

Handles:

- User APIs
- Authentication logic
- User serializers
- User endpoints

### Important Files

| File | Purpose |
|---|---|
| serializers.py | Data serialization |
| urls.py | API routing |
| views.py | API request handling |

---

## watchlist_app

Handles:

- Watchlist CRUD operations
- Reviews and ratings
- API permissions
- Pagination
- Throttling

### Important Files

| File | Purpose |
|---|---|
| pagination.py | API pagination |
| permissions.py | Custom permissions |
| serializers.py | Model serialization |
| throttling.py | API rate limiting |
| urls.py | Endpoint routing |
| views.py | API views |

---

# API Endpoints

## Watchlist APIs

| Method | Endpoint | Description |
|---|---|---|
| GET | `/watchlist/` | Retrieve all watchlists |
| POST | `/watchlist/` | Create watchlist |
| GET | `/watchlist/<id>/` | Retrieve single watchlist |
| PUT | `/watchlist/<id>/` | Update watchlist |
| DELETE | `/watchlist/<id>/` | Delete watchlist |

---

## Review APIs

| Method | Endpoint | Description |
|---|---|---|
| POST | `/review-create/` | Create review |
| GET | `/review/` | Retrieve reviews |

---

## User APIs

| Method | Endpoint | Description |
|---|---|---|
| POST | `/register/` | Register user |
| POST | `/login/` | User login |

---

# Running Tests

Execute application tests:

```bash
python manage.py test
```

---

# SQLite Database

The application uses SQLite by default.

Database file:

```text
db.sqlite3
```

No additional database installation is required for local development.

---

# Common Commands

## Run Server

```bash
python manage.py runserver
```

## Make Migrations

```bash
python manage.py makemigrations
```

## Apply Migrations

```bash
python manage.py migrate
```

## Run Tests

```bash
python manage.py test
```

## Create Superuser

```bash
python manage.py createsuperuser
```

---

# API Features

## Pagination

Implemented in:

```text
watchlist_app/api/pagination.py
```

Used to limit API response sizes.

---

## Permissions

Implemented in:

```text
watchlist_app/api/permissions.py
```

Controls access to protected endpoints.

---

## Throttling

Implemented in:

```text
watchlist_app/api/throttling.py
```

Limits excessive API requests.

---

# Troubleshooting

## ModuleNotFoundError

Ensure virtual environment is activated and dependencies are installed:

```bash
pip install -r requirements.txt
```

---

## Migration Errors

Delete old migration files if necessary and rerun:

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## Port Already in Use

Run server on another port:

```bash
python manage.py runserver 8089
```

---

# Future Improvements

- JWT authentication
- Docker support
- PostgreSQL integration
- Swagger/OpenAPI documentation
- CI/CD pipeline integration
- Cloud deployment

---

# Contribution Guide

## Create Feature Branch

```bash
git checkout -b feature/new-feature
```

## Commit Changes

```bash
git commit -m "Add new feature"
```

## Push Changes

```bash
git push origin feature/new-feature
```

---

# License

Refer to the repository license for licensing information.

---

# Repository

https://github.com/YENEALEM-FL/Movie-watch-review-FDD-proj
