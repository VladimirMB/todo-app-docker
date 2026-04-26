# Todo App Docker

A minimal full-stack todo application with a FastAPI backend and a plain HTML/CSS/JavaScript frontend.

## Run with Docker Compose

```bash
docker compose up --build
```

Then open your browser at `http://localhost:8000`.

## Project structure

- `/backend` - FastAPI backend code and SQLite database file
- `/frontend` - static HTML, CSS, and JavaScript frontend
- `Dockerfile` - container image for the FastAPI app
- `docker-compose.yml` - runs the API service on port 8000

## API endpoints

- `GET /tasks` - return all tasks
- `POST /tasks` - add a task with JSON body `{ "text": "..." }`
- `DELETE /tasks/{id}` - delete a task by id
