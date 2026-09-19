# Minimal Planner (Streamlit + FastAPI + Postgres)

This scaffold provides a simple black-and-white planner with notes, schedule, and trackers using Streamlit for frontend, FastAPI for backend, and Postgres for storage.

Quick start (requires Docker & Docker Compose):

```bash
docker-compose up --build
```

- Frontend: http://localhost:8501
- Backend: http://localhost:8000
- Postgres: 5432

The backend currently uses an in-memory store for notes; we'll add SQLAlchemy models and migrations next.

# How to run the App locally
backend:  uvicorn app:app --reload --host 0.0.0.0 --port 8000
Frontend:  streamlit run streamlit_app.py