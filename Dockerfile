# Use a slim version of Python 3.10
FROM python:3.10.11-slim

# Install system dependencies required for psycopg2
RUN apt-get update && apt-get install -y \
    libpq-dev gcc python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /Flashcard

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Set environment variables
ENV FLASK_APP=run.py
ENV FLASK_ENV=production

# Expose the application port
EXPOSE 5000

# Start the Flask application using Gunicorn
CMD ["sh", "-c", "flask db upgrade && gunicorn -w 4 -b 0.0.0.0:5000 run:app"]
