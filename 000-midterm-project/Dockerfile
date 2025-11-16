# 1. Base image
FROM python:3.12-slim

# 2. Environment variables
ENV PYTHONDONTWRITEBYTECODE=1 
ENV PYTHONUNBUFFERED=1
ENV PIPENV_VENV_IN_PROJECT=1  

# 3. Working directory
WORKDIR /app

# 4. System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    gcc \
    g++ \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# 5. Install pipenv
RUN pip install --upgrade pip pipenv

# 6. Copy Pipfile and Pipfile.lock (Docker caching)
COPY Pipfile Pipfile.lock ./

# 7. Install dependencies into global site-packages
RUN pipenv install --deploy --ignore-pipfile --system

# 8. Copy the rest of the project
COPY . .

# 9. Create non-root user & switch
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# 10. Expose port
EXPOSE 9696

# 11. Run FastAPI
CMD ["uvicorn", "predict:app", "--host", "0.0.0.0", "--port", "9696"]
