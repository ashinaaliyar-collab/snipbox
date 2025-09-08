# snipbox
SnipBox (Short Notes Saving App)  
SnipBox is a backend service for a note-saving application that allows users to save and organize short text snippets. The application is built using Django Rest Framework (DRF) and provides APIs for creating, retrieving, and managing snippets with tagging functionality.


## Features

- User registration and login with mobile number and password
- JWT authentication (access and refresh tokens stored in HTTP-only cookies)
- CRUD APIs for code snippets
- Tag management with unique tag titles
- Snippet filtering by tag and user
- Overview API with snippet count and detail links
- All date-times returned in IST (Indian Standard Time)
- Secure endpoints (except login and registration)

## Tech Stack

- Python 3.12+
- Django 5.x
- Django REST Framework
- PostgreSQL (recommended)
- JWT (PyJWT)
- Docker/Docker Compose (optional)

## Setup

1. **Clone the repository**
    ```bash
    git clone git@github.com:ashinaaliyar-collab/snipbox.git
    cd snipbox
    ```

2. **Install dependencies**
    ```bash
    pip install -r app/requirements.txt
    ```

3. **Configure environment**
    - Set your `SECRET_KEY` and database settings in `app/settings.py`.

4. **Apply migrations**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5. **Run the server**
    ```bash
    python manage.py runserver
    ```
    
## Setup with Docker

1. **Build the images**
   ```bash
   docker-compose build
2. **Run the containers**
    ``` bash
    docker-compose up
    ```
    -Django app will be available at: http://localhost:8000
    -PostgreSQL will run inside the container and be available to the app.
3. **Apply migrations (inside container)**
    ```bash
    docker compose exec {container_id} bash
    python3 manage.py makemigrations
    python3 manage.py migrate
    ```
4. **for docker logs**
    ```bash
    docker-compose logs -f

    

## API Endpoints

| Endpoint                | Method | Description                                 |
|-------------------------|--------|---------------------------------------------|
| `/user/create/`         | POST   | Register a new user                         |
| `/user/login/`          | POST   | Login and receive JWT cookies               |
| `/user/refresh/`        | POST   | Refresh access and refresh tokens           |
| `/user/logout/`         | POST   | Logout and clear tokens                     |
| `/snippet/create/`      |  POST   | Create a new snippet                        |
| `/snippet/detail/<id>/` | GET    | Get snippet details                         |
| `/snippet/update/<id>/` | PUT    | Update a snippet                            |
| `/snippet/delete/<id>/` | DELETE | Delete a snippet                            |
| `/snippet/list/`        | GET    | List all snippets for the user              |
| `/snippet/tags/`        | GET    | List all tags                               |
| `/snippet/tags/<id>/`   | GET    | List snippets for a specific tag            |
| `/snippet/overview/`    | GET    | Overview: total count and snippet links     |

## Authentication

- JWT tokens are set as HTTP-only cookies (`access_token`, `refresh_token`).
- Use `credentials: 'include'` (fetch) or `withCredentials: true` in your frontend.
- Most endpoints require authentication except login and registration.

## Development

- Follow PEP8 for code formatting.
- Use the provided mixins for consistent API responses.
- All date-times are returned in IST.

## License

MIT License

---

**Happy
