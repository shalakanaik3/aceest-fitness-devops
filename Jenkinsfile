pipeline {
    agent any
    environment {
        DOCKER_HUB_USER = "your_username" 
        SONAR_TOKEN = "your_saved_token"
    }
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Static Code Analysis') {
            steps {
                // This simulates the SonarQube check
                echo "Running SonarQube Analysis..."
            }
        }
        stage('Test') {
            steps {
                sh 'pip install -r requirements.txt'
                sh 'pytest'
            }
        }
        stage('Build & Push Docker') {
            steps {
                sh "docker build -t ${DOCKER_HUB_USER}/aceest-fitness-app:latest ."
                sh "docker push ${DOCKER_HUB_USER}/aceest-fitness-app:latest"
            }
        }
        stage('Deploy to Kubernetes') {
            steps {
                sh 'kubectl apply -f deployment.yaml'
                sh 'kubectl rollout status deployment/aceest-fitness'
            }
        }
    }
}