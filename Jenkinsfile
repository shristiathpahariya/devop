pipeline {
    agent {
        docker {
            image 'shedocks/jenkins-python-agent'
            registryCredentialsId 'shristi'
            args '-u root --platform linux/amd64'
        }
    }

    environment {
        REPO_URL = 'https://github.com/shristiathpahariya/devop.git'
        BRANCH = 'main'
        DOCKER_IMAGE = 'your-dockerhub/your-repo'
        DOCKER_TAG = "${env.BUILD_NUMBER}"
        VENV_PATH = "${WORKSPACE}/venv"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm  // Simplified checkout
            }
        }

        stage('Setup') {
            steps {
                sh """
                    python -m venv ${VENV_PATH}
                    . ${VENV_PATH}/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                """
            }
        }

        stage('Test') {
            steps {
                sh """
                    . ${VENV_PATH}/bin/activate
                    pytest tests/ --cov=src --cov-report=xml
                """
            }
            post {
                always {
                    junit '**/test-results/*.xml'
                    cobertura '**/coverage.xml'
                }
            }
        }

        stage('Build Docker Image') {
            when {
                expression { fileExists('Dockerfile') }
            }
            steps {
                script {
                    docker.build("${DOCKER_IMAGE}:${DOCKER_TAG}")
                }
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}
