pipeline {
    agent {
        kubernetes {
            // Specify the label and image for the agent pod
            label 'my-jenkins-agent'
            defaultContainer 'jnlp'
            yaml """
apiVersion: v1
kind: Pod
metadata:
  labels:
    some-label: some-label-value
  spec:
    serviceAccountName: jenkins-sa  # Use the Jenkins service account
    containers:
    - name: jnlp
      image: 'jenkins/inbound-agent:4.3-4'
      resources:
        limits:
          memory: '512Mi'
          cpu: '500m'
        requests:
          memory: '256Mi'
          cpu: '250m'
"""
        }
    }

    environment {
        DOCKER_HUB_REPO = 'luisrivas35'
        APP_NAME = 'my-app'
        KUBE_NAMESPACE = 'test'
        DOCKER_IMAGE_NAME = "${DOCKER_HUB_REPO}/${APP_NAME}"
        KUBE_DEPLOYMENT_FILE = 'mypod.yaml'
    }

    stages {
        stage('Install kubectl') {
            steps {
                script {
                    def kubectlInstalled = sh(script: 'kubectl version --client --short', returnStatus: true) == 0

                    if (!kubectlInstalled) {
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

        stage('Set kubectl Context') {
            steps {
                script {
                    sh 'kubectl config use-context docker-desktop'
                }
            }
        }

        stage('Cleanup') {
            steps {
                script {
                    sh "docker rm -f ${APP_NAME}"
                }
            }
        }

        stage('Build and Push Docker Image') {
            steps {
                script {
                    def imageExists = sh(script: "docker images -q ${DOCKER_IMAGE_NAME}:latest", returnStatus: true) == 0

                    sh "docker build -t ${DOCKER_IMAGE_NAME}:latest ."
                    sh "docker push ${DOCKER_IMAGE_NAME}:latest"
                    sh "docker rm -f ${APP_NAME}" 
                    sh "docker run -d --name ${APP_NAME} ${DOCKER_IMAGE_NAME}:latest"
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                script {
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
