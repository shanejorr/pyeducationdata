"""Utility functions for URL construction and data processing.

This module provides helper functions for building API URLs, processing
filters, and other common operations.
"""

from typing import Any, Optional
from urllib.parse import urlencode

from .constants import API_ENDPOINT


def build_endpoint_url(
    level: str,
    source: str,
    topic: str,
    subtopic: Optional[list[str]] = None,
    filters: Optional[dict[str, Any]] = None,
) -> str:
    """Build a URL for a data endpoint.

    Constructs URLs following the API pattern:
    /api/v1/{level}/{source}/{topic}/{year}/{subtopic}/

    Args:
        level: API data level (schools, school-districts, college-university)
        source: Data source (ccd, ipeds, crdc, etc.)
        topic: Data topic (enrollment, directory, finance, etc.)
        subtopic: Optional list of subtopic components (e.g., ['grade-9'], ['race', 'sex'])
        filters: Optional dictionary of query parameters (year is extracted and added to path)

    Returns:
        Complete URL for the endpoint

    Example:
        >>> build_endpoint_url('schools', 'ccd', 'enrollment', ['grade-9'], {'year': 2020, 'fips': 6})
        'https://educationdata.urban.org/api/v1/schools/ccd/enrollment/2020/grade-9/?fips=6'
    """
    # Build the base path
    path_parts = [API_ENDPOINT, level, source, topic]

    # Extract year from filters and add to path BEFORE subtopics
    year = None
    remaining_filters = {}

    if filters:
        # Make a copy of filters to avoid modifying the original
        filters_copy = filters.copy()
        year = filters_copy.pop('year', None)
        remaining_filters = filters_copy

    # Add year to path if provided (as a single value)
    if year is not None:
        if isinstance(year, (list, tuple)):
            # If year is a list with one element, use that element
            if len(year) == 1:
                year = year[0]
            else:
                # For multiple years, keep as query parameter (though API may not support this)
                remaining_filters['year'] = year
                year = None

        if year is not None:
            path_parts.append(str(year))

    # Add subtopic AFTER year
    if subtopic:
        path_parts.extend(subtopic)

    # Join path parts and ensure trailing slash
    url = "/".join(path_parts)
    if not url.endswith("/"):
        url += "/"

    # Add remaining query parameters if provided
    if remaining_filters:
        query_string = build_query_string(remaining_filters)
        if query_string:
            url += "?" + query_string

    return url


def build_summary_url(
    level: str,
    source: str,
    topic: str,
    subtopic: Optional[list[str]] = None,
    stat: Optional[str] = None,
    var: Optional[str] = None,
    by: Optional[list[str]] = None,
    filters: Optional[dict[str, Any]] = None,
) -> str:
    """Build a URL for a summary endpoint.

    Summary endpoints follow the pattern:
    /api/v1/{level}/{source}/{topic}/{year}/{subtopic}/summaries/

    Args:
        level: API data level
        source: Data source
        topic: Data topic
        subtopic: Optional list of subtopic components
        stat: Statistic to compute (sum, avg, median, etc.)
        var: Variable to aggregate
        by: Variables to group by
        filters: Optional dictionary of query parameters (year extracted to path)

    Returns:
        Complete URL for the summary endpoint

    Example:
        >>> build_summary_url('schools', 'ccd', 'enrollment',
        ...                   subtopic=['grade-99'], stat='sum', var='enrollment', by=['fips'],
        ...                   filters={'year': 2020})
        'https://educationdata.urban.org/api/v1/schools/ccd/enrollment/2020/grade-99/summaries/?stat=sum&var=enrollment&by=fips'
    """
    # Build the base path
    path_parts = [API_ENDPOINT, level, source, topic]

    # Extract year from filters and add to path BEFORE subtopics
    year = None
    remaining_filters = {}

    if filters:
        # Make a copy of filters to avoid modifying the original
        filters_copy = filters.copy()
        year = filters_copy.pop('year', None)
        remaining_filters = filters_copy

    # Add year to path if provided (as a single value)
    if year is not None:
        if isinstance(year, (list, tuple)):
            # If year is a list with one element, use that element
            if len(year) == 1:
                year = year[0]
            else:
                # For multiple years, keep as query parameter
                remaining_filters['year'] = year
                year = None

        if year is not None:
            path_parts.append(str(year))

    # Add subtopic AFTER year
    if subtopic:
        path_parts.extend(subtopic)

    # Add 'summaries' endpoint
    path_parts.append("summaries")

    # Join path parts and ensure trailing slash
    url = "/".join(path_parts)
    if not url.endswith("/"):
        url += "/"

    # Build query parameters
    params = {}

    if stat:
        params["stat"] = stat
    if var:
        params["var"] = var
    if by:
        # Join multiple 'by' values with comma
        params["by"] = ",".join(by) if isinstance(by, list) else by

    # Add remaining filters
    if remaining_filters:
        params.update(remaining_filters)

    # Add query parameters to URL
    if params:
        query_string = build_query_string(params)
        url += "?" + query_string

    return url


