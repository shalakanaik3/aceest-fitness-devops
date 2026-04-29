FROM python:3.9-slim

RUN adduser --disabled-password fitnessuser
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# COMPLIANT: Root ownership ensures app files are read-only for the process
COPY --chown=root:root --chmod=755 . .

USER fitnessuser
EXPOSE 5000

CMD ["python", "app.py"]