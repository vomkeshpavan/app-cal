pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'vomkeshpavan/calculator:latest'
        EKS_CLUSTER_NAME = 'MASTER'
        AWS_REGION = 'us-east-1'
    }

    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    echo 'Building Docker image...'
                    sh 'docker build -t ${DOCKER_IMAGE} .'
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    echo 'Pushing Docker image to Docker Hub...'
                    withCredentials([usernamePassword(credentialsId: 'docker-credentials', passwordVariable: 'DOCKER_HUB_CREDENTIALS_PSW', usernameVariable: 'DOCKER_HUB_CREDENTIALS_USR')]) {
                        sh "echo ${DOCKER_HUB_CREDENTIALS_PSW} | docker login -u ${DOCKER_HUB_CREDENTIALS_USR} --password-stdin"
                    }
                    sh "docker push ${DOCKER_IMAGE}"
                }
            }
        }

        stage('Deploy to EKS') {
            steps {
                script {
                    echo 'Deploying to EKS...'
                    withCredentials([usernamePassword(credentialsId: 'aws-account', passwordVariable: 'AWS_SECRET_ACCESS_KEY', usernameVariable: 'AWS_ACCESS_KEY_ID')]) {
                        sh "aws configure set aws_access_key_id ${AWS_ACCESS_KEY_ID}"
                        sh "aws configure set aws_secret_access_key ${AWS_SECRET_ACCESS_KEY}"
                    }
                    sh "aws configure set region ${AWS_REGION}"
                    sh "aws eks --region ${AWS_REGION} update-kubeconfig --name ${EKS_CLUSTER_NAME}"
                    sh "kubectl apply -f deployment.yaml"
                }
            }
        }

        stage('Post') {
            steps {
                script {
                    if (currentBuild.result == 'SUCCESS') {
                        echo 'Pipeline succeeded!'
                    } else {
                        echo 'Pipeline failed!'
                    }
                }
            }
        }
    }
}
