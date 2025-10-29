"""Pagination handling for API responses.

This module provides functionality to automatically iterate through paginated
API responses and combine them into a single DataFrame.
"""

from typing import Callable, Optional

import pandas as pd

from .constants import PAGE_SIZE_LIMIT
from .exceptions import PaginationError
from .models import APIResponse


def paginate_results(
    initial_response: APIResponse,
    fetch_next_page: Callable[[str], APIResponse],
    verbose: bool = True,
) -> pd.DataFrame:
    """Iterate through paginated API responses and combine into a DataFrame.

    The Education Data Portal API returns up to 10,000 records per page.
    This function automatically fetches all pages and combines them.

    Args:
        initial_response: First page of API response
        fetch_next_page: Function to fetch the next page given a URL
        verbose: Whether to print progress messages

    Returns:
        DataFrame containing all records from all pages

    Raises:
        PaginationError: If pagination fails

    Example:
        >>> response = client.get_json_response(url)
        >>> df = paginate_results(
        ...     response,
        ...     lambda next_url: client.get_json_response(next_url),
        ...     verbose=True
        ... )
    """
    # Accumulate DataFrames from each page
    dataframes: list[pd.DataFrame] = []

    # Calculate total pages for progress reporting
    total_records = initial_response.count
    total_pages = calculate_total_pages(total_records) if total_records else None

    # Process first page
    if initial_response.results:
        dataframes.append(pd.DataFrame(initial_response.results))

    if verbose and total_pages:
        print(f"Fetching {total_records:,} records across {total_pages} pages...")
        print(f"Page 1 of {total_pages} complete")

    # Iterate through remaining pages
    current_page = 1
    next_url = initial_response.next

    while next_url:
        try:
            response = fetch_next_page(next_url)

            if response.results:
                dataframes.append(pd.DataFrame(response.results))

            current_page += 1
            if verbose and total_pages:
                print(f"Page {current_page} of {total_pages} complete")

            next_url = response.next

        except Exception as e:
            raise PaginationError(
                f"Failed to fetch page {current_page + 1}. "
                f"Partial results ({len(dataframes)} pages) retrieved. "
                f"Error: {str(e)}"
            ) from e

    # Combine all DataFrames
    if not dataframes:
        # No results - return empty DataFrame
        return pd.DataFrame()

    try:
        combined_df = pd.concat(dataframes, ignore_index=True)

        if verbose:
            print(f"Successfully retrieved {len(combined_df):,} records")

        return combined_df

    except Exception as e:
        raise PaginationError(f"Failed to combine paginated results: {str(e)}") from e


def calculate_total_pages(total_records: Optional[int]) -> Optional[int]:
    """Calculate the total number of pages based on record count.

    Args:
        total_records: Total number of records matching the query

    Returns:
        Number of pages, or None if total_records is None

    Example:
        >>> calculate_total_pages(25000)
        3
        >>> calculate_total_pages(10000)
        1
        >>> calculate_total_pages(10001)
        2
    """
    if total_records is None:
        return None

    if total_records == 0:
        return 0

    # Calculate pages needed (ceiling division)
    return (total_records + PAGE_SIZE_LIMIT - 1) // PAGE_SIZE_LIMIT


def estimate_download_size(total_records: int, avg_record_size_kb: float = 0.5) -> str:
    """Estimate the download size for a given number of records.

    This provides users with a sense of how much data they're about to download.

    Args:
        total_records: Total number of records
        avg_record_size_kb: Estimated average size per record in KB

    Returns:
        Human-readable size estimate (e.g., "12.5 MB")

    Example:
        >>> estimate_download_size(25000)
        '12.5 MB'
    """
    size_kb = total_records * avg_record_size_kb

    if size_kb < 1024:
        return f"{size_kb:.1f} KB"
    else:
        size_mb = size_kb / 1024
        if size_mb < 1024:
            return f"{size_mb:.1f} MB"
        else:
            size_gb = size_mb / 1024
            return f"{size_gb:.1f} GB"


def suggest_csv_download(total_records: int, threshold: int = 100000) -> bool:
    """Determine if CSV download should be suggested over JSON pagination.

    Large datasets may be more efficiently downloaded as CSV files.

    Args:
        total_records: Total number of records to download
        threshold: Record count threshold for CSV recommendation

    Returns:
        True if CSV download is recommended

    Example:
        >>> suggest_csv_download(150000)
        True
        >>> suggest_csv_download(50000)
        False
    """
    return total_records > threshold


def format_progress_message(
    current_page: int,
    total_pages: int,
    records_so_far: int,
    total_records: int,
) -> str:
    """Format a progress message for multi-page downloads.

    Args:
        current_page: Current page number (1-indexed)
        total_pages: Total number of pages
        records_so_far: Number of records retrieved so far
        total_records: Total number of records expected

    Returns:
        Formatted progress string

    Example:
        >>> format_progress_message(2, 5, 20000, 45000)
        'Page 2/5 (20,000/45,000 records, 44%)'
    """
    percentage = (records_so_far / total_records * 100) if total_records > 0 else 0

    return (
        f"Page {current_page}/{total_pages} "
        f"({records_so_far:,}/{total_records:,} records, {percentage:.0f}%)"
    )


class PaginationProgress:
    """Track and display progress for paginated downloads.

    This class provides a simple way to track pagination progress and
    display informative messages to users.
    """

    def __init__(self, total_records: Optional[int] = None, verbose: bool = True):
        """Initialize pagination progress tracker.

        Args:
            total_records: Total number of records expected
            verbose: Whether to print progress messages
        """
        self.total_records = total_records
        self.total_pages = calculate_total_pages(total_records)
        self.verbose = verbose
        self.current_page = 0
        self.records_retrieved = 0

    def start(self):
        """Print initial progress message."""
        if self.verbose and self.total_records:
            print(f"Fetching {self.total_records:,} records...", end="")
            if self.total_pages and self.total_pages > 1:
                print(f" ({self.total_pages} pages)")
                # Suggest CSV if large
                if suggest_csv_download(self.total_records):
                    est_size = estimate_download_size(self.total_records)
                    print(
                        f"  Tip: For large datasets (~{est_size}), "
                        "consider using csv=True for faster downloads."
                    )
            else:
                print()

    def update(self, records_in_page: int):
        """Update progress with records from current page.

        Args:
            records_in_page: Number of records in the current page
        """
        self.current_page += 1
        self.records_retrieved += records_in_page

        if self.verbose and self.total_pages and self.total_pages > 1:
            msg = format_progress_message(
                self.current_page,
                self.total_pages,
                self.records_retrieved,
                self.total_records or self.records_retrieved,
            )
            print(f"  {msg}")

    def finish(self):
        """Print completion message."""
        if self.verbose:
            print(f"✓ Successfully retrieved {self.records_retrieved:,} records")
