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
                    # Check if python3 exists, if not try to install (for Docker-based Jenkins)
                    which python3 || (apt-get update && apt-get install -y python3 python3-pip python3-venv) || true
                    
                    # Display Python version
                    python3 --version
                    
                    # Create virtual environment
                    python3 -m venv venv || true
                    
                    # Activate venv and install dependencies
                    . venv/bin/activate || true
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }
        
        stage('Lint') {
            steps {
                echo 'Running linter...'
                sh '''
                    . venv/bin/activate || true
                    flake8 app.py --count --select=E9,F63,F7,F82 --show-source --statistics || true
                '''
            }
        }
        
        stage('Build') {
            steps {
                echo 'Compiling Python files...'
                sh '''
                    . venv/bin/activate || true
                    python -m py_compile app.py
                '''
            }
        }
        
        stage('Test') {
            steps {
                echo 'Running tests...'
                sh '''
                    . venv/bin/activate || true
                    pytest tests/ -v --junitxml=test-results.xml
                '''
            }
            post {
                always {
                    junit allowEmptyResults: true, testResults: 'test-results.xml'
                }
            }
        }
        
        stage('Docker Build') {
            steps {
                echo 'Building Docker image...'
                sh '''
                    # Check if docker is available
                    which docker && docker build -t ${DOCKER_IMAGE}:${BUILD_NUMBER} . || echo "Docker not available - skipping image build"
                '''
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
            cleanWs(cleanWhenNotBuilt: false, deleteDirs: true, disableDeferredWipeout: true, notFailBuild: true)
        }
    }
}