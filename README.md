# ACEest Fitness & Gym

Flask-based fitness management application with CI/CD pipeline for the DevOps Assignment.

## Features

- **Fitness Programs**: Fat Loss, Muscle Gain, and Beginner programs
- **Client Management**: Register and track clients with SQLite
- **Calorie Calculator**: Automatic calculation based on weight and program
- **Progress Tracking**: Weekly adherence logging
- **REST API**: JSON endpoints for all data
- **CSV Export**: Export client data
- **Containerized**: Docker support

## Local Setup

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/aceest-fitness.git
cd aceest-fitness
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
python app.py
```

Visit `http://localhost:5000` in your browser.

## Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=app
```

## Docker

### Build Image
```bash
docker build -t aceest-fitness .
```

### Run Container
```bash
docker run -p 5000:5000 aceest-fitness
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Home page |
| `/programs` | GET | List all programs |
| `/programs/<id>` | GET | Program details |
| `/client` | GET/POST | Client registration |
| `/clients` | GET | All clients |
| `/api/programs` | GET | All programs (JSON) |
| `/api/clients` | GET | All clients (JSON) |
| `/api/metrics` | GET | Gym metrics (JSON) |
| `/api/calculate-calories` | POST | Calculate calories |

## CI/CD Pipeline

### GitHub Actions
- **Trigger**: Push to `master`/`develop` or Pull Request to `master`
- **Stages**:
  1. Lint with flake8
  2. Run pytest suite
  3. Build Docker image
  4. Test container health

### Jenkins
- **Stages**:
  1. Checkout source code
  2. Setup Python environment
  3. Lint code
  4. Compile Python files
  5. Run tests with JUnit output
  6. Build Docker image

## Project Structure

```
aceest-fitness/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── Dockerfile            # Container definition
├── Jenkinsfile           # Jenkins pipeline
├── .github/
│   └── workflows/
│       └── main.yml      # GitHub Actions
├── templates/            # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── programs.html
│   ├── program_detail.html
│   ├── client.html
│   ├── clients.html
│   └── 404.html
└── tests/                # Pytest tests
    ├── conftest.py
    ├── test_app.py
    └── test_routes.py
```

## Version Control

This project follows semantic commit messages:
- `feat:` - New features
- `fix:` - Bug fixes
- `docs:` - Documentation
- `test:` - Tests
- `chore:` - Maintenance
- `ci:` - CI/CD changes

## Author

Thivyata - 2024tm93551
## License

Educational use only.
