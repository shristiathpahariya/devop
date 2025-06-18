pipeline {
    agent any
    
    environment {
        DOCKER_HUB_CREDENTIALS = credentials('docker-hub-credentials')
        MODEL_VERSION = "${env.BUILD_ID}"
    }
    
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/your-repo/sentiment-analysis.git'
            }
        }
        
        stage('Test') {
            steps {
                sh 'python -m pytest tests/'
            }
        }
        
        stage('Retrain Model') {
            when {
                expression { 
                    // Run retraining weekly or when data changes
                    currentBuild.getBuildCauses()[0].toString().contains('TimerTrigger') || 
                    params.FORCE_RETRAIN == true 
                }
            }
            steps {
                sh 'python src/model_training.py'
                stash includes: 'models/**', name: 'models'
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    dockerImage = docker.build("your-dockerhub/sentiment-analysis:${env.MODEL_VERSION}")
                }
            }
        }
        
        stage('Push Docker Image') {
            steps {
                script {
                    docker.withRegistry('https://registry.hub.docker.com', 'docker-hub-credentials') {
                        dockerImage.push()
                        dockerImage.push('latest')
                    }
                }
            }
        }
        
        stage('Deploy') {
            steps {
                sshagent(['deployment-key']) {
                    sh """
                    ssh user@production-server "docker pull your-dockerhub/sentiment-analysis:${env.MODEL_VERSION}"
                    ssh user@production-server "docker-compose -f /path/to/docker-compose.yml up -d"
                    """
                }
            }
        }
    }
    
    post {
        always {
            cleanWs()
        }
        failure {
            slackSend channel: '#alerts', message: "Build ${currentBuild.result}: ${env.JOB_NAME} #${env.BUILD_NUMBER}"
        }
    }
}