"""Tests for the API client in api.py."""

import pytest
import respx
from httpx import Response

from pyeducationdata.api import APIClient
from pyeducationdata.exceptions import APIConnectionError


class TestAPIClient:
    """Tests for the APIClient class."""

    def test_client_initialization(self):
        """Test that client initializes correctly."""
        client = APIClient()
        assert client.base_url is not None
        assert client.timeout > 0
        assert client.max_retries > 0
        client.close()

    def test_client_context_manager(self):
        """Test client as context manager."""
        with APIClient() as client:
            assert client.client is not None

    @respx.mock
    def test_successful_get_request(self, mock_api_response):
        """Test successful GET request."""
        url = "https://educationdata.urban.org/api/v1/schools/ccd/enrollment/"

        respx.get(url).mock(return_value=Response(200, json=mock_api_response))

        with APIClient() as client:
            response = client.get(url)
            assert "results" in response
            assert response["count"] == 100

    @respx.mock
    def test_404_error(self):
        """Test handling of 404 errors."""
        url = "https://educationdata.urban.org/api/v1/invalid/endpoint/"

        respx.get(url).mock(return_value=Response(404, json={"error": "Not found"}))

        with APIClient() as client:
            with pytest.raises(APIConnectionError, match="404"):
                client.get(url)

    @respx.mock
    def test_500_error(self):
        """Test handling of 500 errors."""
        url = "https://educationdata.urban.org/api/v1/schools/ccd/enrollment/"

        respx.get(url).mock(return_value=Response(500, json={"error": "Server error"}))

        with APIClient() as client:
            with pytest.raises(APIConnectionError, match="500"):
                client.get(url)

    @respx.mock
    def test_retry_on_503(self):
        """Test that client retries on 503 errors."""
        url = "https://educationdata.urban.org/api/v1/schools/ccd/enrollment/"

        # First request returns 503, second succeeds
        route = respx.get(url)
        route.side_effect = [
            Response(503, json={"error": "Service unavailable"}),
            Response(200, json={"results": [], "count": 0}),
        ]

        with APIClient(max_retries=2) as client:
            response = client.get(url)
            assert "results" in response

    @respx.mock
    def test_max_retries_exceeded(self):
        """Test that APIConnectionError is raised after max retries."""
        url = "https://educationdata.urban.org/api/v1/schools/ccd/enrollment/"

        # Always return 503
        respx.get(url).mock(return_value=Response(503, json={"error": "Service unavailable"}))

        with APIClient(max_retries=2) as client:
            with pytest.raises(APIConnectionError, match="failed after"):
                client.get(url)

    @respx.mock
    def test_get_json_response(self, mock_api_response):
        """Test get_json_response method."""
        url = "https://educationdata.urban.org/api/v1/schools/ccd/enrollment/"

        respx.get(url).mock(return_value=Response(200, json=mock_api_response))

        with APIClient() as client:
            response = client.get_json_response(url)
            assert hasattr(response, "results")
            assert hasattr(response, "count")
            assert hasattr(response, "next")
            assert len(response.results) == 2

    @respx.mock
    def test_invalid_json_response(self):
        """Test handling of invalid JSON responses."""
        url = "https://educationdata.urban.org/api/v1/schools/ccd/enrollment/"

        respx.get(url).mock(return_value=Response(200, text="Invalid JSON"))

        with APIClient() as client:
            with pytest.raises(APIConnectionError, match="parse JSON"):
                client.get(url)

    @respx.mock
    def test_get_metadata(self, mock_metadata_response):
        """Test metadata retrieval."""
        url = "https://educationdata.urban.org/api/v1/api-endpoints/"

        respx.get(url).mock(return_value=Response(200, json=mock_metadata_response))

        with APIClient() as client:
            metadata = client.get_metadata("endpoints")
            assert "results" in metadata
            assert len(metadata["results"]) == 2

    def test_invalid_metadata_type(self):
        """Test that invalid metadata type raises error."""
        with APIClient() as client:
            with pytest.raises(ValueError, match="Invalid metadata type"):
                client.get_metadata("invalid_type")


class TestDefaultClient:
    """Tests for default client singleton."""

    def test_get_default_client(self):
        """Test getting default client instance."""
        from pyeducationdata.api import close_default_client, get_default_client

        # Clean up any existing client
        close_default_client()

        client1 = get_default_client()
        client2 = get_default_client()

        # Should return same instance
        assert client1 is client2

        # Clean up
        close_default_client()

    def test_close_default_client(self):
        """Test closing default client."""
        from pyeducationdata.api import close_default_client, get_default_client

        client = get_default_client()
        assert client is not None

        close_default_client()

        # Getting client again should create new instance
        new_client = get_default_client()
        assert new_client is not client

        close_default_client()
