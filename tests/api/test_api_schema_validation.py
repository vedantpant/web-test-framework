import json
import pytest
import jsonschema

class TestSchemaValidation:

    @pytest.fixture(autouse=True)
    def load_schema(self):
        with open("tests/api/schemas/user_schema.json") as f:
            self.user_schema = json.load(f)

        with open("tests/api/schemas/device_schema.json") as f:
            self.device_schema = json.load(f)

    def test_get_user_matches_schema(self, api_session, api_base_url):
        response = api_session.get(f"{api_base_url}/users/1")
        assert response.status_code == 200

        user = response.json().get("data")
        assert user is not None, "User data should be present"

        try:
            jsonschema.validate(user, self.user_schema)
        except jsonschema.ValidationError as e:
            pytest.fail(f"User response does not match schema: {e.message}")


    def test_get_users_list_all_match_schema(self,api_session, api_base_url):
        response = api_session.get(f"{api_base_url}/users")
        assert response.status_code == 200

        data = response.json()
        users = data.get("data", [])
        assert len(users) > 0, "should return at least one user"

        for idx, user in enumerate(users):
            try:
                jsonschema.validate(user, self.user_schema)
            except jsonschema.ValidationError as e:
                pytest.fail(f"User at index {idx} does not match schema: {e.message}")


    def test_post_user_response_matches_schema(self, api_session, api_base_url, sample_user_payload):
        response = api_session.post(f"{api_base_url}/users", json=sample_user_payload)
        assert response.status_code == 201

        user = response.json()

        assert user.get("id") is not None, "Created user should have an ID"


    def test_user_has_required_fields(self, api_session, api_base_url):
        response = api_session.get(f"{api_base_url}/users/1")
        user = response.json().get("data")

        required_fields = ["id", "email", "first_name", "last_name"]

        for field in required_fields:
            assert field in user, f"User should have required field '{field}'"


    def test_user_has_correct_field_types(self, api_session, api_base_url):
        response = api_session.get(f"{api_base_url}/users/1")

        user = response.json().get("data")
        assert isinstance(user.get("id"), int), "id should be an integer"
        assert isinstance(user.get("email"), str), "email should be a string"
        assert isinstance(user.get("first_name"), str), "first_name should be a string"
        assert isinstance(user.get("last_name"), str), "last_name should be a string"

        if "avatar" in user:
            assert isinstance(user.get("avatar"), str), "avatar should be a string"


    def test_email_format_is_valid(self, api_session, api_base_url):
        response = api_session.get(f"{api_base_url}/users/1")
        user = response.json().get("data")

        email = user.get("email")
        assert email is not None, "Email shoud be present"
        assert "@" in email, "Email should contain '@' symbol"
        assert "." in email.split("@")[1], "email domain should contain a '.' symbol"

    def test_user_id_is_positive(self, api_session, api_base_url):
        response = api_session.get(f"{api_base_url}/users/1")
        user = response.json().get("data")

        user_id = user.get("id")
        assert user_id > 0, "User id should be positive"


    def test_pagination_response_structure(self, api_session, api_base_url):
        response = api_session.get(f"{api_base_url}/users", params={"page": 1})
        assert response.status_code == 200

        data = response.json()

        assert "page" in data, "Response should contain 'page'"
        assert "per_page" in data, "Response should contain 'per_page'"
        assert "total" in data, "Response should contain 'total'"
        assert "total_pages" in data, "Response should contain 'total_pages'"
        assert "data" in data, "Response should contain 'data'"

        assert isinstance(data["data"], list), "'data' should be a list"
        assert isinstance(data["page"], int), "'page' should be an integer"
        assert isinstance(data["per_page"], int), "'per_page' should be an integer"
        assert isinstance(data["total_pages"], int), "'total_pages' should be an integer"
        assert isinstance(data["total"], int), "'total' should be an integer"