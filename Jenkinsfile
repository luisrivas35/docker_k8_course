pipeline {
    agent any

    environment {
        DOCKER_HUB_REPO = 'luisrivas35'
        APP_NAME = 'my-app'
        KUBE_NAMESPACE = 'test'
        DOCKER_IMAGE_NAME = "${DOCKER_HUB_REPO}/${APP_NAME}"
        KUBE_DEPLOYMENT_FILE = 'mypod.yaml'  // Specify the full path to the deployment file
    }

    stages {
        stage('Install kubectl') {
            steps {
                script {
                    // Check if kubectl is installed
                    def kubectlInstalled = sh(script: 'kubectl version --client --short', returnStatus: true) == 0

                    if (!kubectlInstalled) {
                        // Install kubectl if it's not already installed
                        echo 'kubectl is not installed. Installing...'
                        sh 'curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"'
                        sh 'chmod +x kubectl'
                        sh "mv kubectl /usr/local/bin/"
                        echo 'kubectl installed successfully.'
                    } else {
                        echo 'kubectl is already installed.'
                    }
                }
            }
        }

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
                    def imageExists = sh(script: "docker images -q ${DOCKER_IMAGE_NAME}:latest", returnStatus: true) == 0

                    // Build the Docker image
                    sh "docker build -t ${DOCKER_IMAGE_NAME}:latest ."

                    // Push the Docker image
                    sh "docker push ${DOCKER_IMAGE_NAME}:latest"

                    // Remove any previous containers (if any)
                    sh "docker rm -f ${APP_NAME}" 

                    // Start the Docker container
                    sh "docker run -d --name ${APP_NAME} ${DOCKER_IMAGE_NAME}:latest"
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                script {
                    // Ensure kubectl is configured with the correct context and credentials.
                    // kubectl should be installed and configured on the Jenkins server.

                    // Apply the Kubernetes deployment to the specified namespace
                    sh "kubectl apply -n $KUBE_NAMESPACE -f $KUBE_DEPLOYMENT_FILE"
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
