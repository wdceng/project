# syntax=docker/dockerfile:1

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/go/dockerfile-reference/

# Want to help us make this template better? Share your feedback here: https://forms.gle/ybq9Krt8jtBL3iCk7

ARG PYTHON_VERSION=3.13.3
FROM python:${PYTHON_VERSION}-slim AS base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

WORKDIR /

# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/go/dockerfile-user-best-practices/
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
# Leverage a bind mount to requirements.txt to avoid having to copy them into
# into this layer.
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=app/requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt

# Copy the source code into the container.
COPY . .

# Ensure the non-root user owns all application files to allow safe read/write access at runtime
RUN chown -R appuser /app

# Drop privileges by switching to the non-root user for improved container security
USER appuser

# Expose the port that the application listens on.
EXPOSE 5050

# Run the application with gunicorn.
## Added "--chdir", "/app" because of /app folder
CMD ["gunicorn", "--chdir", "/app", "--bind", "0.0.0.0:5050", "app:app", "--timeout", "120"]

## If the Flask app is inside the root folder but I don't want to mix Docker and app files
# CMD ["gunicorn", "--bind", "0.0.0.0:5050", "app:app", "--timeout 120"]

# Run the application with flask run.
# CMD ["flask", "run", "--host=0.0.0.0", "--port=5050"]

## Minimum Dockerfile requirements, above created by CLI: docker init
# FROM python:3.13.3-slim

# WORKDIR /

# COPY app/requirements.txt .
# RUN pip install --no-cache-dir -r /app/requirements.txt

# COPY . .

# CMD ["gunicorn", "--chdir", "/app", "--bind", "0.0.0.0:5050", "app:app", "--timeout", "120"]
