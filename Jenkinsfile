pipeline {
    agent {
        docker {
            image 'python:3.9.9-slim-bullseye'
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
        stage('Install Build Dependencies') {
            steps {
                sh '''
                    apt-get update && \
                    apt-get install -y \
                        build-essential \
                        gcc \
                        g++ \
                        python3-dev \
                        cmake \
                        libopenblas-dev \
                        pkg-config
                '''
            }
        }

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup') {
            steps {
                sh """
                    python -m venv ${VENV_PATH}
                    . ${VENV_PATH}/bin/activate
                    pip install --upgrade pip setuptools wheel
                    pip install --no-cache-dir -r requirements.txt
                """
            }
        }

        stage('Test') {
            steps {
                sh """
                    . ${VENV_PATH}/bin/activate
                    export PYTHONPATH=\$PYTHONPATH:\$WORKSPACE/src
                    pytest tests/ --cov=src --cov-report=xml
                """
            }
            post {
                always {
                    junit 'report.xml'
                    cobertura 'coverage.xml'
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
