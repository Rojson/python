import pytest
from fastapi.testclient import TestClient
from datetime import datetime
from main import app

@pytest.fixture
def client():
    client = TestClient(app)
    return client

def test_get_prime_lower_than_0(client):
    number = -11
    resp = client.get(f"/prime/{number}")
    assert resp.status_code == 200
    expected = False
    assert resp.json() == expected

def test_get_prime(client):
    number = 17
    resp = client.get(f"/prime/{number}")
    assert resp.status_code == 200
    expected = True
    assert resp.json() == expected

def test_get_prime_big_number(client):
    number = 104513
    resp = client.get(f"/prime/{number}")
    assert resp.status_code == 200
    expected = True
    assert resp.json() == expected

def test_get_prime_not_prime(client):
    number = 104512
    resp = client.get(f"/prime/{number}")
    assert resp.status_code == 200
    expected = False
    assert resp.json() == expected

def test_get_prime_out_of_range(client):
    number = 9223372036854775809
    resp = client.get(f"/prime/{number}")
    assert resp.status_code == 200
    expected = False
    assert resp.json() == expected

def test_get_secure_endpoint(client):
    key = 'zeszytdopolskiego'
    resp = client.get(f"/secure_endpoint?access_token={key}")
    assert resp.status_code == 200

def test_get_secure_endpoint_bad_key(client):
    key = 'zeszytdomatematyki'
    resp = client.get(f"/secure_endpoint?access_token={key}")
    assert resp.status_code == 403