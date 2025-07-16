FROM python:3.12.6-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=core.settings

# Install netcat for health checks
RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

# Set non-root user for security
RUN addgroup --system app && adduser --system --group app

WORKDIR /code

# Install dependencies first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Create directories for static files and media
RUN mkdir -p /code/staticfiles /code/media

# Set proper permissions
RUN chown -R app:app /code

# Copy entrypoint script and set permissions
COPY docker-entrypoint.sh /code/docker-entrypoint.sh
RUN chmod +x /code/docker-entrypoint.sh
USER app

ENTRYPOINT ["/code/docker-entrypoint.sh"]

# Run gunicorn by default
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
