import pytest
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import json
from pathlib import Path

API_BASE_URL = "https://reqres.in/api"
WIREMOCK_URL = "http://localhost:8080"

def get_session_with_retries():
    session = requests.Session()
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429,500,502,503,504],
        allowed_methods=["HEAD","GET","OPTIONS","POST","PUT","DELETE"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session

@pytest.fixture(scope="session")
def api_session():
    session = get_session_with_retries()
    yield session
    session.close()

@pytest.fixture
def api_base_url():
    return API_BASE_URL

@pytest.fixture
def wiremock_url():
    return WIREMOCK_URL

@pytest.fixture
def sample_user_payload():
    return {
        "name": "John Doe",
        "job": "QA Engineer"
    }

@pytest.fixture(autouse=True)
def log_api_call(request):
    print(f"\n[API TEST] {request.node.name}")
    yield
    print(f"[API TEST COMPLETE] {request.node.name}")