pipeline {
    agent any

    environment {
        DOCKER_HUB_REPO = 'luisrivas35/my-app'
        KUBE_NAMESPACE = 'test'
        KUBE_DEPLOYMENT_NAME = 'mypod.yaml'
    }

    stages {
        stage('Checkout Code') {
            steps {
                // Initialize workspace as a Git repository
                dir("${WORKSPACE}") {
                    sh 'git init'
                    sh "git remote add origin ${REPO_URL}"
                    sh "git fetch --tags --progress origin +refs/heads/*:refs/remotes/origin/*"
                    sh "git checkout -f -q FETCH_HEAD"
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
                    withCredentials([usernamePassword(credentialsId: '7fb69c42-a77e-4cc1-b490-7f183e4233d0', usernameVariable: 'DOCKER_HUB_USERNAME', passwordVariable: 'DOCKER_HUB_PASSWORD')]) {
                        sh "docker login -u ${DOCKER_HUB_USERNAME} -p ${DOCKER_HUB_PASSWORD}"
                    }

                    // Push Docker image to Docker Hub
                    sh "docker push $DOCKER_HUB_REPO:latest"
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                script {
                    // Apply Kubernetes deployment YAML file
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
