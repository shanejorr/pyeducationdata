"""pyeducationdata: Python package for the Urban Institute's Education Data Portal API.

This package provides convenient access to comprehensive US education data from
kindergarten through postsecondary education, covering decades of data from
multiple federal sources.

Example usage:
    >>> import pyeducationdata as ped
    >>> df = ped.get_education_data(
    ...     level='schools',
    ...     source='ccd',
    ...     topic='enrollment',
    ...     filters={'year': 2020, 'grade': 9}
    ... )

For more information, visit: https://educationdata.urban.org/
"""

from .client import get_education_data, get_education_data_summary
from .exceptions import (
    APIConnectionError,
    DataProcessingError,
    EducationDataError,
    EndpointNotFoundError,
    InvalidFilterError,
    PaginationError,
    ValidationError,
)

__version__ = "0.1.0"
__author__ = "Shane Orr"
__license__ = "MIT"

# Public API
__all__ = [
    # Main functions
    "get_education_data",
    "get_education_data_summary",
    # Exceptions
    "EducationDataError",
    "EndpointNotFoundError",
    "InvalidFilterError",
    "APIConnectionError",
    "PaginationError",
    "ValidationError",
    "DataProcessingError",
    # Metadata
    "__version__",
]
