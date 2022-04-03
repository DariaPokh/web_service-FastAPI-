from main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_health_check():
    response = client.get('http://127.0.0.1:8000/docs#')
    assert response.status_code == 200


def test_health_check_post():
    response = client.get('http://127.0.0.1:8000/docs#/images/post_images_post_post')
    assert response.status_code == 200


def test_health_check_get():
    response = client.get('http://127.0.0.1:8000/docs#/images/get_images_get__request_code__get')
    assert response.status_code == 200


def test_health_check_delete():
    response = client.get('http://127.0.0.1:8000/docs#/images/get_images_delete__request_code__delete')
    assert response.status_code == 200
