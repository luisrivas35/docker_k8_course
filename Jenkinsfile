pipeline {
    agent any

    environment {
        DOCKER_HUB_REPO = 'luisrivas35/my-app'
        KUBE_NAMESPACE = 'test'
        KUBE_DEPLOYMENT_NAME = 'mypod.yaml'
        DOCKER_HUB_USERNAME = ''
        DOCKER_HUB_PASSWORD = ''
    }

    stages {
        stage('Cleanup') {
            steps {
                script {
                    // Remove all Docker containers and images
                    sh 'docker system prune -af'
                }
            }
        }

        stage('Dockerize Application') {
            steps {
                script {
                    // Build Docker image
                    sh 'docker build -t my-app .'
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    // Use Jenkins credentials for Docker Hub login
                    withCredentials([usernamePassword(credentialsId: 'docker_hub_creds', usernameVariable: 'DOCKER_HUB_USERNAME', passwordVariable: 'DOCKER_HUB_PASSWORD')]) {
                        // Ensure the Docker image is built with the correct tag
                        sh 'docker build -t my-app .'
                        sh "docker login -u ${DOCKER_HUB_USERNAME} -p ${DOCKER_HUB_PASSWORD}"
                        sh "docker push my-app:latest"
                    }
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                script {
                    sh "kubectl apply -n $KUBE_NAMESPACE -f $KUBE_DEPLOYMENT_NAME"
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully'
        }
        failure {
            echo 'Pipeline failed'
        }
    }
}
