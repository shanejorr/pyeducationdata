"""Pydantic models for parameter validation.

This module defines data models using pydantic v2 for type-safe parameter
validation and data structure definitions.
"""

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field, field_validator


class EducationDataRequest(BaseModel):
    """Model for get_education_data() parameters.

    This model validates and normalizes all parameters for the main
    data retrieval function.
    """

    level: Literal["schools", "school-districts", "college-university"] = Field(
        ...,
        description="API data level (schools, school-districts, or college-university)",
    )
    source: str = Field(
        ...,
        description="API data source (e.g., ccd, ipeds, crdc)",
        min_length=2,
    )
    topic: str = Field(
        ...,
        description="API data topic (e.g., enrollment, directory, finance)",
        min_length=2,
    )
    subtopic: Optional[list[str]] = Field(
        default=None,
        description="Optional grouping parameters (e.g., ['race', 'sex'])",
    )
    filters: Optional[dict[str, Any]] = Field(
        default=None,
        description="Query filters (e.g., {'year': 2020, 'grade': 9})",
    )
    add_labels: bool = Field(
        default=False,
        description="Convert integer codes to descriptive labels",
    )
    csv: bool = Field(
        default=False,
        description="Download full CSV instead of using JSON API",
    )

    @field_validator("source", "topic")
    @classmethod
    def lowercase_strings(cls, v: str) -> str:
        """Convert source and topic to lowercase for consistency."""
        return v.lower().strip()

    @field_validator("subtopic")
    @classmethod
    def lowercase_subtopic(cls, v: Optional[list[str]]) -> Optional[list[str]]:
        """Convert subtopic elements to lowercase for consistency."""
        if v is not None:
            return [item.lower().strip() for item in v]
        return v

    @field_validator("filters")
    @classmethod
    def normalize_filters(cls, v: Optional[dict[str, Any]]) -> Optional[dict[str, Any]]:
        """Normalize filter values.

        Converts single values to lists where appropriate, and ensures
        consistent formatting.
        """
        if v is None:
            return None

        normalized = {}
        for key, value in v.items():
            # Convert keys to lowercase
            key = key.lower().strip()

            # Convert single values to lists for consistency in URL building
            # (though we'll handle both in the URL builder)
            if isinstance(value, (list, tuple)):
                normalized[key] = list(value)
            else:
                normalized[key] = value

        return normalized

    model_config = {"extra": "forbid"}  # Raise error for unexpected fields


class EducationDataSummaryRequest(BaseModel):
    """Model for get_education_data_summary() parameters.

    This model validates and normalizes all parameters for the summary
    statistics function.
    """

    level: Literal["schools", "school-districts", "college-university"] = Field(
        ...,
        description="API data level",
    )
    source: str = Field(
        ...,
        description="API data source",
        min_length=2,
    )
    topic: str = Field(
        ...,
        description="API data topic",
        min_length=2,
    )
    subtopic: Optional[list[str]] = Field(
        default=None,
        description="Optional grouping parameters",
    )
    stat: Literal["sum", "avg", "mean", "median", "max", "min", "count", "stddev", "variance"] = (
        Field(
            ...,
            description="Statistic to compute",
        )
    )
    var: str = Field(
        ...,
        description="Variable to aggregate",
        min_length=1,
    )
    by: Optional[str | list[str]] = Field(
        default=None,
        description="Variables to group by",
    )
    filters: Optional[dict[str, Any]] = Field(
        default=None,
        description="Query filters",
    )

    @field_validator("source", "topic", "var")
    @classmethod
    def lowercase_strings(cls, v: str) -> str:
        """Convert strings to lowercase for consistency."""
        return v.lower().strip()

    @field_validator("subtopic")
    @classmethod
    def lowercase_subtopic(cls, v: Optional[list[str]]) -> Optional[list[str]]:
        """Convert subtopic elements to lowercase."""
        if v is not None:
            return [item.lower().strip() for item in v]
        return v

    @field_validator("by")
    @classmethod
    def normalize_by(cls, v: Optional[str | list[str]]) -> Optional[list[str]]:
        """Convert 'by' parameter to list format."""
        if v is None:
            return None
        if isinstance(v, str):
            return [v.lower().strip()]
        return [item.lower().strip() for item in v]

    @field_validator("filters")
    @classmethod
    def normalize_filters(cls, v: Optional[dict[str, Any]]) -> Optional[dict[str, Any]]:
        """Normalize filter values."""
        if v is None:
            return None

        normalized = {}
        for key, value in v.items():
            key = key.lower().strip()
            if isinstance(value, (list, tuple)):
                normalized[key] = list(value)
            else:
                normalized[key] = value

        return normalized

    model_config = {"extra": "forbid"}


class EndpointInfo(BaseModel):
    """Metadata about an API endpoint.

    This model stores information about endpoint structure and availability,
    typically retrieved from the API's metadata endpoints.
    """

    endpoint_id: Optional[int] = None
    level: str
    source: str
    topic: str
    subtopic: Optional[list[str]] = None
    years_available: Optional[list[int]] = None
    optional_vars: Optional[list[str]] = None
    required_vars: Optional[list[str]] = None
    main_filters: Optional[list[str]] = None
    csv_available: bool = False

    model_config = {"extra": "allow"}  # Allow additional metadata fields


class APIResponse(BaseModel):
    """Model for API JSON response structure.

    The Education Data Portal API returns responses with a consistent
    structure including results, count, and pagination URLs.
    """

    results: list[dict[str, Any]] = Field(
        ...,
        description="Array of data records",
    )
    count: Optional[int] = Field(
        default=None,
        description="Total number of records matching the query",
    )
    next: Optional[str] = Field(
        default=None,
        description="URL for the next page of results",
    )
    previous: Optional[str] = Field(
        default=None,
        description="URL for the previous page of results",
    )

    model_config = {"extra": "allow"}  # Allow additional fields from API
