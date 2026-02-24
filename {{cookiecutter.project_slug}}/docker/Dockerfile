FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/home/django_user/.local/bin:${PATH}"

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    bash \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

SHELL ["/bin/bash", "-c"]

RUN adduser --disabled-password --gecos '' django_user \
    && mkdir -p app/static_cdn/{media_root,static_root} \
    && chown -R django_user:django_user /app

WORKDIR /app
USER django_user

COPY --chown=django_user:django_user requirements.txt .

RUN python -m pip install --upgrade pip \
 && python -m pip install -r requirements.txt gunicorn \
    --index-url https://mirror-pypi.codinto.ir/root/pypi/+simple/ \
    --trusted-host mirror-pypi.codinto.ir

COPY --chown=django_user:django_user . .

CMD [ \
    "gunicorn", "your_application.wsgi:application", \
     "--bind", "0.0.0.0:8000", \
     "--timeout", "120", \
     "--log-level", "info" \
    ]