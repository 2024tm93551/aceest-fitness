# ACEest Fitness & Gym - DevOps Assignment 2

Flask-based fitness management application with a fully automated CI/CD pipeline
including SonarQube code quality, Docker Hub registry, and Kubernetes deployment.

## Features

- **Fitness Programs**: Fat Loss, Muscle Gain, Beginner programs
- **Client Management**: SQLite-backed client registration and tracking
- **Calorie Calculator**: Auto-calculation based on weight and program
- **Progress Tracking**: Weekly adherence and chart visualization
- **Workout & Metrics Logging**: Full activity history
- **REST API**: JSON endpoints for all data
- **Containerized**: Docker + Kubernetes deployment

---

## Local Setup

### 1. Clone Repository
```bash
git clone https://github.com/YOUR_USERNAME/aceest-fitness.git
cd aceest-fitness
```

### 2. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate        # macOS/Linux
# venv\Scripts\activate         # Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the App
```bash
python app.py
```
Visit http://localhost:5000

---

## Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage report
pytest tests/ -v --cov=app --cov-report=term-missing
```

---

## Docker

### Build Image
```bash
docker build -t aceest-fitness:latest .
```

### Run Container
```bash
docker run -d -p 5000:5000 --name aceest aceest-fitness:latest
```

### Push to Docker Hub
```bash
docker tag aceest-fitness:latest YOUR_USERNAME/aceest-fitness:latest
docker push YOUR_USERNAME/aceest-fitness:latest
```

---

## Kubernetes (Minikube)

### Start Minikube
```bash
minikube start
```

### Deploy Application
```bash
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

### Access Application
```bash
minikube service aceest-fitness-service
```

### Check Status
```bash
kubectl get pods
kubectl get deployments
kubectl get services
```

### Rolling Update (Zero-Downtime)
```bash
# Update image version
kubectl set image deployment/aceest-fitness \
  aceest-fitness=YOUR_USERNAME/aceest-fitness:NEW_VERSION

# Watch update progress
kubectl rollout status deployment/aceest-fitness
```

### Rollback if Something Goes Wrong
```bash
kubectl rollout undo deployment/aceest-fitness
```

---

## CI/CD Pipeline

### GitHub Actions (automatic on every push)
| Stage | Tool | What it does |
|-------|------|--------------|
| Lint | flake8 | Checks code syntax |
| Test | pytest | Runs 20 test cases with coverage |
| Docker Build | Docker | Builds container image |
| Docker Push | Docker Hub | Pushes to registry |

### Jenkins Pipeline (10 stages)
| Stage | Tool | What it does |
|-------|------|--------------|
| Checkout | Git | Pulls latest code |
| Setup Python | pip | Creates venv, installs deps |
| Lint | flake8 | Code style check |
| Build | Python | Syntax compilation check |
| Test | pytest | 20 tests + coverage XML |
| SonarQube Analysis | sonar-scanner | Code quality scan |
| Quality Gate | SonarQube | Blocks pipeline if quality fails |
| Docker Build | Docker | Builds image with build number tag |
| Docker Push | Docker Hub | Pushes versioned image |
| Deploy to Kubernetes | kubectl | Rolling deployment to Minikube |

---

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Home page |
| `/programs` | GET | All fitness programs |
| `/programs/<id>` | GET | Program detail page |
| `/client` | GET/POST | Client registration |
| `/clients` | GET | All clients list |
| `/clients/export` | GET | Export CSV |
| `/workout/<name>` | GET/POST | Log workout |
| `/metrics/<name>` | GET/POST | Log body metrics |
| `/progress/<name>/chart` | GET | Progress chart |
| `/api/programs` | GET | JSON - all programs |
| `/api/clients` | GET | JSON - all clients |
| `/api/clients/<name>` | GET | JSON - one client |
| `/api/metrics` | GET | JSON - gym metrics |
| `/api/bmi/<name>` | GET | JSON - BMI calculation |
| `/api/calculate-calories` | POST | JSON - calorie calculation |

---

## Project Structure

```
aceest-fitness/
├── app.py                         # Flask application (main)
├── requirements.txt               # Python dependencies
├── Dockerfile                     # Container definition
├── Jenkinsfile                    # Jenkins 10-stage pipeline
├── sonar-project.properties       # SonarQube config
├── .github/
│   └── workflows/
│       └── main.yml               # GitHub Actions workflow
├── k8s/
│   ├── configmap.yaml             # Environment variables
│   ├── deployment.yaml            # K8s deployment (rolling update)
│   └── service.yaml               # K8s service (NodePort)
├── templates/                     # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── programs.html
│   ├── program_detail.html
│   ├── client.html
│   ├── client_detail.html
│   ├── clients.html
│   ├── progress_chart.html
│   ├── log_workout.html
│   ├── workout_history.html
│   ├── log_metrics.html
│   └── 404.html
└── tests/
    ├── conftest.py
    ├── test_app.py
    ├── test_routes.py
    └── test_health.py
```

---

## Semantic Commit Messages

| Prefix | Meaning |
|--------|---------|
| `feat:` | New feature |
| `fix:` | Bug fix |
| `docs:` | Documentation |
| `test:` | Tests |
| `chore:` | Maintenance |
| `ci:` | CI/CD changes |

---

## Author

[Your Name] - BITS Pilani DevOps Assignment 2  
Course: Introduction to DevOps (CSIZG514/SEZG514)

## License

Educational use only.
