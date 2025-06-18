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
        stage('Install Build Dependencies') {
            steps {
                sh '''
                    apk-get update && \
                    apk-get install -y \
                        build-essential \
                        gcc \
                        g++ \
                        python3-dev \
                        cmake \
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
            apk update && apk add build-base python3-dev
            python -m venv ${VENV_PATH}
            . ${VENV_PATH}/bin/activate
            pip install --upgrade pip
            pip install --prefer-binary -r requirements.txt
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
