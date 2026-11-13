import pytest
import requests

PAYLOAD_CASES = [
    ("John Doe", 201),
    ("Jose Garcia", 201),
    ("A" * 255, 201),
]

@pytest.mark.parametrize(
    "name, expected_status",
    PAYLOAD_CASES, 
    ids=["plain-ascii", "accented-chars", "long-name"],
)
def test_post_payload_variations(wiremock_url, name, expected_status):
    stub = {
        "request": {
            "method": "POST",
            "url": "/api/mock/payload",
            "bodyPatterns": [
                {"equalToJson": {"name": name, "job": "QA Engineer"}}
            ]
        },
        "response": {
            "status": expected_status,
            "jsonBody": {"name": name}
        }
    }

    register = requests.post(f"{wiremock_url}/__admin/mappings", json=stub)
    assert register.status_code == 201, f"Stub registration failed: {register.text}"

    response = requests.post(
        f"{wiremock_url}/api/mock/payload",
        json={"name": name, "job": "QA Engineer"}
    )

    assert response.status_code == expected_status
    assert response.json()["name"] == name


INVALID_CASES = [
    ({"name": "", "job": "QA Engineer"}, "name is required"),
    ({"name": None, "job": "QA Engineer"}, "name must be a string"),
    ({"name": 12345, "job": "QA Engineer"}, "name must be a string"),
]
@pytest.mark.parametrize(
    "payload, expected_error",
    INVALID_CASES,
    ids=["empty-name", "null-name", "numeric-name"]
)
def test_post_invalid_payload(wiremock_url, payload, expected_error):
    stub = {
         "request": {
            "method": "POST",
            "url": "/api/mock/payload/invalid",
            "bodyPatterns": [
                {"equalToJson": payload}
            ]
        },
        "response": {
            "status": 400,
            "jsonBody": {"error": expected_error}
        }
    }

    register = requests.post(f"{wiremock_url}/__admin/mappings", json=stub)
    assert register.status_code == 201, f"Stub registration failed: {register.text}"

    response = requests.post(
        f"{wiremock_url}/api/mock/payload/invalid",
        json=payload
    )
    assert response.status_code == 400
    assert response.json()["error"] == expected_error