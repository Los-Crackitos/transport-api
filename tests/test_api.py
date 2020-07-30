import pytest


def test_transport_route(client):
    response = client.get('/api/v1/transports')

    assert response.status_code == 200
    assert response.content_type == 'application/json'
