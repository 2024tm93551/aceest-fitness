import json

def test_client_profile_get(client):
    """Test client profile page loads"""
    response = client.get('/client')
    assert response.status_code == 200
    assert b'Client Profile' in response.data

def test_client_profile_post(client):
    """Test client registration"""
    response = client.post('/client', data={
        'name': 'Test User',
        'age': 25,
        'weight': 70,
        'program': 'fat_loss'
    }, follow_redirects=True)
    assert response.status_code == 200
    # After successful POST, should redirect back to client profile page
    assert b'Client Profile' in response.data

def test_api_client_not_found(client):
    """Test API returns 404 for non-existent client"""
    response = client.get('/api/clients/nonexistent')
    assert response.status_code == 404

def test_api_program_detail(client):
    """Test API returns specific program"""
    response = client.get('/api/programs/muscle_gain')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['name'] == 'Muscle Gain (MG)'

def test_api_program_not_found(client):
    """Test API returns 404 for invalid program"""
    response = client.get('/api/programs/invalid')
    assert response.status_code == 404