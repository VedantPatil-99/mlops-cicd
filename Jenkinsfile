pipeline {
    agent any

    stages {
        stage('Test') {
            steps {
                bat 'python -m unittest discover -s tests -v'
            }
        }
        stage('Build image') {
            steps {
                bat 'docker build -t mlops-cicd:latest .'
            }
        }
        stage('Smoke test') {
            steps {
                bat 'docker run --rm mlops-cicd:latest python -m unittest discover -s tests -v'
            }
        }
    }
}
