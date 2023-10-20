pipeline {
    agent any

    environment {
        DOCKER_HUB_REPO = 'luisrivas35'
        APP_NAME = 'my-app'
        KUBE_NAMESPACE = 'test'
        KUBE_DEPLOYMENT_NAME = 'mypod.yaml'
        DOCKER_IMAGE_NAME = "${DOCKER_HUB_REPO}/${APP_NAME}"
    }

    stages {
        stage('Cleanup') {
            steps {
                script {
                    sh 'docker container prune -f'
                }
            }
        }

        stage('Check if Docker image exists') {
            steps {
                script {
                    def imageExists = sh(script: "docker images -q ${DOCKER_IMAGE_NAME}:latest", returnStatus: true) == 0

                    if (imageExists) {
                        echo 'Docker image already exists'
                    } else {
                        echo 'Docker image does not exist, building...'
                        sh 'docker build -t my-app .'
                    }
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'docker_hub_creds', usernameVariable: 'DOCKER_HUB_USERNAME', passwordVariable: 'DOCKER_HUB_PASSWORD')]) {
                        sh "docker login -u ${DOCKER_HUB_USERNAME} -p ${DOCKER_HUB_PASSWORD}"
                        sh "docker tag my-app:latest ${DOCKER_IMAGE_NAME}:latest"
                        sh "docker push ${DOCKER_IMAGE_NAME}:latest"
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
