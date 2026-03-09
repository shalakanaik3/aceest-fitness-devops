# ACEest Fitness & Gym - Automated Deployment Workflow

## 🚀 Project Overview
As a Junior DevOps Engineer, I have transitioned the ACEest Fitness logic from a local desktop application to a robust, containerized Web API. This solution ensures code integrity via automated testing and environment consistency through Docker.

## 🛠 Tech Stack
- **Framework:** Flask (Python)
- **Containerization:** Docker
- **CI/CD:** GitHub Actions & Jenkins
- **Testing:** Pytest
- **VCS:** Git/GitHub

## 📋 Phase-by-Phase Implementation

### 1. Development & Modularization
The core logic was migrated from Tkinter to a Flask-based REST API (`app.py`), enabling server-side execution suitable for cloud environments.

### 2. Unit Testing & Quality Gates
We integrated the **Pytest** framework. Every build must pass:
- `test_health_endpoint`: Ensures the service is live.
- `test_calorie_logic`: Validates the fitness calculation accuracy.

### 3. Containerization
The `Dockerfile` uses a multi-layer build approach to ensure the "write once, run anywhere" consistency, eliminating environmental drift.

### 4. CI/CD Integration
- **GitHub Actions:** Every `push` triggers a `.github/workflows/main.yml` pipeline that Lints the code, runs Unit Tests, and builds the Docker image.
- **Jenkins:** Acts as the secondary validation layer, performing clean builds in a controlled environment to ensure staging readiness.

## 🏃 Setup Instructions
1. **Local Run:** `pip install -r requirements.txt`
   `python app.py`
2. **Run Tests:**
   `pytest`
3. **Docker Deployment:**
   `docker build -t aceest-fitness .`
   `docker run -p 5000:5000 aceest-fitness`