pipeline {
    agent any

    environment {
        DOCKER_HUB_REPO = 'luisrivas35'
        APP_NAME = 'my-app'
        DOCKER_IMAGE_NAME = "${DOCKER_HUB_REPO}/${APP_NAME}"
    }

    stages {
        stage('Cleanup') {
            steps {
                script {
                    // Remove the Docker container with the same name as your app
                    sh "docker rm -f ${APP_NAME}"  // Remove the container with the name "my-app"

                    // Remove the Docker image
                    sh "docker rmi -f ${DOCKER_IMAGE_NAME}:latest"
                }
            }
        }

        stage('Build and Push Docker Image') {
            steps {
                script {
                    def imageExists = sh(script: "docker images -q ${DOCKER_IMAGE_NAME}:latest", returnStatus: true) == 0

                    // Build the Docker image
                    sh "docker build -t ${DOCKER_IMAGE_NAME}:latest ."

                    // Push the Docker image
                    sh "docker push ${DOCKER_IMAGE_NAME}:latest"

                    // Remove any previous containers (if any)
                    sh "docker rm -f ${APP_NAME}"
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
