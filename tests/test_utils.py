"""Tests for utility functions in utils.py."""

import pandas as pd

from pyeducationdata import utils


class TestBuildEndpointUrl:
    """Tests for build_endpoint_url function."""

    def test_basic_url_construction(self):
        """Test basic URL construction without subtopic or filters."""
        url = utils.build_endpoint_url(level="schools", source="ccd", topic="enrollment")

        assert "schools" in url
        assert "ccd" in url
        assert "enrollment" in url
        assert url.endswith("/")

    def test_url_with_subtopic(self):
        """Test URL construction with subtopic."""
        url = utils.build_endpoint_url(
            level="schools", source="ccd", topic="enrollment", subtopic=["race", "sex"]
        )

        assert "schools" in url
        assert "ccd" in url
        assert "enrollment" in url
        assert "race" in url
        assert "sex" in url

    def test_url_with_filters(self):
        """Test URL construction with query parameters."""
        url = utils.build_endpoint_url(
            level="schools",
            source="ccd",
            topic="enrollment",
            filters={"year": 2020, "grade": 9},
        )

        assert "/2020/" in url  # year goes in path, not query string
        assert "grade=9" in url
        assert "?" in url

    def test_url_with_list_filters(self):
        """Test URL construction with list-valued filters."""
        url = utils.build_endpoint_url(
            level="schools",
            source="ccd",
            topic="enrollment",
            filters={"year": 2020, "grade": [9, 10, 11]},
        )

        assert "/2020/" in url  # year goes in path, not query string
        assert "grade=9" in url
        assert "grade=10" in url
        assert "grade=11" in url


class TestBuildSummaryUrl:
    """Tests for build_summary_url function."""

    def test_basic_summary_url(self):
        """Test basic summary URL construction."""
        url = utils.build_summary_url(
            level="schools",
            source="ccd",
            topic="enrollment",
            stat="sum",
            var="enrollment",
            by=["fips"],
        )

        assert "summaries" in url
        assert "stat=sum" in url
        assert "var=enrollment" in url
        assert "by=fips" in url

    def test_summary_url_with_multiple_grouping(self):
        """Test summary URL with multiple grouping variables."""
        url = utils.build_summary_url(
            level="schools",
            source="ccd",
            topic="enrollment",
            stat="avg",
            var="enrollment",
            by=["fips", "grade"],
        )

        assert "by=fips,grade" in url or ("by=fips" in url and "grade" in url)

    def test_summary_url_with_filters(self):
        """Test summary URL with additional filters."""
        url = utils.build_summary_url(
            level="schools",
            source="ccd",
            topic="enrollment",
            stat="sum",
            var="enrollment",
            by=["fips"],
            filters={"year": 2020},
        )

        assert "/2020/" in url  # year goes in path, not query string


class TestBuildQueryString:
    """Tests for build_query_string function."""

    def test_empty_params(self):
        """Test with empty parameters."""
        query = utils.build_query_string({})
        assert query == ""

    def test_single_param(self):
        """Test with single parameter."""
        query = utils.build_query_string({"year": 2020})
        assert "year=2020" in query

    def test_multiple_params(self):
        """Test with multiple parameters."""
        query = utils.build_query_string({"year": 2020, "fips": 6})
        assert "year=2020" in query
        assert "fips=6" in query

    def test_list_param(self):
        """Test with list-valued parameter."""
        query = utils.build_query_string({"grade": [9, 10, 11]})
        assert "grade=9" in query
        assert "grade=10" in query
        assert "grade=11" in query

    def test_none_values_ignored(self):
        """Test that None values are ignored."""
        query = utils.build_query_string({"year": 2020, "fips": None})
        assert "year=2020" in query
        assert "fips" not in query


class TestNormalizeGrade:
    """Tests for normalize_grade function."""

    def test_integer_grade(self):
        """Test normalization of integer grades."""
        assert utils.normalize_grade(9) == "grade-9"
        assert utils.normalize_grade(12) == "grade-12"

    def test_string_grade(self):
        """Test normalization of string grades."""
        assert utils.normalize_grade("pk") == "grade-pk"
        assert utils.normalize_grade("PK") == "grade-pk"

    def test_already_normalized(self):
        """Test that already-normalized grades are unchanged."""
        assert utils.normalize_grade("grade-9") == "grade-9"
        assert utils.normalize_grade("grade-pk") == "grade-pk"


class TestApplyDataframeFilters:
    """Tests for apply_dataframe_filters function."""

    def test_no_filters(self, sample_dataframe):
        """Test that DataFrame is unchanged with no filters."""
        result = utils.apply_dataframe_filters(sample_dataframe, None)
        pd.testing.assert_frame_equal(result, sample_dataframe)

    def test_single_value_filter(self, sample_dataframe):
        """Test filtering with single value."""
        result = utils.apply_dataframe_filters(sample_dataframe, {"grade": 9})
        assert len(result) == 1
        assert result.iloc[0]["grade"] == 9

    def test_list_value_filter(self, sample_dataframe):
        """Test filtering with list of values."""
        result = utils.apply_dataframe_filters(sample_dataframe, {"grade": [9, 10]})
        assert len(result) == 2
        assert set(result["grade"].values) == {9, 10}

    def test_multiple_filters(self, sample_dataframe):
        """Test filtering with multiple conditions."""
        result = utils.apply_dataframe_filters(
            sample_dataframe, {"year": 2020, "fips": 1, "grade": [9, 10]}
        )
        assert len(result) == 2
        assert all(result["year"] == 2020)
        assert all(result["fips"] == 1)

    def test_nonexistent_column_ignored(self, sample_dataframe):
        """Test that filters for nonexistent columns are ignored."""
        result = utils.apply_dataframe_filters(sample_dataframe, {"nonexistent": 1})
        assert len(result) == len(sample_dataframe)


class TestParseEndpointPath:
    """Tests for parse_endpoint_path function."""

    def test_full_url_parsing(self):
        """Test parsing a full endpoint URL."""
        url = "https://educationdata.urban.org/api/v1/schools/ccd/enrollment/race/"
        parsed = utils.parse_endpoint_path(url)

        assert parsed["level"] == "schools"
        assert parsed["source"] == "ccd"
        assert parsed["topic"] == "enrollment"
        assert parsed["subtopic"] == ["race"]

    def test_partial_path_parsing(self):
        """Test parsing a partial path."""
        path = "/schools/ccd/enrollment/"
        parsed = utils.parse_endpoint_path(path)

        assert parsed["level"] == "schools"
        assert parsed["source"] == "ccd"
        assert parsed["topic"] == "enrollment"

    def test_path_with_multiple_subtopics(self):
        """Test parsing path with multiple subtopic components."""
        path = "/schools/ccd/enrollment/race/sex/"
        parsed = utils.parse_endpoint_path(path)

        assert parsed["subtopic"] == ["race", "sex"]


class TestValidateYear:
    """Tests for validate_year function."""

    def test_valid_year(self):
        """Test that valid years pass validation."""
        assert utils.validate_year(2020) is True
        assert utils.validate_year(1990) is True
        assert utils.validate_year(2025) is True

    def test_invalid_year_range(self):
        """Test that years outside valid range fail."""
        assert utils.validate_year(1900) is False
        assert utils.validate_year(2050) is False

    def test_invalid_year_type(self):
        """Test that non-numeric years fail."""
        assert utils.validate_year("invalid") is False
        assert utils.validate_year(None) is False
