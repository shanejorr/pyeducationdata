"""Main client functions for accessing the Education Data Portal API.

This module provides the two primary user-facing functions:
- get_education_data(): Retrieve detailed records
- get_education_data_summary(): Retrieve aggregated statistics
"""

from typing import Any, Optional

import pandas as pd
from pydantic import ValidationError as PydanticValidationError

from .api import get_default_client
from .exceptions import ValidationError
from .models import EducationDataRequest, EducationDataSummaryRequest
from .pagination import paginate_results
from .utils import apply_dataframe_filters, build_endpoint_url, build_summary_url


def get_education_data(
    level: str,
    source: str,
    topic: str,
    subtopic: Optional[list[str]] = None,
    filters: Optional[dict[str, Any]] = None,
    add_labels: bool = False,
    csv: bool = False,
) -> pd.DataFrame:
    """Retrieve data from the Urban Institute Education Data Portal API.

    This is the main function for accessing education data. It handles parameter
    validation, URL construction, pagination, and data formatting automatically.

    Args:
        level: API data level. Must be one of:
            - 'schools': K-12 school-level data
            - 'school-districts': K-12 district-level data
            - 'college-university': Postsecondary institution data

        source: Data source. Common sources include:
            - 'ccd': Common Core of Data (K-12 schools and districts)
            - 'crdc': Civil Rights Data Collection (K-12 schools)
            - 'ipeds': Integrated Postsecondary Education Data System (colleges)
            - 'edfacts': State assessment data (K-12)
            - 'saipe': Poverty estimates (K-12 districts)
            - 'scorecard': College Scorecard data
            - And many more (see documentation)

        topic: Data topic. Common topics include:
            - 'directory': Basic institution information
            - 'enrollment': Student enrollment data
            - 'finance': Revenue and expenditure data
            - 'assessments': Test scores and performance metrics
            - And many more (varies by source)

        subtopic: Optional list of disaggregation parameters.
            For example, ['race', 'sex'] for enrollment broken down by
            race/ethnicity and sex. Available subtopics vary by endpoint.

        filters: Optional dictionary of query filters. Common filters:
            - 'year': int or list[int] - Academic year(s)
            - 'grade': int or list[int] - Grade level(s)
            - 'fips': int or list[int] - State FIPS code(s)
            - 'ncessch': str - Specific school ID
            - 'leaid': str - Specific district ID
            - 'unitid': int - Specific college/university ID
            Available filters vary by endpoint.

        add_labels: If True, convert integer-coded categorical variables to
            pandas Categorical dtype with descriptive labels. For example,
            convert race codes (1, 2, 3) to labels ("White", "Black", "Hispanic").
            Default: False (return raw integer codes).

        csv: If True, download the complete dataset as a CSV file instead of
            using the JSON API. This is faster for large datasets but slower
            for small filtered queries. Filters are applied client-side after
            download. Default: False (use JSON API with server-side filtering).

    Returns:
        DataFrame containing the requested data. Column names correspond to
        variable names in the API. Each row represents one observation.

    Raises:
        ValidationError: If parameters are invalid (wrong type, missing required values)
        EndpointNotFoundError: If the level/source/topic combination doesn't exist
        InvalidFilterError: If filter variables are invalid for the endpoint
        APIConnectionError: If the API request fails (network error, timeout, etc.)
        PaginationError: If pagination handling fails
        DataProcessingError: If data conversion to DataFrame fails

    Examples:
        Basic query for school enrollment:
        >>> df = get_education_data(
        ...     level='schools',
        ...     source='ccd',
        ...     topic='enrollment',
        ...     filters={'year': 2020, 'grade': 9}
        ... )

        Enrollment with demographic breakdowns:
        >>> df = get_education_data(
        ...     level='schools',
        ...     source='ccd',
        ...     topic='enrollment',
        ...     subtopic=['race', 'sex'],
        ...     filters={'year': 2020, 'grade': [9, 10, 11, 12], 'fips': 6},
        ...     add_labels=True
        ... )

        College directory data:
        >>> df = get_education_data(
        ...     level='college-university',
        ...     source='ipeds',
        ...     topic='directory',
        ...     filters={'year': 2023}
        ... )

        Large dataset via CSV:
        >>> df = get_education_data(
        ...     level='schools',
        ...     source='ccd',
        ...     topic='directory',
        ...     filters={'year': 2020},
        ...     csv=True
        ... )

    Notes:
        - The API has a 10,000 record per page limit. This function automatically
          handles pagination to retrieve all matching records.
        - For large datasets (>100,000 records), consider using csv=True for
          better performance.
        - Some endpoints require specific filters (e.g., year) to be provided.
        - Data is cached on the API side, so repeated identical queries are fast.

    See Also:
        get_education_data_summary: For aggregated statistics instead of raw data
    """
    # Validate parameters using pydantic
    try:
        request = EducationDataRequest(
            level=level,
            source=source,
            topic=topic,
            subtopic=subtopic,
            filters=filters,
            add_labels=add_labels,
            csv=csv,
        )
    except PydanticValidationError as e:
        raise ValidationError(f"Invalid parameters: {e}") from e

    # Route to CSV or JSON handler
    if request.csv:
        return _get_data_csv(request)
    else:
        return _get_data_json(request)


