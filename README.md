# ACEest Fitness & Gym - Automated Deployment Workflow

## 📌 Project Overview
ACEest Fitness & Gym is a rapidly scaling startup requiring a modern, robust DevOps architecture. This project represents the transition from legacy desktop scripts to a high-availability, containerized **Flask Web API**. The solution implements a rigorous CI/CD lifecycle ensuring code integrity, environmental consistency, and rapid delivery.

## 🏗️ Architecture & Core Assignment Phases
The application has been modularized to support a professional DevOps lifecycle:

1.  **Application Refactoring:** Logic from legacy Tkinter scripts was refactored into a Flask REST API to allow for headless testing and containerized deployment.
2.  **Version Control (VCS):** Implemented a structured Git strategy with descriptive commits and environment-specific ignoring (via `.gitignore`).
3.  **Unit Testing:** Integrated **Pytest** to validate internal service logic and database integrity before the build stage.
4.  **Containerization:** Encapsulated the environment using **Docker** to eliminate "it works on my machine" syndrome.
5.  **Quality Gates:** Implemented dual-layer validation using **Jenkins** (Internal Build) and **GitHub Actions** (Cloud CI).

---

## 🚀 Local Setup & Execution
To run this project on your local machine:

1. **Clone the Repository:**
git clone <your-repository-url>
cd aceest-devops

2. **Install Dependencies:**
pip install -r requirements.txt

3. **Initialize & Run:**
python app.py

*The API will be live at `http://localhost:5000*`

---

## 🧪 Testing & Validation

To manually execute the comprehensive Pytest suite:

pytest test_app.py

*These tests validate the `/health` endpoint, database retrieval, and POST request logic.*

---

## ⚙️ CI/CD Pipeline Logic

### 1. GitHub Actions (Cloud Validation)

The `.github/workflows/main.yml` pipeline is triggered on every push. It performs:

* **Lint/Build:** Dependency installation and syntax check.
* **Automated Testing:** Execution of Pytest within the GitHub Ubuntu runner.
* **Docker Assembly:** Verification of the Dockerfile build process.

### 2. Jenkins (Internal Quality Gate)

Jenkins serves as the primary **BUILD environment** and secondary validation layer:

* **Pull-based integration:** Jenkins pulls the latest code from GitHub.
* **Jenkinsfile Pipeline:** Executes a scripted pipeline that mirrors the production build environment to ensure the code integrates correctly on local/private infrastructure.

---

## 🐳 Docker Production Build

To build and run the production-ready container:

docker build -t aceest-fitness:1.0 .
docker run -p 5000:5000 aceest-fitness:1.0


## 📊 Evaluation Benchmarks

* **Application Integrity:** Successfully transitioned to a Flask-based service model.
* **Docker Efficiency:** Optimized image using `python:3.9-slim` to reduce attack surface and build time.
* **VCS Maturity:** Meaningful commit history and strict exclusion of binaries/local databases.
* **Pipeline Reliability:** Verified "Green" status on both GitHub Actions and Jenkins Stage Views.

---

**Prepared by:** Shalaka N

---