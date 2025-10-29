"""Pytest configuration and fixtures for testing pyeducationdata.

This module provides fixtures and helpers for mocking API responses using respx.
"""

import pytest
import respx
from httpx import Response


@pytest.fixture
def mock_api_response():
    """Fixture providing a sample API response structure."""
    return {
        "count": 100,
        "results": [
            {
                "year": 2020,
                "ncessch": "010000100277",
                "school_name": "Test Elementary School",
                "fips": 1,
                "enrollment": 500,
                "grade": 9,
            },
            {
                "year": 2020,
                "ncessch": "010000100278",
                "school_name": "Test High School",
                "fips": 1,
                "enrollment": 800,
                "grade": 9,
            },
        ],
        "next": None,
        "previous": None,
    }


@pytest.fixture
def mock_paginated_response():
    """Fixture providing paginated API responses."""

    def create_page(page_num: int, total_pages: int):
        """Create a single page of results."""
        results = [
            {
                "year": 2020,
                "ncessch": f"01000010{page_num:04d}",
                "enrollment": 500 + page_num,
            }
            for _ in range(10)
        ]

        next_url = (
            f"https://educationdata.urban.org/api/v1/test?page={page_num + 1}"
            if page_num < total_pages
            else None
        )

        return {
            "count": total_pages * 10,
            "results": results,
            "next": next_url,
            "previous": None,
        }

    return create_page


@pytest.fixture
def mock_metadata_response():
    """Fixture providing API metadata response."""
    return {
        "results": [
            {
                "endpoint_id": 1,
                "level": "schools",
                "source": "ccd",
                "topic": "enrollment",
                "years_available": [2018, 2019, 2020],
                "optional_vars": ["fips", "grade", "ncessch"],
                "required_vars": ["year"],
            },
            {
                "endpoint_id": 2,
                "level": "schools",
                "source": "ccd",
                "topic": "directory",
                "years_available": [2018, 2019, 2020],
                "optional_vars": ["fips", "ncessch", "charter"],
                "required_vars": ["year"],
            },
        ]
    }


@pytest.fixture
def mock_variables_response():
    """Fixture providing variable metadata response."""
    return {
        "results": [
            {
                "variable": "race",
                "name": "race",
                "labels": {
                    "1": "White",
                    "2": "Black or African American",
                    "3": "Hispanic or Latino",
                    "4": "Asian",
                    "5": "American Indian or Alaska Native",
                },
            },
            {
                "variable": "sex",
                "name": "sex",
                "labels": {"1": "Male", "2": "Female"},
            },
            {"variable": "enrollment", "name": "enrollment", "labels": None},
        ]
    }


@pytest.fixture
def mock_respx():
    """Fixture that sets up respx for mocking HTTP requests."""
    with respx.mock:
        yield respx


@pytest.fixture
def setup_basic_mock(mock_respx, mock_api_response):
    """Fixture that sets up a basic mock response for a common endpoint."""

    def _setup(url: str = None):
        if url is None:
            url = "https://educationdata.urban.org/api/v1/schools/ccd/enrollment/"

        route = mock_respx.get(url).mock(
            return_value=Response(
                200,
                json=mock_api_response,
            )
        )
        return route

    return _setup


@pytest.fixture
def setup_error_mock(mock_respx):
    """Fixture that sets up error responses for testing error handling."""

    def _setup(url: str, status_code: int = 404):
        route = mock_respx.get(url).mock(
            return_value=Response(status_code, json={"error": "Not found"})
        )
        return route

    return _setup


@pytest.fixture
def sample_dataframe():
    """Fixture providing a sample pandas DataFrame."""
    import pandas as pd

    return pd.DataFrame(
        {
            "year": [2020, 2020, 2020],
            "ncessch": ["010000100277", "010000100278", "010000100279"],
            "school_name": ["School A", "School B", "School C"],
            "fips": [1, 1, 1],
            "enrollment": [500, 800, 600],
            "grade": [9, 10, 11],
            "race": [1, 2, 3],
        }
    )


# Test helpers


def assert_dataframe_equal_ignore_order(df1, df2):
    """Assert that two DataFrames are equal, ignoring row order.

    Args:
        df1: First DataFrame
        df2: Second DataFrame

    Raises:
        AssertionError: If DataFrames are not equal
    """
    from pandas.testing import assert_frame_equal

    # Sort both DataFrames by all columns to normalize order
    df1_sorted = df1.sort_values(by=list(df1.columns)).reset_index(drop=True)
    df2_sorted = df2.sort_values(by=list(df2.columns)).reset_index(drop=True)

    assert_frame_equal(df1_sorted, df2_sorted)