def _get_data_json(request: EducationDataRequest) -> pd.DataFrame:
    """Retrieve data via JSON API with pagination.

    Args:
        request: Validated request parameters

    Returns:
        DataFrame with all matching records
    """
    # Build endpoint URL
    url = build_endpoint_url(
        level=request.level,
        source=request.source,
        topic=request.topic,
        subtopic=request.subtopic,
        filters=request.filters,
    )

    # Get API client
    client = get_default_client()

    # Fetch first page
    response = client.get_json_response(url)

    # Handle pagination
    df = paginate_results(
        initial_response=response,
        fetch_next_page=lambda next_url: client.get_json_response(next_url),
        verbose=True,
    )

    # Apply labels if requested
    if request.add_labels and not df.empty:
        df = _apply_labels(df, request)

    return df


def _get_data_csv(request: EducationDataRequest) -> pd.DataFrame:
    """Retrieve data via CSV download.

    Note: CSV downloads retrieve complete datasets. Filters are applied
    client-side after download.

    Args:
        request: Validated request parameters

    Returns:
        DataFrame with filtered records
    """
    # Build CSV path (this is an approximation - may need adjustment)
    csv_path_parts = [request.level, request.source, request.topic]
    if request.subtopic:
        csv_path_parts.extend(request.subtopic)

    csv_path = "_".join(csv_path_parts) + ".csv"

    # Get API client
    client = get_default_client()

    # Download CSV
    print(f"Downloading CSV file: {csv_path}")
    df = client.download_csv(csv_path)
    print(f"Downloaded {len(df):,} records")

    # Apply filters client-side
    if request.filters:
        print("Applying filters...")
        df = apply_dataframe_filters(df, request.filters)
        print(f"After filtering: {len(df):,} records")

    # Apply labels if requested
    if request.add_labels and not df.empty:
        df = _apply_labels(df, request)

    return df


def _apply_labels(df: pd.DataFrame, request: EducationDataRequest) -> pd.DataFrame:
    """Apply descriptive labels to integer-coded categorical variables.

    This is a placeholder for label mapping functionality, which will be
    implemented in the labels.py module.

    Args:
        df: DataFrame with raw integer codes
        request: Request parameters (for identifying endpoint)

    Returns:
        DataFrame with categorical columns labeled
    """
    # TODO: Implement label mapping using metadata API
    # For now, just return the DataFrame unchanged
    # The labels.py module will provide the full implementation
    print("Label mapping not yet fully implemented - returning raw codes")
    return df


