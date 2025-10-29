"""Custom exceptions for the pyeducationdata package.

This module defines a hierarchy of exceptions used throughout the package
to provide clear, actionable error messages to users.
"""


class EducationDataError(Exception):
    """Base exception for all pyeducationdata errors.

    All custom exceptions in this package inherit from this base class,
    making it easy to catch any package-specific error.
    """
    pass


class EndpointNotFoundError(EducationDataError):
    """Raised when the specified endpoint doesn't exist.

    This typically occurs when an invalid combination of level, source,
    and topic is provided, or when the endpoint is not available in the API.
    """
    pass


class InvalidFilterError(EducationDataError):
    """Raised when a filter variable is invalid for the specified endpoint.

    This occurs when trying to filter by a variable that doesn't exist
    in the endpoint's data, or when the filter value is invalid.
    """
    pass


class APIConnectionError(EducationDataError):
    """Raised when the API request fails.

    This can occur due to network issues, API server errors, or timeouts.
    """
    pass


class PaginationError(EducationDataError):
    """Raised when pagination handling fails.

    This occurs when there's an issue iterating through paginated results,
    such as a malformed 'next' URL or unexpected response structure.
    """
    pass


class ValidationError(EducationDataError):
    """Raised when parameter validation fails.

    This occurs when required parameters are missing or when parameter
    values don't meet the expected constraints.
    """
    pass


class DataProcessingError(EducationDataError):
    """Raised when data processing or transformation fails.

    This can occur during DataFrame construction, type conversion,
    or label mapping operations.
    """
    pass
