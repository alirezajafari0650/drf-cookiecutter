# Base python image
FROM python:3.11-slim                    # Official lightweight Python base image | Default: latest Python 3.x slim

# Environment Variables
ENV PYTHONDONTWRITEBYTECODE=1            # Prevents Python from writing .pyc files | Default: 0 (writes .pyc)
ENV PYTHONUNBUFFERED=1                   # Forces stdout/stderr to be unbuffered for real-time logging | Default: 0 (buffered)
ENV PATH="/usr/local/bin:$PATH"          # Ensures global binaries are found | Default: auto-set by base image

# Set working directory
WORKDIR /app                             # All following commands run inside /app | Default: /

# System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libmagic1                            # Required for file validation (used by python-magic / DRF validators) \
 && rm -rf /var/lib/apt/lists/*          # Clean apt cache to reduce image size

# Create directories for static & media files
RUN mkdir -p /vol/web/static /vol/web/media   # Persistent directories for static/media files

# Install Python dependencies
COPY requirements.txt .                   # Copy dependency list first (for Docker layer caching)
RUN pip install --upgrade pip             # Upgrade pip for compatibility | Default: comes preinstalled
RUN pip install --no-cache-dir -r requirements.txt  # Install main dependencies | --no-cache-dir reduces image size
RUN pip install --no-cache-dir celery redis gunicorn # Install common production tools (Celery, Redis, Gunicorn)

# Copy project files
COPY . .                                  # Copy Django project files into the container

# Optional: Collect static files
# RUN python manage.py collectstatic --noinput  # Collects static files for production | Default: skipped

# Permissions (Optional but recommended)
RUN adduser --disabled-password --no-create-home django_user  # Create non-root user
RUN chown -R django_user:django_user /app /vol                # Give permissions to app folders
USER django_user                                              # Run container as non-root for security

# Gunicorn command
CMD [ \
  "gunicorn", "your_project.wsgi:application", \
  "--workers", "17", \                             # Adjust: 2 × cores + 1 | Default: 2 × cores + 1
  "--worker-class", "gthread", \                   # Worker type: gthread for I/O, sync default | Default: sync
  "--threads", "2", \                              # Threads per worker | Default: 1
  "--preload", \                                   # Preload app before forking | Default: off
  "--pid", "/tmp/gunicorn.pid", \                  # PID file for process management | Default: none
  "--timeout", "120", \                            # Max seconds per request | Default: 30
  "--graceful-timeout", "30", \                    # Graceful shutdown wait | Default: 30
  "--keep-alive", "5", \                           # Keep connections alive (seconds) | Default: 2
  "--max-requests", "1000", \                      # Restart worker after N requests | Default: 0
  "--max-requests-jitter", "50", \                 # Randomize restarts | Default: 0
  "--access-logfile", "/dev/stdout", \             # Send access logs to stdout | Default: stdout
  "--error-logfile", "/dev/stderr", \              # Send error logs to stderr | Default: stderr
  "--log-level", "info", \                         # Logging level | Default: info
  "--capture-output", \                            # Capture stdout/stderr | Default: off
  "--bind", "0.0.0.0:8000"                         # Bind to all interfaces for Docker networking | Default: 127.0.0.1:8000
]
# Note: Using 0.0.0.0 inside Docker is required (Unix socket is for host-based Nginx setups)