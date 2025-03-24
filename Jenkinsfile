pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'shvmrathod/flask-app:latest'
    }

    stages {
        stage('Clone Repository') {
            steps {
                git credentialsId: 'Shivam', branch: 'main', url: 'https://github.com/shvmrathod/Flask-Deploy.git'
            }
        }

        stage('SonarQube Scan') {
            steps {
                withSonarQubeEnv('MySonar') {
                    sh 'sonar-scanner'
                }
            }
        }

        stage('Install Dependencies') {
            steps {
                script {
                    docker.image('python:3.10').inside {
                        sh 'pip install --upgrade pip'
                        sh 'pip install -r requirements.txt'
                    }
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.image('docker:latest').inside('--privileged -v /var/run/docker.sock:/var/run/docker.sock') {
                        sh 'docker build -t $DOCKER_IMAGE .'
                    }
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withDockerRegistry([credentialsId: 'docker-hub-credentials', url: '']) {
                    sh 'docker push $DOCKER_IMAGE'
                }
            }
        }
    }
}