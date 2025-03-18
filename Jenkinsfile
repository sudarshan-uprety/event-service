pipeline {
    agent any

    environment {
        PROD_ENV = 'ES_PROD_ENV'
        UAT_ENV = 'ES_UAT_ENV'
        DEV_ENV = 'ES_DEV_ENV'
        ECOM_PATH = '/home/ubuntu/sudarshan/microservices/event-consumer'
    }

    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Create .env File') {
            steps {
                script {
                    def envFileCredentialId = ""
                    
                    if (env.BRANCH_NAME == 'prod') {
                        envFileCredentialId = env.PROD_ENV
                    } else if (env.BRANCH_NAME == 'uat') {
                        envFileCredentialId = env.UAT_ENV
                    } else if (env.BRANCH_NAME == 'dev') {
                        envFileCredentialId = env.DEV_ENV
                    } else {
                        error "This branch does not have corresponding environment variables"
                    }

                    echo "Selected env file credential: ${envFileCredentialId}"

                    withCredentials([file(credentialsId: envFileCredentialId, variable: 'ENV_FILE')]) {
                        sh "ls -l \$ENV_FILE"
                        
                        sh '''
                            # Enable command tracing for debugging
                            set -x
                            echo "Attempting to copy the env file..."
                            cp "$ENV_FILE" .env
                            echo "Successfully copied the env file."
                        '''
                    }
                }
            }
        }

        stage('Sync Deployments with rsync') {
            steps {
                script {
                    withCredentials([ 
                        string(credentialsId: 'HOST_IP', variable: 'SERVER_HOST'),
                        string(credentialsId: 'SERVER_USER', variable: 'SERVER_USER'),
                        file(credentialsId: 'SERVER_KEY', variable: 'SSH_KEY_PATH'),
                        string(credentialsId: 'SERVER_PORT', variable: 'SSH_PORT')
                    ]) {
                        sh """
                                scp -i \$SSH_KEY_PATH -P \$SSH_PORT -r -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null ./ \${SERVER_USER}@\${SERVER_HOST}:${env.ECOM_PATH}/${env.BRANCH_NAME}
                        """
                    }
                }
            }
        }

        stage('Start Docker Containers') {
            steps {
                script {
                    def composeUpCommand = ''
                    if (env.BRANCH_NAME == 'dev') {
                        composeUpCommand = 'sudo docker-compose up --build -d consumer-dev'
                    } else if (env.BRANCH_NAME == 'uat') {
                        composeUpCommand = 'sudo docker-compose up --build -d consumer-uat'
                    } else if (env.BRANCH_NAME == 'prod') {
                        composeUpCommand = 'sudo docker-compose up --build -d consumer-prod'
                    } else {
                        error "Unexpected branch"
                    }

                    withCredentials([ 
                        string(credentialsId: 'HOST_IP', variable: 'SERVER_HOST'),
                        string(credentialsId: 'SERVER_USER', variable: 'SERVER_USER'),
                        file(credentialsId: 'SERVER_KEY', variable: 'SSH_KEY_PATH'),
                        string(credentialsId: 'SERVER_PORT', variable: 'SSH_PORT')
                    ]) {
                        sh """
                                ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -i \$SSH_KEY_PATH -p \$SSH_PORT \${SERVER_USER}@\${SERVER_HOST} "cd ${env.ECOM_PATH}/${env.BRANCH_NAME} && ${composeUpCommand} && sudo docker image prune -a --force"
                        """
                    }
                }
            }
        }
    }

    post {
        always {
            script {
                commiterEmail = sh(script: "git show -s --format='%ae'", returnStdout: true).trim()
            }
            cleanWs()
        }
        success {
            emailext body: '${DEFAULT_CONTENT}',
                to: commiterEmail, 
                subject: '${DEFAULT_SUBJECT}', 
                saveOutput: false
        }
        failure {
            emailext body: '${DEFAULT_CONTENT}',
                to: commiterEmail, 
                subject: '${DEFAULT_SUBJECT}', 
                saveOutput: false
        }
    }
}
