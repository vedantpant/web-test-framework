import pytest

class TestStatusCodes:

    def test_get_users_success(self, api_session,api_base_url):
        response = api_session.get(f"{api_base_url}/users")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        assert response.json() is not None, "Response body should not be empty"

    def test_get_single_user_success(self, api_session, api_base_url):
        response = api_session.get(f"{api_base_url}/users/1")
        assert response.status_code == 200
        user = response.json().get("data")
        assert user is not None, "User data should not be present"
        assert user.get("id") == 1, "User ID should be 1"

    def test_get_nonexistent_user_404(self, api_session, api_base_url):
        response = api_session.get(f"{api_base_url}/users/9999")
        assert response.status_code == 404, f"Expected 404, got {response.status_code}"

    def test_post_user_created(self, api_session, api_base_url, sample_user_payload):
        response = api_session.post(f"{api_base_url}/users", json=sample_user_payload)
        assert response.status_code == 201, f"Expected 201, got {response.status_code}"
        user = response.json()
        assert user.get("name") == sample_user_payload["name"]
        assert user.get("id") is not None, "Created user should have an ID"

    def test_put_user_updated(self, api_session, api_base_url, sample_user_payload):
        updated_data = {**sample_user_payload, "name": "jane doe"}
        response = api_session.put(f"{api_base_url}/users/1", json=updated_data)
        assert response.status_code == 200
        user = response.json()
        assert user.get("name") == "jane doe", "User name should be updated"

    def test_delete_user_success(self, api_session, api_base_url):
        response = api_session.delete(f"{api_base_url}/users/1")
        assert response.status_code == 204, f"expected 204, got {response.status_code}"
        assert response.text == "" or response.text is None, "204 should have no body"

    def test_get_user_with_pagination(self, api_session, api_base_url):
        response = api_session.get(f"{api_base_url}/users", params={"page": 2})
        assert response.status_code == 200
        data = response.json()
        assert data.get("page") == 2, "page number should be 2"
        assert data.get("data") is not None, "should have data array"

    def test_response_time_acceptable(self, api_session, api_base_url):
        import time
        start_time = time.time()
        response = api_session.get(f"{api_base_url}/users")
        elapsed = time.time() - start_time

        assert response.status_code == 200
        assert elapsed < 5.0, f"Request took {elapsed:.2f}s, expected < 5s (performance issue)"