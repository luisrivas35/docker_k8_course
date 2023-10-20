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
                    // Remove only the Docker container with the same name as your app
                    sh "docker rm -f ${APP_NAME}"  // Remove the container with the name "my-app"
                }
            }
        }

        stage('Build and Push Docker Image') {
            steps {
                script {
                    def dockerImageExists = sh(script: "docker images -q ${DOCKER_IMAGE_NAME}:latest", returnStatus: true) == 0

                    if (!dockerImageExists) {
                        echo 'Docker image does not exist, building...'
                        sh "docker build -t ${DOCKER_IMAGE_NAME}:latest ."
                    } else {
                        echo 'Docker image already exists, updating...'
                    }

                    // Push the Docker image
                    sh "docker push ${DOCKER_IMAGE_NAME}:latest"
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
