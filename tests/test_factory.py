from webtrap import create_app


def test_config():
    """Test create_app without passing test config."""
    assert not create_app().testing
    assert create_app({"TESTING": True}).testing


def test_api_main(client):
    response = client.get('/api')
    assert b'list' in response.data
    assert response.status_code == 200

def test_api_create(client):
    response = client.get('/api/create')
    assert b'created' in response.data
    assert response.status_code == 200

def test_api_delete(client):
    response = client.get('/api/delete')
    assert b'deleted' in response.data
    assert response.status_code == 200
    response = client.get('/api/delete?notawaiting=1')
    assert b'notawaiting' in response.data
    assert response.status_code == 400
    response = client.get('/api/delete?notawaiting=0')
    assert b'deleted' in response.data
    assert response.status_code == 200

def test_api_read(client):
    response = client.get('/api/read')
    assert b'readed' in response.data
    assert response.status_code == 200

def test_api_invalid(client):
    response = client.get('/api/create?invalid=1')
    assert b'invalid' in response.data
    assert response.status_code == 400
    response = client.get('/api?invalid=1')
    assert b'invalid' in response.data
    assert response.status_code == 400
    response = client.get('/api/create?invalid=0')
    assert b'created' in response.data
    assert response.status_code == 200
    response = client.get('/api?invalid=0')
    assert b'list' in response.data
    assert response.status_code == 200

def test_api_not_implemented(client):
    response = client.get('/api/update')
    assert response.status_code == 501
    response = client.get('/api/slap')
    assert response.status_code == 501

def test_post(client):
    response = client.post('/api')
    assert response.status_code == 405

def test_not_api_request(client):
    response = client.get('/')
    assert response.status_code == 404
    response = client.get('/lol')
    assert response.status_code == 404
    response = client.get('/kek')
    assert response.status_code == 404
