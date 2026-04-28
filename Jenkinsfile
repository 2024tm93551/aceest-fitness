pipeline {
    agent any

    environment {
        DOCKER_HUB_USER  = '2024tm93551thivyata'
        DOCKER_IMAGE     = 'aceest-fitness'
        DOCKER_HUB_REPO  = "${DOCKER_HUB_USER}/${DOCKER_IMAGE}"
        SONAR_PROJECT    = 'aceest-fitness'
    }

    stages {

        // ── Stage 1: Pull source code from GitHub ──────────────
        stage('Checkout') {
            steps {
                echo '=== Stage 1: Checkout Source Code ==='
                checkout scm
            }
        }

        // ── Stage 2: Create venv and install Python deps ───────
        stage('Setup Python') {
            steps {
                echo '=== Stage 2: Setup Python Environment ==='
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        // ── Stage 3: Lint - check for syntax errors ────────────
        stage('Lint') {
            steps {
                echo '=== Stage 3: Lint with flake8 ==='
                sh '''
                    . venv/bin/activate
                    flake8 app.py --count --select=E9,F63,F7,F82 \
                        --show-source --statistics || true
                '''
            }
        }

        // ── Stage 4: Compile check ─────────────────────────────
        stage('Build') {
            steps {
                echo '=== Stage 4: Build (Compile Check) ==='
                sh '''
                    . venv/bin/activate
                    python -m py_compile app.py
                    echo "Build successful - no syntax errors"
                '''
            }
        }

        // ── Stage 5: Run all pytest tests with coverage ────────
        stage('Test') {
            steps {
                echo '=== Stage 5: Run Tests with Coverage ==='
                sh '''
                    . venv/bin/activate
                    pytest tests/ -v \
                        --junitxml=test-results.xml \
                        --cov=app \
                        --cov-report=xml:coverage.xml \
                        --cov-report=term-missing
                '''
            }
            post {
                always {
                    junit 'test-results.xml'
                }
            }
        }

        // ── Stage 6: SonarQube code quality scan ───────────────
        stage('SonarQube Analysis') {
            steps {
                echo '=== Stage 6: SonarQube Code Quality Analysis ==='
                withSonarQubeEnv('SonarQube') {
                    script {
                        def scannerHome = tool 'SonarScanner'
                        sh """
                            ${scannerHome}/bin/sonar-scanner \
                                -Dsonar.projectKey=${SONAR_PROJECT} \
                                -Dsonar.projectName="ACEest Fitness and Gym" \
                                -Dsonar.projectVersion=2.0 \
                                -Dsonar.sources=. \
                                -Dsonar.language=py \
                                -Dsonar.python.version=3.11 \
                                -Dsonar.exclusions=**/venv/**,**/__pycache__/** \
                                -Dsonar.python.coverage.reportPaths=coverage.xml \
                                -Dsonar.token=${SONAR_AUTH_TOKEN}
                        """
                    }
                }
            }
        }

        // ── Stage 7: Wait for SonarQube quality gate result ────
        stage('Quality Gate') {
            steps {
                echo '=== Stage 7: Checking SonarQube Quality Gate ==='
                timeout(time: 5, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        // ── Stage 8: Build Docker image ─────────────────────────
        stage('Docker Build') {
            steps {
                echo '=== Stage 8: Build Docker Image ==='
                sh """
                    docker build \
                        -t ${DOCKER_HUB_REPO}:${BUILD_NUMBER} \
                        -t ${DOCKER_HUB_REPO}:latest \
                        .
                """
            }
        }

        // ── Stage 9: Push image to Docker Hub registry ─────────
        stage('Docker Push') {
            steps {
                echo '=== Stage 9: Push to Docker Hub Registry ==='
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh '''
                        echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                        docker push ${DOCKER_HUB_REPO}:${BUILD_NUMBER}
                        docker push ${DOCKER_HUB_REPO}:latest
                        echo "Image pushed: ${DOCKER_HUB_REPO}:${BUILD_NUMBER}"
                        echo "Image pushed: ${DOCKER_HUB_REPO}:latest"
                    '''
                }
            }
        }

        // ── Stage 10: Deploy to Minikube / Kubernetes ──────────
        stage('Deploy to Kubernetes') {
            steps {
                echo '=== Stage 10: Deploy to Minikube ==='
                sh """
                    # Update the image tag in the deployment
                    kubectl set image deployment/aceest-fitness \
                        aceest-fitness=${DOCKER_HUB_REPO}:${BUILD_NUMBER} \
                        --record || true

                    # Apply all k8s manifests (first-time or update)
                    kubectl apply -f k8s/configmap.yaml
                    kubectl apply -f k8s/deployment.yaml
                    kubectl apply -f k8s/service.yaml

                    # Wait for rolling update to finish (zero-downtime)
                    kubectl rollout status deployment/aceest-fitness \
                        --timeout=120s

                    echo "Deployment complete!"
                    kubectl get pods
                    kubectl get services
                """
            }
        }
    }

    // ── Post-pipeline actions ───────────────────────────────────
    post {
        success {
            echo '✅ Pipeline PASSED - ACEest Fitness is deployed!'
        }
        failure {
            echo '❌ Pipeline FAILED - Rolling back deployment...'
            sh 'kubectl rollout undo deployment/aceest-fitness || true'
        }
        always {
            cleanWs()
        }
    }
}
