pipeline {
    agent any

    environment {
        SCANNER_HOME = tool 'sonar-scanner'
        IMAGE_NAME = "tanle92/ou-library"
        CONTAINER_NAME = "ou-library-container"
    }
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/tanle9t2/OU-Library.git'
            }
        }
        stage("Sonarqube Check") {
            steps {
                withSonarQubeEnv('sonar-server') {
                    sh """
                        ${SCANNER_HOME}/bin/sonar-scanner \
                        -Dsonar.projectKey=ou-library-flask \
                        -Dsonar.projectName=OU-Library-Flask \
                        -Dsonar.sources=. \
                        -Dsonar.language=py \
                        -Dsonar.python.version=3 \
                        -Dsonar.sourceEncoding=UTF-8
                    """
                }
            }
        }

        stage('Set Commit-Based Tag') {
            steps {
                script {
                    def commit = sh(script: 'git rev-parse --short HEAD', returnStdout: true).trim()
                    env.IMAGE_TAG = "main-${commit}"
                }
            }
        }
        //test
        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
            }
        }

        stage('Push to Docker Hub') {

            steps {
                withDockerRegistry(credentialsId: 'dockerhub', url: 'https://index.docker.io/v1/') {
                    sh "docker push ${IMAGE_NAME}:${IMAGE_TAG}"
                }
            }
        }

        stage('Run Docker Container') {
            steps {
                sh """
                    docker rm -f ${CONTAINER_NAME} || true
                """
                sh """
                    docker run -d \
                          --name $CONTAINER_NAME \
                          --add-host=host.docker.internal:host-gateway \
                          -p 5000:5000 \
                          -e DB_URL=$DB_URL \
                          -e DB_PASSWORD=$DB_PASSWORD \
                          -e SECRET_KEY=$SECRET_KEY \\
                          -v /mnt/d/code/QLDA/firebase.json:/app/firebase.json \
                          -e FIREBASE_PATH=$FIREBASE_PATH \
                          -e CLIENT_ID=$CLIENT_ID \
                          -e CLIENT_SECRET=$CLIENT_SECRET \
                          ${IMAGE_NAME}:${IMAGE_TAG}
                """
            }
        }
    }

    post {
        always {
            echo 'Cleaning up...'
        }
        success {
            echo '✅ Deployed Flask app successfully!'
        }
        failure {
            echo '❌ Deployment failed!'
        }
    }
}