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

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $DOCKER_IMAGE .'
            }
        }

        stage('Scan with Trivy') {
            steps {
                sh '''
                    if ! command -v trivy &> /dev/null; then
                        echo "Trivy not found, installing..."
                        brew install aquasecurity/trivy/trivy
                    fi
                    trivy image --severity CRITICAL,HIGH $DOCKER_IMAGE
                '''
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withDockerRegistry([credentialsId: 'docker-hub-credentials', url: '']) {
                    sh 'docker push $DOCKER_IMAGE'
                }
            }
        }

        stage('Deploy to Minikube') {
            steps {
                sh '''
                    kubectl config use-context minikube
                    kubectl apply -f deployment.yaml
                    kubectl apply -f service.yaml
                '''
            }
        }

        stage('Apply Ingress') {
            steps {
                sh 'kubectl apply -f ingress.yaml'
            }
        }
    }

    post {
        success {
            echo '✅ Pipeline completed and deployed to Minikube!'
        }
        failure {
            echo '❌ Pipeline failed. Check the logs.'
        }
    }
}