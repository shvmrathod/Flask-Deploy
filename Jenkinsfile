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
                withCredentials([string(credentialsId: 'sonar_token', variable: 'SONAR_TOKEN')]) {
                    withSonarQubeEnv('MySonar') {
                        sh "/opt/homebrew/bin/sonar-scanner -Dsonar.login=$SONAR_TOKEN"
                    }
                }
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }
        
        stage('Debug Docker Path') {
            steps {
                sh 'which docker'
                sh 'which docker-credential-desktop'
                }
}
        stage('Verify PATH') {
            steps {
                sh 'echo $PATH'
                sh 'which docker-credential-desktop'
            }
}
        stage('Debug Docker Credential Helper') {
            steps {
                sh 'which docker-credential-desktop'
        }
}
        stage('Build Docker Image') {
            steps {
                sh '/usr/local/bin/docker build -t $DOCKER_IMAGE .'
                
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

    post {
        success {
            echo '✅ Pipeline completed successfully!'
        }
        failure {
            echo '❌ Pipeline failed. Please check the logs for details.'
        }
    }
}