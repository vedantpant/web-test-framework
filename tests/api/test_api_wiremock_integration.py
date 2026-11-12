import pytest
import requests

class TestWireMockIntegration:

    def test_wiremock_server_is_running(self, wiremock_url):
        try:
            response = requests.get(f"{wiremock_url}/__admin/mappings")
            assert response.status_code == 200, "wiremock server should be running"
        except requests.ConnectionError:
            pytest.skip("Wremock server not running on localhost: 8080")

    def test_wremock_returns_stubbed_user(self, wiremock_url):
        stub = {
            "request": {
                "method": "GET",
                "url" : "/api/mock/users/1"
            },
            "response" : {
                "status": 200,
                "headers": {"Content-Type": "application/json"},
                "jsonBody": {"id": 1, "name": "Mock User"}
            }
        }

        register = requests.post(f"{wiremock_url}/__admin/mappings", json=stub)
        assert register.status_code == 201, f"Failed to register stub with WireMock {register.text}"

        response = requests.get(f"{wiremock_url}/api/mock/users/1")

        assert response.status_code == 200
        assert response.json()["name"] == "Mock User"

    def test_wiremock_returns_stubbed_server_error(self, wiremock_url):
        stub = {
            "request": {
                "method": "GET",
                "url" : "/api/mock/users/500"
            },

            "response" : {
                "status":   500,
                "headers": {"Content-Type": "applcation/json"},
                "jsonBody": {"error": "Internal server error"}
            }
        }

        register = requests.post(f"{wiremock_url}/__admin/mappings", json=stub)
        assert register.status_code == 201, f"Stub registration failed: {register.text}"

        response = requests.get(f"{wiremock_url}/api/mock/users/500")

        assert response.status_code == 500
        assert response.json()["error"] == "Internal server error"

    def test_session_retries_500_then_gives_up(self, api_session, wiremock_url):
        stub = {
            "request": {
                "method": "GET",
                "url": "/api/mock/retry"
            },
            "response": {
                "status": 500,
                "jsonBody": {"error": "Internal Server Error"}
            }
        }

        register = requests.post(f"{wiremock_url}/__admin/mappings", json=stub)
        assert register.status_code == 201, f"Stub registration failed: {register.text}" 

        with pytest.raises(requests.exceptions.RetryError):
            api_session.get(f"{wiremock_url}/api/mock/retry")

        count_response = requests.post(f"{wiremock_url}/__admin/requests/count", 
                                       json={"method": "GET", "url": "/api/mock/retry"}
                                       )

        count = count_response.json()["count"]
        assert count == 4, f"Expected 1 orgnial + 3 retries, got {count} requests"