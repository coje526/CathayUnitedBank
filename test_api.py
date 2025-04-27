import pytest
import httpx

BASE_URL = "http://backend:8000"


@pytest.mark.parametrize("page", [1, 2])
def test_get_products(page):
    response = httpx.get(f"{BASE_URL}/products", params={"page": page})
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_products_price_between():
    response = httpx.get(f"{BASE_URL}/products", params={"between": "price,10,50"})
    assert response.status_code == 200
    for product in response.json():
        assert 10 <= product["price"] <= 50

def test_get_products_invalid_between():
    response = httpx.get(f"{BASE_URL}/products", params={"between": "price,abc,50"})
    assert response.status_code == 400

def test_get_products_sort_name_asc():
    response = httpx.get(f"{BASE_URL}/products", params={"sort": "name,asc"})
    assert response.status_code == 200

def test_get_single_product_success():
    response = httpx.get(f"{BASE_URL}/products/1")
    assert response.status_code == 200
    assert response.json()["id"] == "1"

def test_get_single_product_not_found():
    response = httpx.get(f"{BASE_URL}/products/9999")
    assert response.status_code == 404

def test_get_product_illegal_character():
    response = httpx.get(f"{BASE_URL}/products/&")
    assert response.status_code in (400, 422, 404)

def test_post_message_success():
    payload = {
        "name": "John Doe",
        "subject": "Test Subject",
        "message": "Test Message Content",
        "email": "johndoe@example.com"
    }
    response = httpx.post(f"{BASE_URL}/messages", json=payload)
    assert response.status_code == 200

def test_post_message_invalid_email():
    payload = {
        "name": "John Doe",
        "subject": "Test Subject",
        "message": "Test Message Content",
        "email": "invalid_email"
    }
    response = httpx.post(f"{BASE_URL}/messages", json=payload)
    assert response.status_code == 422

def test_post_message_empty_subject_message():
    payload = {
        "name": "John Doe",
        "subject": "",
        "message": "",
        "email": "johndoe@example.com"
    }
    response = httpx.post(f"{BASE_URL}/messages", json=payload)
    assert response.status_code == 422