def get_education_data_summary(
    level: str,
    source: str,
    topic: str,
    stat: str,
    var: str,
    by: Optional[str | list[str]] = None,
    subtopic: Optional[list[str]] = None,
    filters: Optional[dict[str, Any]] = None,
) -> pd.DataFrame:
    """Retrieve aggregated summary statistics from the API.

    Summary endpoints provide server-side aggregation, which is much faster
    than downloading raw data and computing statistics client-side. Use this
    when you need totals, averages, or other statistics grouped by one or
    more variables.

    Args:
        level: API data level (schools, school-districts, college-university)

        source: Data source (ccd, ipeds, crdc, etc.)

        topic: Data topic (enrollment, directory, finance, etc.)

        stat: Statistic to compute. Must be one of:
            - 'sum': Sum of values
            - 'avg' or 'mean': Average (mean) value
            - 'median': Median value
            - 'max': Maximum value
            - 'min': Minimum value
            - 'count': Count of records
            - 'stddev': Standard deviation
            - 'variance': Variance

        var: Variable name to aggregate. Must be a numeric variable available
            in the endpoint (e.g., 'enrollment', 'revenue', 'expenditure').

        by: Variable(s) to group by. Can be a string for a single grouping
            variable, or a list of strings for multiple grouping variables.
            Common grouping variables include:
            - 'fips': State
            - 'year': Academic year
            - 'grade': Grade level
            - 'race': Race/ethnicity
            - 'sex': Sex/gender
            Available grouping variables vary by endpoint.

        subtopic: Optional list of disaggregation parameters (same as
            get_education_data())

        filters: Optional dictionary of query filters to subset the data
            before aggregation. Same format as get_education_data().

    Returns:
        DataFrame containing aggregated statistics. Includes one row per
        unique combination of grouping variables, plus a column with the
        computed statistic.

    Raises:
        ValidationError: If parameters are invalid
        EndpointNotFoundError: If the endpoint doesn't exist
        APIConnectionError: If the API request fails
        DataProcessingError: If data conversion fails

    Examples:
        State-level enrollment totals:
        >>> summary = get_education_data_summary(
        ...     level='schools',
        ...     source='ccd',
        ...     topic='enrollment',
        ...     stat='sum',
        ...     var='enrollment',
        ...     by='fips',
        ...     filters={'year': 2020}
        ... )

        Average enrollment by school level:
        >>> summary = get_education_data_summary(
        ...     level='schools',
        ...     source='ccd',
        ...     topic='enrollment',
        ...     stat='avg',
        ...     var='enrollment',
        ...     by='school_level',
        ...     filters={'year': 2020}
        ... )

        Multi-dimensional grouping:
        >>> summary = get_education_data_summary(
        ...     level='schools',
        ...     source='ccd',
        ...     topic='enrollment',
        ...     subtopic=['race', 'sex'],
        ...     stat='sum',
        ...     var='enrollment',
        ...     by=['fips', 'race', 'sex'],
        ...     filters={'year': 2020}
        ... )

    Notes:
        - Summary endpoints are significantly faster than downloading and
          aggregating raw data locally.
        - The 'by' parameter can include variables not in the original
          endpoint, as summary endpoints join with directory data.
        - Not all endpoints support summary statistics - this depends on
          API implementation.

    See Also:
        get_education_data: For retrieving raw data records
    """
    # Validate parameters using pydantic
    try:
        request = EducationDataSummaryRequest(
            level=level,
            source=source,
            topic=topic,
            stat=stat,
            var=var,
            by=by,
            subtopic=subtopic,
            filters=filters,
        )
    except PydanticValidationError as e:
        raise ValidationError(f"Invalid parameters: {e}") from e

    # Build summary endpoint URL
    url = build_summary_url(
        level=request.level,
        source=request.source,
        topic=request.topic,
        subtopic=request.subtopic,
        stat=request.stat,
        var=request.var,
        by=request.by,
        filters=request.filters,
    )

    # Get API client
    client = get_default_client()

    # Fetch summary data (usually fits in one page)
    response = client.get_json_response(url)

    # Handle pagination if needed (though summaries are typically small)
    df = paginate_results(
        initial_response=response,
        fetch_next_page=lambda next_url: client.get_json_response(next_url),
        verbose=True,
    )

    return df
