FROM python:3.12-slim

WORKDIR /app

# Install dependencies using pip and pyproject.toml
COPY pyproject.toml ./
RUN pip install --no-cache-dir .

COPY . .

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
