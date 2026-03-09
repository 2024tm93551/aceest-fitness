import json

def test_home_page(client):
    """Test home page returns 200"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'ACEest' in response.data

def test_programs_page(client):
    """Test programs page returns 200"""
    response = client.get('/programs')
    assert response.status_code == 200
    assert b'Fitness Programs' in response.data

def test_program_detail(client):
    """Test individual program page"""
    response = client.get('/programs/fat_loss')
    assert response.status_code == 200
    assert b'Fat Loss' in response.data

def test_program_not_found(client):
    """Test 404 for invalid program"""
    response = client.get('/programs/invalid')
    assert response.status_code == 404

def test_api_programs(client):
    """Test API returns all programs as JSON"""
    response = client.get('/api/programs')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'fat_loss' in data
    assert 'muscle_gain' in data
    assert 'beginner' in data

def test_api_metrics(client):
    """Test API returns gym metrics"""
    response = client.get('/api/metrics')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['capacity'] == 150

def test_calculate_calories(client):
    """Test calorie calculation API"""
    response = client.post('/api/calculate-calories',
                          data=json.dumps({'weight': 70, 'program': 'fat_loss'}),
                          content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['calories'] == 1540  # 70 * 22

def test_clients_page(client):
    """Test clients list page"""
    response = client.get('/clients')
    assert response.status_code == 200
