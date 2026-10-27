# MLOps CI/CD and Monitoring Lab

This repository contains a small Flask application that estimates student
performance risk from study hours, attendance, and a previous score. It is a
transparent demonstration project for Git, GitHub Actions, Docker, Jenkins,
and application monitoring.

## Endpoints

- `/` - browser form
- `/health` - service health in JSON
- `/predict` - prediction API using `study_hours`, `attendance`, and
  `previous_score`
- `/metrics` - Prometheus-compatible counters

Example:

```text
http://127.0.0.1:5000/predict?study_hours=8&attendance=90&previous_score=80
```

## Run locally

Python and Flask must already be available:

```powershell
python app.py
```

Open `http://127.0.0.1:5000`.

## Test

```powershell
python -m unittest discover -s tests -v
```

## Docker

When Docker Desktop is running:

```powershell
docker build -t mlops-cicd .
docker run --rm -p 5000:5000 mlops-cicd
```

## CI/CD

GitHub Actions tests the application and builds the Docker image on pushes and
pull requests. `Jenkinsfile` provides equivalent Windows-oriented pipeline
stages for a Jenkins agent with Python and Docker already installed.

## Monitoring

The health endpoint supports availability checks. The metrics endpoint exposes
request, high-risk prediction, and validation-error counters for scraping by a
monitoring system.
