import pytest
import time

def test_real_api_create_user_echoes_name(api_session, api_base_url):
    payload = {"name": "John Doe", "job": "QA Engineer"}
    response = api_session.post(f"{api_base_url}/users", json=payload)

    if response.status_code == 429:
        pytest.skip("Rate limit exceeded, skipping test.")

    assert response.status_code == 201, f"Expected 201, got {response.status_code}"
    body = response.json()
    assert body["name"] == "John Doe"
    assert body["job"] == "QA Engineer"
    assert "id" in body, "Response should contain an 'id' field"
    assert "createdAt" in body, "Response should contain a 'createdAt' field"


def test_real_api_create_user_accented_name(api_session, api_base_url):
    time.sleep(2)

    payload = {
        "name": "Jose garcia",
        "job": "QA Engineer"
    }

    response = api_session.post(f"{api_base_url}/users", json=payload)

    if response.status_code == 429:
        pytest.skip("reqres.in rate limit exceeded, skipping test.")

    assert response.status_code == 201, f"Expected 201, got {response.status_code}"
    assert response.json()["name"] == "Jose garcia", "Accented characters should come back unchanged."