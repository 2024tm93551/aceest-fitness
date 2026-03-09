pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = 'aceest-fitness'
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out source code...'
                checkout scm
            }
        }
        
        stage('Setup Python') {
            steps {
                echo 'Setting up Python environment...'
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }
        
        stage('Lint') {
            steps {
                echo 'Running linter...'
                sh '''
                    . venv/bin/activate
                    flake8 app.py --count --select=E9,F63,F7,F82 --show-source --statistics || true
                '''
            }
        }
        
        stage('Build') {
            steps {
                echo 'Compiling Python files...'
                sh '''
                    . venv/bin/activate
                    python -m py_compile app.py
                '''
            }
        }
        
        stage('Test') {
            steps {
                echo 'Running tests...'
                sh '''
                    . venv/bin/activate
                    pytest tests/ -v --junitxml=test-results.xml
                '''
            }
            post {
                always {
                    junit 'test-results.xml'
                }
            }
        }
        
        stage('Docker Build') {
            steps {
                echo 'Building Docker image...'
                sh "docker build -t ${DOCKER_IMAGE}:${BUILD_NUMBER} ."
            }
        }
    }
    
    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed!'
        }
        always {
            cleanWs()
        }
    }
}
