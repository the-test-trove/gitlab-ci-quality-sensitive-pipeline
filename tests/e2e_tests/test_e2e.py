"""End-to-end tests."""

import subprocess


class TestEndToEnd:
    """End-to-end tests."""

    def test_get_user_happy_path(self):
        """Tests get_user happy path."""
        user_id = 1
        output = subprocess.check_output(["./get_user.py", str(user_id)])
        assert output.decode("utf-8") == "Leanne Graham\n"
