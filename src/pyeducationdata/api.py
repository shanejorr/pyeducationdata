"""HTTP client for the Education Data Portal API.

This module provides the core HTTP client functionality using httpx for
making requests to the Education Data Portal API.
"""

import time
from typing import Any, Optional

import httpx
import pandas as pd

from .constants import (
    API_ENDPOINT,
    CSV_DOWNLOAD_URL,
    DEFAULT_HEADERS,
    DEFAULT_TIMEOUT,
    MAX_RETRIES,
)
from .exceptions import APIConnectionError, DataProcessingError
from .models import APIResponse


class APIClient:
    """HTTP client for the Education Data Portal API.

    This class handles all HTTP communication with the API, including:
    - Making GET requests with proper error handling
    - Retrying failed requests
    - Downloading CSV files
    - Converting responses to appropriate Python objects

    Attributes:
        base_url: Base URL for the API endpoint
        timeout: Request timeout in seconds
        max_retries: Maximum number of retry attempts for failed requests
        client: httpx.Client instance for connection pooling
    """

    def __init__(
        self,
        base_url: str = API_ENDPOINT,
        timeout: int = DEFAULT_TIMEOUT,
        max_retries: int = MAX_RETRIES,
    ):
        """Initialize the API client.

        Args:
            base_url: Base URL for the API (default: from constants)
            timeout: Request timeout in seconds (default: 30)
            max_retries: Maximum retry attempts (default: 3)
        """
        self.base_url = base_url
        self.timeout = timeout
        self.max_retries = max_retries
        self.client = httpx.Client(
            timeout=timeout,
            headers=DEFAULT_HEADERS,
            follow_redirects=True,
        )

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - close the client."""
        self.close()

    def close(self):
        """Close the HTTP client and release resources."""
        self.client.close()

    def get(self, url: str, params: Optional[dict[str, Any]] = None) -> dict[str, Any]:
        """Make a GET request to the API.

        This method handles retries, error checking, and response parsing.

        Args:
            url: Full URL to request
            params: Optional query parameters

        Returns:
            Parsed JSON response as a dictionary

        Raises:
            APIConnectionError: If the request fails after all retries
        """
        last_exception = None

        for attempt in range(self.max_retries):
            try:
                response = self.client.get(url, params=params)
                response.raise_for_status()
                return response.json()

            except httpx.HTTPStatusError as e:
                # HTTP error (4xx, 5xx)
                status_code = e.response.status_code
                if status_code == 404:
                    raise APIConnectionError(
                        f"Endpoint not found (404): {url}. "
                        "Check that the level/source/topic combination is valid."
                    ) from e
                elif status_code == 500:
                    raise APIConnectionError(
                        f"Server error (500): {url}. "
                        "The API encountered an internal error. Please try again later."
                    ) from e
                elif status_code == 503:
                    # Service unavailable - retry
                    last_exception = e
                    if attempt < self.max_retries - 1:
                        time.sleep(2**attempt)  # Exponential backoff
                        continue
                else:
                    raise APIConnectionError(
                        f"HTTP error {status_code}: {url}. Response: {e.response.text}"
                    ) from e

            except httpx.TimeoutException as e:
                # Timeout - retry
                last_exception = e
                if attempt < self.max_retries - 1:
                    time.sleep(2**attempt)
                    continue
                raise APIConnectionError(
                    f"Request timeout after {self.timeout} seconds: {url}"
                ) from e

            except httpx.RequestError as e:
                # Network error - retry
                last_exception = e
                if attempt < self.max_retries - 1:
                    time.sleep(2**attempt)
                    continue
                raise APIConnectionError(f"Network error: {url}. Error: {str(e)}") from e

            except ValueError as e:
                # JSON parsing error
                raise APIConnectionError(
                    f"Failed to parse JSON response from: {url}. "
                    "The API response may be malformed."
                ) from e

        # If we get here, all retries failed
        raise APIConnectionError(
            f"Request failed after {self.max_retries} attempts: {url}"
        ) from last_exception

    def get_json_response(self, url: str, params: Optional[dict[str, Any]] = None) -> APIResponse:
        """Get a JSON response and parse it into an APIResponse model.

        Args:
            url: Full URL to request
            params: Optional query parameters

        Returns:
            Parsed APIResponse object

        Raises:
            APIConnectionError: If the request fails
            DataProcessingError: If the response structure is invalid
        """
        try:
            data = self.get(url, params=params)
            return APIResponse(**data)
        except Exception as e:
            if isinstance(e, APIConnectionError):
                raise
            raise DataProcessingError(
                f"Failed to parse API response into expected structure: {str(e)}"
            ) from e

    def download_csv(
        self,
        csv_path: str,
        output_file: Optional[str] = None,
    ) -> pd.DataFrame:
        """Download a CSV file from the API.

        Args:
            csv_path: Path to the CSV file (relative to CSV base URL)
            output_file: Optional path to save the CSV file locally

        Returns:
            DataFrame containing the CSV data

        Raises:
            APIConnectionError: If the download fails
            DataProcessingError: If CSV parsing fails
        """
        url = f"{CSV_DOWNLOAD_URL}/{csv_path}"

        try:
            with self.client.stream("GET", url) as response:
                response.raise_for_status()

                if output_file:
                    # Save to file
                    with open(output_file, "wb") as f:
                        for chunk in response.iter_bytes():
                            f.write(chunk)
                    # Read from saved file
                    return pd.read_csv(output_file)
                else:
                    # Read directly into DataFrame
                    return pd.read_csv(response.iter_lines())

        except httpx.HTTPStatusError as e:
            raise APIConnectionError(
                f"Failed to download CSV from {url}: HTTP {e.response.status_code}"
            ) from e
        except httpx.RequestError as e:
            raise APIConnectionError(f"Network error downloading CSV from {url}: {str(e)}") from e
        except Exception as e:
            raise DataProcessingError(f"Failed to parse CSV data: {str(e)}") from e

    def get_metadata(self, metadata_type: str) -> dict[str, Any]:
        """Retrieve metadata from the API.

        Args:
            metadata_type: Type of metadata to retrieve
                          (e.g., 'endpoints', 'variables', 'endpoint_varlist')

        Returns:
            Metadata as a dictionary

        Raises:
            APIConnectionError: If the metadata request fails
        """
        from .constants import METADATA_ENDPOINTS

        if metadata_type not in METADATA_ENDPOINTS:
            raise ValueError(
                f"Invalid metadata type: {metadata_type}. "
                f"Valid types: {list(METADATA_ENDPOINTS.keys())}"
            )

        url = METADATA_ENDPOINTS[metadata_type]
        return self.get(url)


# Module-level client instance for convenience
_default_client: Optional[APIClient] = None


def get_default_client() -> APIClient:
    """Get or create the default API client instance.

    This provides a singleton client that can be reused across multiple
    function calls for connection pooling.

    Returns:
        The default APIClient instance
    """
    global _default_client
    if _default_client is None:
        _default_client = APIClient()
    return _default_client


def close_default_client():
    """Close and reset the default API client.

    Call this to explicitly clean up resources when done with the API.
    """
    global _default_client
    if _default_client is not None:
        _default_client.close()
        _default_client = None
