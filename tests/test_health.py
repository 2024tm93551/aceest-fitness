import json


def test_health_api_programs_structure(client):
    """Test API programs returns correct structure"""
    response = client.get('/api/programs')
    assert response.status_code == 200
    data = json.loads(response.data)
    for prog in data.values():
        assert 'name' in prog
        assert 'workout' in prog
        assert 'diet' in prog


def test_health_api_metrics_fields(client):
    """Test gym metrics has all required fields"""
    response = client.get('/api/metrics')
    data = json.loads(response.data)
    assert 'capacity' in data
    assert 'area_sqft' in data
    assert 'break_even_members' in data


def test_health_calorie_fat_loss(client):
    """Test calorie calculation for fat loss program"""
    response = client.post(
        '/api/calculate-calories',
        data=json.dumps({'weight': 80, 'program': 'fat_loss'}),
        content_type='application/json'
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['calories'] == 1760


def test_health_calorie_muscle_gain(client):
    """Test calorie calculation for muscle gain program"""
    response = client.post(
        '/api/calculate-calories',
        data=json.dumps({'weight': 80, 'program': 'muscle_gain'}),
        content_type='application/json'
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['calories'] == 2800


def test_health_404_page(client):
    """Test 404 returns correct status"""
    response = client.get('/programs/nonexistent_program')
    assert response.status_code == 404


def test_health_clients_api(client):
    """Test clients API returns list"""
    response = client.get('/api/clients')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)


def test_health_client_register(client):
    """Test client registration returns success message"""
    # Use with client to preserve session/flash messages through redirects
    with client:
        response = client.post('/client', data={
            'name': 'HealthCheckUser',
            'age': 30,
            'weight': 75,
            'program': 'beginner'
        }, follow_redirects=True)
        assert response.status_code == 200
        # Check for flash message in rendered template
        assert b'HealthCheckUser' in response.data
        assert b'saved successfully' in response.data