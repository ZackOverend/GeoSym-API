# GeoSym API

Few-shot geological symbol classifier using prototypical networks on tiled USGS raster maps. Outputs confidence-scored GeoJSON served via a FastAPI inference pipeline.

## Requirements

- Python 3.11+
- PostgreSQL 18
- Redis

## Setup

### 1. Clone and install dependencies

```bash
git clone https://github.com/ZackOverend/GeoSym-API.git
cd GeoSym-API
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
```

Edit `.env` with your database credentials.

### 3. Set up the database

Run these once on a new machine to create the Postgres user and database:

```bash
psql postgres -c "CREATE USER geosym WITH PASSWORD 'your_password';"
psql postgres -c "CREATE DATABASE geosym OWNER geosym;"
```

Then update `DATABASE_URL` in your `.env` with the password you chose.

### 4. Run migrations

```bash
alembic upgrade head
```

### 5. Start the server

```bash
uvicorn app.main:app --reload
```

API docs available at [http://localhost:8000/docs](http://localhost:8000/docs).

### 6. Start the ARQ worker (separate terminal)

```bash
arq app.worker.WorkerSettings
```

## Database migrations

```bash
# Generate a new migration after changing models
alembic revision --autogenerate -m "description"

# Apply all pending migrations
alembic upgrade head

# Roll back one migration
alembic downgrade -1
```

## Running tests

```bash
pytest
```
