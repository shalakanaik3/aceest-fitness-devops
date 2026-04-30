pipeline {
    agent any
    
    environment {
        DOCKER_HUB_USER = "shalaka3"
        SONAR_TOKEN = "sqp_bafb516dfd7062f1628aaf14e7cff9205b6d1814"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Static Code Analysis (SonarQube)') {
            steps {
                // This command assumes sonar-scanner is installed on the Jenkins agent
                sh "sonar-scanner -Dsonar.projectKey=aceest-fitness -Dsonar.sources=. -Dsonar.host.url=http://localhost:9000 -Dsonar.login=${SONAR_TOKEN}"
            }
        }

        stage('Unit Testing (Pytest)') {
            steps {
                sh 'pip install -r requirements.txt'
                sh 'pytest --junitxml=reports/result.xml'
            }
        }

        stage('Build & Push Docker Image') {
            steps {
                sh "docker build -t ${DOCKER_HUB_USER}/aceest-fitness:latest ."
                sh "docker push ${DOCKER_HUB_USER}/aceest-fitness:latest"
            }
        }

        stage('Deploy to Kubernetes (Minikube)') {
            steps {
                // Apply the rolling update manifest
                sh 'kubectl apply -f k8s/rolling-deployment.yaml'
                // Check if deployment is successful
                sh 'kubectl rollout status deployment/aceest-rolling'
            }
        }
    }
    
    post {
        always {
            junit 'reports/result.xml'
        }
    }
}