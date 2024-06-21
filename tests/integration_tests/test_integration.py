"""Integration tests."""

from lib.api import get_user
import pytest


class TestIntegrationApi:
    """API integration tests."""

    def test_get_user_happy_path(self):
        """Tests get_user happy path."""
        user_id = 1
        user = get_user(user_id)
        assert user["name"] == "Leanne Graham"

    def test_get_inexisting_user(self):
        """Tests get_user happy path."""
        user_id = 1000
        with pytest.raises(ValueError):
            get_user(user_id)
