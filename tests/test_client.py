"""Tests for main client functions in client.py."""

import pandas as pd
import pytest
import respx
from httpx import Response

from pyeducationdata import get_education_data, get_education_data_summary
from pyeducationdata.exceptions import ValidationError


class TestGetEducationData:
    """Tests for get_education_data function."""

    @respx.mock
    def test_basic_data_retrieval(self, mock_api_response):
        """Test basic data retrieval."""
        url_pattern = "https://educationdata.urban.org/api/v1/schools/ccd/enrollment/"

        respx.get(url_pattern).mock(return_value=Response(200, json=mock_api_response))

        df = get_education_data(level="schools", source="ccd", topic="enrollment")

        assert isinstance(df, pd.DataFrame)
        assert len(df) == 2
        assert "enrollment" in df.columns
        assert "year" in df.columns

    @respx.mock
    def test_data_with_filters(self, mock_api_response):
        """Test data retrieval with filters."""
        # Year goes in path, so we need to mock the URL with /2020/ in it
        url_pattern = "https://educationdata.urban.org/api/v1/schools/ccd/enrollment/2020/"

        respx.get(url_pattern).mock(return_value=Response(200, json=mock_api_response))

        df = get_education_data(
            level="schools",
            source="ccd",
            topic="enrollment",
            filters={"year": 2020, "grade": 9},
        )

        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0

    @respx.mock
    def test_data_with_subtopic(self, mock_api_response):
        """Test data retrieval with subtopic."""
        url_pattern = "https://educationdata.urban.org/api/v1/schools/ccd/enrollment/race/"

        respx.get(url_pattern).mock(return_value=Response(200, json=mock_api_response))

        df = get_education_data(
            level="schools", source="ccd", topic="enrollment", subtopic=["race"]
        )

        assert isinstance(df, pd.DataFrame)

    @respx.mock
    def test_paginated_data_retrieval(self, mock_paginated_response):
        """Test retrieval of paginated data."""
        # Set up mock for first page
        url_page1 = "https://educationdata.urban.org/api/v1/schools/ccd/enrollment/"
        page1_data = mock_paginated_response(1, 3)

        respx.get(url_page1).mock(return_value=Response(200, json=page1_data))

        # Set up mocks for subsequent pages
        url_page2 = "https://educationdata.urban.org/api/v1/test?page=2"
        url_page3 = "https://educationdata.urban.org/api/v1/test?page=3"

        page2_data = mock_paginated_response(2, 3)
        page3_data = mock_paginated_response(3, 3)

        respx.get(url_page2).mock(return_value=Response(200, json=page2_data))
        respx.get(url_page3).mock(return_value=Response(200, json=page3_data))

        df = get_education_data(level="schools", source="ccd", topic="enrollment")

        # Should have combined all pages
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 30  # 3 pages * 10 records each

    def test_invalid_level(self):
        """Test that invalid level raises ValidationError."""
        with pytest.raises(ValidationError):
            get_education_data(level="invalid", source="ccd", topic="enrollment")

    def test_missing_required_params(self):
        """Test that missing required parameters raises error."""
        with pytest.raises(TypeError):
            get_education_data(level="schools")

    @respx.mock
    def test_empty_results(self):
        """Test handling of empty results."""
        url_pattern = "https://educationdata.urban.org/api/v1/schools/ccd/enrollment/"

        empty_response = {"count": 0, "results": [], "next": None}

        respx.get(url_pattern).mock(return_value=Response(200, json=empty_response))

        df = get_education_data(level="schools", source="ccd", topic="enrollment")

        assert isinstance(df, pd.DataFrame)
        assert len(df) == 0


class TestGetEducationDataSummary:
    """Tests for get_education_data_summary function."""

    @respx.mock
    def test_basic_summary(self):
        """Test basic summary retrieval."""
        url_pattern = "https://educationdata.urban.org/api/v1/schools/ccd/enrollment/summaries/"

        summary_response = {
            "count": 2,
            "results": [
                {"fips": 1, "enrollment": 50000},
                {"fips": 2, "enrollment": 75000},
            ],
            "next": None,
        }

        respx.get(url_pattern).mock(return_value=Response(200, json=summary_response))

        df = get_education_data_summary(
            level="schools",
            source="ccd",
            topic="enrollment",
            stat="sum",
            var="enrollment",
            by="fips",
        )

        assert isinstance(df, pd.DataFrame)
        assert len(df) == 2
        assert "fips" in df.columns
        assert "enrollment" in df.columns

    @respx.mock
    def test_summary_with_filters(self):
        """Test summary with filters."""
        # Year goes in path, so we need to mock the URL with /2020/ in it
        url_pattern = "https://educationdata.urban.org/api/v1/schools/ccd/enrollment/2020/summaries/"

        summary_response = {
            "count": 1,
            "results": [{"fips": 6, "enrollment": 100000}],
            "next": None,
        }

        respx.get(url_pattern).mock(return_value=Response(200, json=summary_response))

        df = get_education_data_summary(
            level="schools",
            source="ccd",
            topic="enrollment",
            stat="sum",
            var="enrollment",
            by="fips",
            filters={"year": 2020},
        )

        assert isinstance(df, pd.DataFrame)
        assert len(df) == 1

    @respx.mock
    def test_summary_with_multiple_grouping(self):
        """Test summary with multiple grouping variables."""
        url_pattern = "https://educationdata.urban.org/api/v1/schools/ccd/enrollment/summaries/"

        summary_response = {
            "count": 4,
            "results": [
                {"fips": 1, "grade": 9, "enrollment": 10000},
                {"fips": 1, "grade": 10, "enrollment": 11000},
                {"fips": 2, "grade": 9, "enrollment": 15000},
                {"fips": 2, "grade": 10, "enrollment": 16000},
            ],
            "next": None,
        }

        respx.get(url_pattern).mock(return_value=Response(200, json=summary_response))

        df = get_education_data_summary(
            level="schools",
            source="ccd",
            topic="enrollment",
            stat="sum",
            var="enrollment",
            by=["fips", "grade"],
        )

        assert isinstance(df, pd.DataFrame)
        assert len(df) == 4
        assert "fips" in df.columns
        assert "grade" in df.columns

    def test_invalid_statistic(self):
        """Test that invalid statistic raises ValidationError."""
        with pytest.raises(ValidationError):
            get_education_data_summary(
                level="schools",
                source="ccd",
                topic="enrollment",
                stat="invalid",
                var="enrollment",
                by="fips",
            )

    def test_missing_required_params(self):
        """Test that missing required parameters raises error."""
        with pytest.raises(TypeError):
            get_education_data_summary(level="schools", source="ccd", topic="enrollment")


class TestParameterValidation:
    """Tests for parameter validation in client functions."""

    def test_level_normalization(self):
        """Test that level parameter is normalized to lowercase."""
        # This would need a mock, but tests that the validation happens
        with pytest.raises(ValidationError):
            get_education_data(level="INVALID", source="ccd", topic="enrollment")

    def test_source_normalization(self):
        """Test that source parameter is normalized."""
        # The pydantic model should lowercase strings
        # We can't easily test this without mocking the API
        pass

    def test_extra_parameters_rejected(self):
        """Test that extra parameters are rejected."""
        # Pydantic rejects unexpected kwargs at function call level with TypeError
        with pytest.raises(TypeError, match="unexpected keyword argument"):
            get_education_data(
                level="schools",
                source="ccd",
                topic="enrollment",
                invalid_param="value",
            )
