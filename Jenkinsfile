pipeline {
    agent {
        docker {
            image 'shedocks/jenkins-python-agent'
            registryCredentialsId 'shristi'
            args '-u root --platform linux/amd64'  # Force AMD64 architecture
        }
    }

    environment {
        VENV_PATH = "${WORKSPACE}/venv"
    }

    stages {
        stage('Install Build Tools') {
            steps {
                sh '''
                    apt-get update && apt-get install -y \
                    build-essential \
                    gcc \
                    g++ \
                    python3-dev
                '''
            }
        }

        stage('Setup') {
            steps {
                sh """
                    python -m venv ${VENV_PATH}
                    . ${VENV_PATH}/bin/activate
                    pip install --upgrade pip setuptools wheel
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
    }

    post {
        always {
            cleanWs()
        }
    }
}
