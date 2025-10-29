"""Parameter validation utilities.

This module provides functions to validate API parameters against endpoint
metadata and provide helpful error messages for invalid inputs.
"""

from typing import Any, Optional

from .api import get_default_client
from .constants import VALID_LEVELS, VALID_STATISTICS
from .exceptions import EndpointNotFoundError, ValidationError


class EndpointValidator:
    """Validates endpoint existence and parameter compatibility.

    This class queries the API's metadata endpoints to validate that
    requested level/source/topic combinations exist and that filters
    are valid for the endpoint.
    """

    def __init__(self):
        """Initialize the endpoint validator."""
        self._endpoints_cache: Optional[list[dict[str, Any]]] = None

    def get_endpoints_metadata(self) -> list[dict[str, Any]]:
        """Retrieve endpoint metadata from the API.

        Returns:
            List of endpoint metadata dictionaries

        Raises:
            ValidationError: If metadata retrieval fails
        """
        if self._endpoints_cache is not None:
            return self._endpoints_cache

        try:
            client = get_default_client()
            metadata = client.get_metadata("endpoints")
            self._endpoints_cache = metadata.get("results", [])
            return self._endpoints_cache
        except Exception as e:
            raise ValidationError(f"Failed to retrieve endpoint metadata: {str(e)}") from e

    def validate_endpoint_exists(
        self, level: str, source: str, topic: str, subtopic: Optional[list[str]] = None
    ) -> bool:
        """Validate that an endpoint exists in the API.

        Args:
            level: API data level
            source: Data source
            topic: Data topic
            subtopic: Optional subtopic list

        Returns:
            True if endpoint exists

        Raises:
            EndpointNotFoundError: If the endpoint doesn't exist
        """
        # Basic level validation
        if level not in VALID_LEVELS:
            raise EndpointNotFoundError(
                f"Invalid level: '{level}'. Must be one of: {', '.join(VALID_LEVELS)}"
            )

        # Get endpoints metadata
        try:
            endpoints = self.get_endpoints_metadata()
        except Exception:
            # If we can't get metadata, just return True and let the API call fail
            # with its own error message
            return True

        # Search for matching endpoint
        for endpoint in endpoints:
            if (
                endpoint.get("level") == level
                and endpoint.get("source") == source
                and endpoint.get("topic") == topic
            ):
                # Basic match found
                # Could add more sophisticated subtopic checking here
                return True

        # No match found
        raise EndpointNotFoundError(
            f"Endpoint not found: level='{level}', source='{source}', topic='{topic}'. "
            f"Check the API documentation for valid combinations."
        )

    def validate_filters(
        self, filters: dict[str, Any], level: str, source: str, topic: str
    ) -> bool:
        """Validate that filter variables are valid for the endpoint.

        Args:
            filters: Dictionary of filter variables
            level: API data level
            source: Data source
            topic: Data topic

        Returns:
            True if filters are valid

        Raises:
            InvalidFilterError: If a filter variable is invalid
        """
        if not filters:
            return True

        # Get endpoint metadata
        try:
            endpoints = self.get_endpoints_metadata()
        except Exception:
            # Can't validate - assume valid
            return True

        # Find the endpoint
        endpoint_info = None
        for endpoint in endpoints:
            if (
                endpoint.get("level") == level
                and endpoint.get("source") == source
                and endpoint.get("topic") == topic
            ):
                endpoint_info = endpoint
                break

        if not endpoint_info:
            # Endpoint not found in metadata - can't validate
            return True

        # Get list of valid filter variables for this endpoint
        valid_filters = endpoint_info.get("optional_vars", []) + endpoint_info.get(
            "required_vars", []
        )

        # Check each filter
        for filter_name in filters.keys():
            if valid_filters and filter_name not in valid_filters:
                # This is a warning rather than an error, since the metadata
                # might not be complete
                print(
                    f"Warning: Filter '{filter_name}' may not be valid for this endpoint. "
                    f"Valid filters: {', '.join(valid_filters)}"
                )

        return True


