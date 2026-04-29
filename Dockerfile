# Use a slim version for smaller image size
FROM python:3.9-slim

# Create a non-privileged user for security
RUN adduser --disabled-password fitnessuser

WORKDIR /app

# Install dependencies first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code and set ownership to our new user
COPY --chown=fitnessuser:fitnessuser . .

# Switch to the non-root user
USER fitnessuser

# Expose Flask port
EXPOSE 5000

# Run the app
CMD ["python", "app.py"]