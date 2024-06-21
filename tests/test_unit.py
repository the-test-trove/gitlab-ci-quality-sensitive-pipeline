"""Unit tests."""

from unittest import mock

from hypothesis import given, strategies as st
import lib.api
from lib.io import output_stdout, validate
import pytest
import requests


character_strategy = st.characters(blacklist_categories="C")


class TestUnitIO:
    """IO Unit Tests."""

    @given(st.integers(min_value=1))
    def test_validate_happy_path(self, input):
        """Validate happy path."""
        assert validate(input) == input

    @given(st.integers(max_value=0))
    def test_validate_non_positive_integers(self, input):
        """Raise ValueError on non-positive integers."""
        with pytest.raises(ValueError):
            validate(input)

    @given(
        st.none()
        | st.lists(st.integers())
        | st.text(character_strategy)
        | st.dictionaries(st.text(character_strategy), st.integers())
    )
    def test_validate_invalid_input_types(self, input):
        """Raise TypeError on non-positive integers."""
        with pytest.raises(TypeError):
            validate(input)

    def test_output_stdout_happy_path(self):
        """Output to stdout happy path."""
        output = {"name": "John Doe"}
        with mock.patch("builtins.print") as mock_print:
            output_stdout(output)
            mock_print.assert_called_once_with(output["name"])

    @given(
        st.none()
        | st.integers()
        | st.lists(st.integers())
        | st.text(character_strategy)
    )
    def test_output_stdout_invalid_input_types(self, output):
        """Raise TypeError invalid output types."""
        with pytest.raises(TypeError):
            output_stdout(output)

    @given(st.dictionaries(st.text(character_strategy), st.integers()))
    def test_output_stdout_missing_error_key(self, output):
        """Raise KeyError on dicts without name in their keys."""
        with pytest.raises(KeyError):
            output_stdout(output)


class TestUnitApi:
    """API Unit Tests."""

    def test_response_handler_200(self):
        """Tests _response_handler behavior when a 200 status is found."""
        response = mock.Mock()
        response.status_code = 200
        response.json.return_value = {"name": "John Doe"}
        assert lib.api._response_handler(response) == {"name": "John Doe"}

    def test_response_handler_404(self):
        """Tests _response_handler behavior when a 404 status is found."""
        response = mock.Mock()
        response.status_code = 404
        with pytest.raises(ValueError):
            lib.api._response_handler(response)

    def test_response_handler_500(self):
        """Tests _response_handler behavior when a 500 status is found."""
        response = mock.Mock()
        response.status_code = 500
        with pytest.raises(ValueError):
            lib.api._response_handler(response)

    def test_request_handler_timeout(self):
        """Tests _request_handler behavior when a timeout occurs."""
        with mock.patch("requests.get") as mock_get:
            mock_get.side_effect = requests.exceptions.Timeout
            with pytest.raises(Exception):
                lib.api._request_handler("https://example.com")

    def test_request_handler_other_error(self):
        """Tests _request_handler behavior when an error occurs."""
        with mock.patch("requests.get") as mock_get:
            mock_get.side_effect = requests.exceptions.RequestException
            with pytest.raises(Exception):
                lib.api._request_handler("https://example.com")

    def test_get_user_happy_path(self):
        """Tests get_user happy path."""
        with mock.patch("lib.api._request_handler") as mock_request_handler:
            mock_request_handler.return_value = mock.Mock()
            mock_request_handler.return_value.status_code = 200
            mock_request_handler.return_value.json.return_value = {"name": "John Doe"}
            assert lib.api.get_user(1) == {"name": "John Doe"}
