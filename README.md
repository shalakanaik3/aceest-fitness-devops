# ACEest Fitness & Gym - Automated Deployment Workflow

## Overview
This repository contains the refactored Flask web application for ACEest Fitness & Gym. 
The project demonstrates a full CI/CD lifecycle, transitioning from a Python-based 
logic core to a containerized, cloud-validated deployment.

## Tech Stack
* **Framework:** Flask (Python 3.9)
* **Testing:** Pytest
* **Containerization:** Docker
* **CI/CD:** GitHub Actions & Jenkins

## Local Setup Instructions
1. **Clone the repo:** `git clone <your-repo-link>`
2. **Install dependencies:** `pip install -r requirements.txt`
3. **Run application:** `python app.py`
4. **Access API:** Navigate to `http://localhost:5000/health`

## Manual Testing
To execute the unit test suite manually, run:
```bash
pytest test_app.py