# Use official lightweight Python runtime
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Ensure standard output and error streams are unbuffered
ENV PYTHONUNBUFFERED=1

# Install dependencies first for efficient layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose application port (default 3000)
EXPOSE 3000

# Run application using Uvicorn on PORT
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-3000}"]
