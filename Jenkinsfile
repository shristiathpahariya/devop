pipeline {
    agent any

    // Environment variables
    environment {
        // Repository configuration
        REPO_URL = 'https://github.com/shristiathpahariya/devops.git'
        BRANCH = 'main'
        
        // Docker configuration (if applicable)
        DOCKER_IMAGE = 'your-dockerhub/your-repo'
        DOCKER_TAG = "${env.BUILD_NUMBER}"
    }

    stages {
        // Stage 1: Checkout with GitHub PAT
        stage('Checkout') {
            steps {
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: "${BRANCH}"]],
                    extensions: [
                        [$class: 'CleanBeforeCheckout'],
                        [$class: 'CloneOption', depth: 1, timeout: 10]
                    ],
                    userRemoteConfigs: [[
                        url: "${REPO_URL}",
                        credentialsId: 'github-pat' // Your PAT credentials ID
                    ]]
                ])
            }
        }

        // Stage 2: Install dependencies
        stage('Setup') {
            steps {
                sh '''
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        // Stage 3: Run tests
        stage('Test') {
            steps {
                sh 'pytest tests/ --cov=src --cov-report=xml'
            }
            post {
                always {
                    junit '**/test-results/*.xml'  // Test reports
                    cobertura coberturaReportFile: '**/coverage.xml'  // Coverage reports
                }
            }
        }

        // Stage 4: Build Docker image (optional)
        stage('Build Docker Image') {
            when {
                expression { 
                    fileExists('Dockerfile') 
                }
            }
            steps {
                script {
                    docker.build("${DOCKER_IMAGE}:${DOCKER_TAG}")
                }
            }
        }

        // Stage 5: Deploy (example)
        stage('Deploy') {
            when {
                branch 'main'
            }
            steps {
                echo "Deploying to production..."
                // Add your deployment steps here
            }
        }
    }

    post {
        always {
            cleanWs()  // Clean workspace
        }
        success {
            slackSend channel: '#builds', 
                     message: "SUCCESS: Job ${env.JOB_NAME} #${env.BUILD_NUMBER}"
        }
        failure {
            slackSend channel: '#alerts', 
                     message: "FAILED: Job ${env.JOB_NAME} #${env.BUILD_NUMBER}"
        }
    }
}