def build_csv_url(
    level: str,
    source: str,
    topic: str,
    subtopic: Optional[list[str]] = None,
) -> str:
    """Build a URL for CSV download.

    CSV downloads follow the pattern:
    https://educationdata.urban.org/csv/{file_path}

    Note: The exact CSV file path structure may vary. This is a best-effort
    construction that may need adjustment based on API documentation.

    Args:
        level: API data level
        source: Data source
        topic: Data topic
        subtopic: Optional list of subtopic components

    Returns:
        Approximate URL for CSV download
    """
    from .constants import CSV_DOWNLOAD_URL

    # Build the file path
    path_parts = [level, source, topic]

    if subtopic:
        path_parts.extend(subtopic)

    # Join with underscores (common CSV naming convention)
    file_name = "_".join(path_parts) + ".csv"

    return f"{CSV_DOWNLOAD_URL}/{file_name}"


def build_query_string(params: dict[str, Any]) -> str:
    """Build a URL query string from a parameters dictionary.

    Handles various parameter types including lists, which are converted
    to comma-separated values or repeated parameters as appropriate.

    Args:
        params: Dictionary of query parameters

    Returns:
        Encoded query string (without leading '?')

    Example:
        >>> build_query_string({'year': 2020, 'grade': [9, 10, 11]})
        'year=2020&grade=9&grade=10&grade=11'
    """
    if not params:
        return ""

    # Process parameters
    query_parts = []

    for key, value in params.items():
        if value is None:
            continue

        if isinstance(value, (list, tuple)):
            # For list values, create separate key=value pairs for each item
            for item in value:
                query_parts.append((key, str(item)))
        else:
            query_parts.append((key, str(value)))

    return urlencode(query_parts)


def normalize_grade(grade: Any) -> str:
    """Normalize grade values to API-expected format.

    The API expects grades in specific formats like 'grade-9' or 'grade-pk'.

    Args:
        grade: Grade value (int, str, or special value)

    Returns:
        Normalized grade string

    Example:
        >>> normalize_grade(9)
        'grade-9'
        >>> normalize_grade('pk')
        'grade-pk'
        >>> normalize_grade('grade-12')
        'grade-12'
    """
    # Convert to string
    grade_str = str(grade).lower().strip()

    # If it already starts with 'grade-', return as-is
    if grade_str.startswith("grade-"):
        return grade_str

    # Otherwise, prepend 'grade-'
    return f"grade-{grade_str}"


def apply_dataframe_filters(
    df: "pd.DataFrame",  # noqa: F821
    filters: Optional[dict[str, Any]] = None,
) -> "pd.DataFrame":  # noqa: F821
    """Apply filters to a DataFrame.

    This is used when downloading CSV files, where filtering must be done
    client-side after retrieving the full dataset.

    Args:
        df: DataFrame to filter
        filters: Dictionary of column: value filters

    Returns:
        Filtered DataFrame

    Example:
        >>> df = apply_dataframe_filters(df, {'year': 2020, 'grade': [9, 10, 11, 12]})
    """
    if not filters:
        return df


    filtered_df = df.copy()

    for column, value in filters.items():
        if column not in filtered_df.columns:
            # Skip filters for columns that don't exist
            continue

        if isinstance(value, (list, tuple)):
            # Filter to rows where column value is in the list
            filtered_df = filtered_df[filtered_df[column].isin(value)]
        else:
            # Filter to rows where column value equals the value
            filtered_df = filtered_df[filtered_df[column] == value]

    return filtered_df


def parse_endpoint_path(url: str) -> dict[str, Any]:
    """Parse an endpoint URL to extract level, source, topic, and subtopic.

    This is useful for analyzing API URLs or reverse-engineering endpoint structure.

    Args:
        url: Full or partial API endpoint URL

    Returns:
        Dictionary with parsed components

    Example:
        >>> parse_endpoint_path('/api/v1/schools/ccd/enrollment/race/')
        {'level': 'schools', 'source': 'ccd', 'topic': 'enrollment', 'subtopic': ['race']}
    """
    # Remove base URL if present
    if API_ENDPOINT in url:
        url = url.replace(API_ENDPOINT, "")

    # Remove leading/trailing slashes and split
    parts = url.strip("/").split("/")

    # Remove 'api' and version if present
    if parts and parts[0] == "api":
        parts = parts[1:]
    if parts and parts[0].startswith("v"):
        parts = parts[1:]

    result: dict[str, Any] = {}

    if len(parts) >= 1:
        result["level"] = parts[0]
    if len(parts) >= 2:
        result["source"] = parts[1]
    if len(parts) >= 3:
        result["topic"] = parts[2]
    if len(parts) >= 4:
        result["subtopic"] = parts[3:]

    return result


def validate_year(year: Any) -> bool:
    """Validate that a year value is reasonable.

    Args:
        year: Year value to validate

    Returns:
        True if valid, False otherwise
    """
    try:
        year_int = int(year)
        # Education data typically ranges from 1980 to present + 1 year
        return 1980 <= year_int <= 2030
    except (ValueError, TypeError):
        return False