def validate_level(level: str) -> str:
    """Validate and normalize level parameter.

    Args:
        level: API data level

    Returns:
        Normalized level string

    Raises:
        ValidationError: If level is invalid
    """
    level = level.lower().strip()

    if level not in VALID_LEVELS:
        raise ValidationError(
            f"Invalid level: '{level}'. Must be one of: {', '.join(VALID_LEVELS)}"
        )

    return level


def validate_source(source: str) -> str:
    """Validate and normalize source parameter.

    Args:
        source: Data source

    Returns:
        Normalized source string

    Raises:
        ValidationError: If source is obviously invalid (too short, etc.)
    """
    source = source.lower().strip()

    if len(source) < 2:
        raise ValidationError(f"Invalid source: '{source}'. Source must be at least 2 characters.")

    # Note: We don't validate against VALID_SOURCES because new sources
    # may be added to the API
    return source


def validate_statistic(stat: str) -> str:
    """Validate and normalize statistic parameter.

    Args:
        stat: Statistic type

    Returns:
        Normalized statistic string

    Raises:
        ValidationError: If statistic is invalid
    """
    stat = stat.lower().strip()

    # Normalize aliases
    if stat == "mean":
        stat = "avg"

    if stat not in VALID_STATISTICS:
        raise ValidationError(
            f"Invalid statistic: '{stat}'. Must be one of: {', '.join(VALID_STATISTICS)}"
        )

    return stat


def validate_year(year: Any) -> int:
    """Validate year parameter.

    Args:
        year: Year value

    Returns:
        Year as integer

    Raises:
        ValidationError: If year is invalid
    """
    try:
        year_int = int(year)
    except (ValueError, TypeError) as e:
        raise ValidationError(f"Invalid year: '{year}'. Must be an integer.") from e

    # Reasonable bounds for education data
    if not (1980 <= year_int <= 2030):
        raise ValidationError(
            f"Invalid year: {year_int}. Must be between 1980 and 2030. "
            "Check the API documentation for data availability."
        )

    return year_int


def validate_fips(fips: Any) -> int:
    """Validate FIPS code parameter.

    Args:
        fips: State FIPS code

    Returns:
        FIPS code as integer

    Raises:
        ValidationError: If FIPS code is invalid
    """
    try:
        fips_int = int(fips)
    except (ValueError, TypeError) as e:
        raise ValidationError(f"Invalid FIPS code: '{fips}'. Must be an integer.") from e

    # Valid FIPS codes (states and territories)
    valid_fips = list(range(1, 57)) + [60, 66, 69, 72, 78]

    if fips_int not in valid_fips:
        raise ValidationError(
            f"Invalid FIPS code: {fips_int}. "
            "Must be a valid state or territory FIPS code (1-56, 60, 66, 69, 72, 78)."
        )

    return fips_int


# Module-level singleton
_default_validator: Optional[EndpointValidator] = None


def get_default_validator() -> EndpointValidator:
    """Get or create the default endpoint validator instance.

    Returns:
        The default EndpointValidator instance
    """
    global _default_validator
    if _default_validator is None:
        _default_validator = EndpointValidator()
    return _default_validator


def validate_endpoint(
    level: str,
    source: str,
    topic: str,
    subtopic: Optional[list[str]] = None,
    filters: Optional[dict[str, Any]] = None,
) -> bool:
    """Validate an endpoint and its filters.

    This is a convenience function that uses the default validator.

    Args:
        level: API data level
        source: Data source
        topic: Data topic
        subtopic: Optional subtopic list
        filters: Optional filter dictionary

    Returns:
        True if endpoint is valid

    Raises:
        EndpointNotFoundError: If the endpoint doesn't exist
        InvalidFilterError: If filters are invalid
    """
    validator = get_default_validator()
    validator.validate_endpoint_exists(level, source, topic, subtopic)

    if filters:
        validator.validate_filters(filters, level, source, topic)

    return True
