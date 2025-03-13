pipeline {
    agent any

    environment {
        DOCKER_HUB_CREDENTIALS = credentials('docker-credentials') // Jenkins credential ID for Docker Hub
        AWS_ACCESS_KEY_ID = credentials('aws-account') // Jenkins credential ID for AWS access key
        AWS_SECRET_ACCESS_KEY = credentials('aws-account') // Jenkins credential ID for AWS secret key
        DOCKER_IMAGE = 'vomkeshpavan/calculator:latest'
        EKS_CLUSTER_NAME = 'MASTER'
        AWS_REGION = 'us-east-1'
    }

    stages {
        stage('Build and Test') {
          steps{
            script {
                pytest
                def testCount = sh(returnStdout: true, script: 'pytest --report-inventory').trim()
                if (testCount == '0') {
                    echo 'No tests executed, skipping subsequent stages'
                    currentBuild.result = 'SUCCESS'
                    return
                }
            }
        }

        stage('Build and Push Docker Image') {
            steps {
                script {
                    echo 'Building and pushing Docker image...'
                    sh "docker build -t ${DOCKER_IMAGE} ."
                    sh "echo ${DOCKER_HUB_CREDENTIALS_PSW} | docker login -u ${DOCKER_HUB_CREDENTIALS_USR} --password-stdin"
                    sh "docker push ${DOCKER_IMAGE}"
                }
            }
        }

        stage('Deploy to EKS') {
            steps {
                script {
                    echo 'Deploying to EKS...'
                    sh "aws configure set aws_access_key_id ${AWS_ACCESS_KEY_ID}"
                    sh "aws configure set aws_secret_access_key ${AWS_SECRET_ACCESS_KEY}"
                    sh "aws configure set region ${AWS_REGION}"
                    sh "aws eks --region ${AWS_REGION} update-kubeconfig --name ${EKS_CLUSTER_NAME}"
                    sh "kubectl apply -f deployment.yaml"
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline succeeded!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}
