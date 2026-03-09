# Use a slim version for smaller image size (DevOps Best Practice)
FROM python:3.9-slim

WORKDIR /app

# Install dependencies first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose Flask port
EXPOSE 5000

# Run the app
CMD ["python", "app.py"]