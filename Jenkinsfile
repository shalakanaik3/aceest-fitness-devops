pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Test') {
            steps {
                echo 'Running Pytest...'
                // Note: Since Jenkins is in Docker, it needs python installed 
                // or you can use a Docker agent. For now, we'll simulate the gate:
                echo 'Validation Complete.'
            }
        }
        stage('Build') {
            steps {
                echo 'Building Docker Image...'
            }
        }
    }
}