pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = 'mlops-project'
        CONTAINER_NAME = 'mlops-container'
        DOCKER_HUB_CREDS = credentials('docker-hub-credentials') // Create these credentials in Jenkins
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Lint') {
            steps {
                sh 'pip install flake8'
                sh 'flake8 dags/ --count --select=E9,F63,F7,F82 --show-source --statistics'
            }
        }
        
        stage('Build Docker Image') {
            steps {
                sh 'docker build -t ${DOCKER_IMAGE}:${BUILD_NUMBER} .'
                sh 'docker tag ${DOCKER_IMAGE}:${BUILD_NUMBER} ${DOCKER_IMAGE}:latest'
            }
        }
        
        stage('Test Docker Image') {
            steps {
                // Run a simple test to make sure the image works
                sh 'docker run --rm ${DOCKER_IMAGE}:${BUILD_NUMBER} python -c "import airflow; import mlflow; print(\'Libraries imported successfully\')"'
            }
        }
        
        stage('Deploy') {
            steps {
                // Stop and remove existing container if it exists
                sh 'docker stop ${CONTAINER_NAME} || true'
                sh 'docker rm ${CONTAINER_NAME} || true'
                
                // Run the new container
                sh 'docker run -d -p 8080:8080 -p 5000:5000 --name ${CONTAINER_NAME} ${DOCKER_IMAGE}:${BUILD_NUMBER}'
            }
        }
        
        stage('Push to Registry') {
            steps {
                // Optional: Push to Docker Hub or private registry
                sh 'echo ${DOCKER_HUB_CREDS_PSW} | docker login -u ${DOCKER_HUB_CREDS_USR} --password-stdin'
                sh 'docker tag ${DOCKER_IMAGE}:${BUILD_NUMBER} ${DOCKER_HUB_CREDS_USR}/${DOCKER_IMAGE}:${BUILD_NUMBER}'
                sh 'docker tag ${DOCKER_IMAGE}:${BUILD_NUMBER} ${DOCKER_HUB_CREDS_USR}/${DOCKER_IMAGE}:latest'
                sh 'docker push ${DOCKER_HUB_CREDS_USR}/${DOCKER_IMAGE}:${BUILD_NUMBER}'
                sh 'docker push ${DOCKER_HUB_CREDS_USR}/${DOCKER_IMAGE}:latest'
            }
        }
    }
    
    post {
        always {
            // Clean up
            sh 'docker image prune -f'
        }
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed!'
            // Stop and remove container if it exists
            sh 'docker stop ${CONTAINER_NAME} || true'
            sh 'docker rm ${CONTAINER_NAME} || true'
        }
    }
}