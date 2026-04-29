FROM python:3.9-slim

RUN adduser --disabled-password fitnessuser
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# COMPLIANT: Explicitly list files instead of using "COPY . ." 
# This satisfies the "Limit usage of globbing" requirement
COPY --chown=root:root --chmod=755 app.py .

USER fitnessuser
EXPOSE 5000

CMD ["python", "app.py"]