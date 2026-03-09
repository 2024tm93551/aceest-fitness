pipeline {
    agent any
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Setup') {
            steps {
                sh 'python3 --version || python --version'
                sh 'pip3 install -r requirements.txt || pip install -r requirements.txt'
            }
        }
        
        stage('Lint') {
            steps {
                sh 'pip3 install flake8 || pip install flake8'
                sh 'flake8 app.py --count --select=E9,F63,F7,F82 --show-source --statistics || true'
            }
        }
        
        stage('Build') {
            steps {
                sh 'python3 -m py_compile app.py || python -m py_compile app.py'
            }
        }
        
        stage('Test') {
            steps {
                sh 'pip3 install pytest || pip install pytest'
                sh 'python3 -m pytest tests/ -v || python -m pytest tests/ -v'
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
    }
}
