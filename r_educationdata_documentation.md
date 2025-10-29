# educationdata R Package: Complete Technical Analysis

The Urban Institute's educationdata R package provides programmatic access to the Education Data Portal API, serving as a well-designed reference implementation for API client packages. This comprehensive analysis covers all aspects needed to create a modern Python equivalent.

## Core functionality and API design

The package exposes **two primary public functions** that serve as the complete user-facing API. The main function `get_education_data()` retrieves detailed records from education datasets, while `get_education_data_summary()` provides pre-aggregated statistics. This minimalist API design reduces cognitive load while offering powerful functionality through parameter combinations.

### Complete function signature: get_education_data()

The primary function signature demonstrates thoughtful parameter design with clear required vs optional arguments:

```r
get_education_data(
  level,              # Required: 'schools', 'school-districts', 'college-university'
  source,             # Required: 'ccd', 'ipeds', 'crdc', 'edfacts', etc.
  topic,              # Required: 'enrollment', 'directory', 'finance', etc.
  subtopic = NULL,    # Optional: list('race', 'sex') for disaggregation
  filters = NULL,     # Optional: named list for filtering (year, grade, fips, etc.)
  add_labels = FALSE, # Optional: convert integer codes to factor labels
  csv = FALSE,        # Optional: download full CSV vs paginated JSON
  verbose = TRUE      # Optional: show progress messages (added v0.1.4)
)
```

**Parameter types and validation**: The function accepts character strings for required parameters, optional lists for subtopic and filters, and boolean flags for behavior modification. The package validates all parameters against API metadata before making requests, providing immediate feedback on invalid combinations rather than cryptic HTTP errors.

**Return value**: Always returns a standard R data.frame with columns representing endpoint variables and rows containing observations. This consistency makes the package compatible with all R data analysis workflows, whether base R, tidyverse, or data.table approaches.

### Complete function signature: get_education_data_summary()

The secondary function provides aggregated statistics:

```r
get_education_data_summary(
  level,              # Required: same as get_education_data()
  source,             # Required: same as get_education_data()
  topic,              # Required: same as get_education_data()
  subtopic = NULL,    # Optional: varies by endpoint
  stat,               # Required: 'sum', 'avg', 'count', 'median', 'min', 'max', 'stddev', 'variance'
  var,                # Required: variable name to aggregate
  by,                 # Required: grouping variable(s) - string or vector
  filters = NULL      # Optional: same as get_education_data()
)
```

**Key distinction**: Summary endpoints offload aggregation to the server, dramatically improving performance for statistical queries over large datasets. Rather than downloading millions of records to calculate state-level totals, the API computes aggregates and returns only summary results.

## Technical implementation deep dive

### Pagination mechanism

The package implements **automatic transparent pagination** to handle the API's 10,000 record per-page limit. The implementation follows a straightforward pattern that Python developers can directly translate:

**API response structure** contains three key fields:
- `count`: Total records available matching the query
- `results`: Array of records for current page (up to 10,000)
- `next`: URL for next page or null when complete

**Pagination algorithm**:
1. Make initial API request with query parameters
2. Parse response to extract `count` and calculate total pages needed
3. Extract `results` data frame from first page
4. Check if `next` URL exists
5. While `next` is not null:
   - Fetch next page using the provided URL
   - Extract `results` from response
   - Append to accumulated data frame using `rbind` or `bind_rows`
   - Update `next` from response
6. Return complete combined data frame

**Python translation**: This maps cleanly to Python using requests and pandas. The key is maintaining state through the pagination loop and efficiently concatenating DataFrames (using `pd.concat()` with a list accumulator rather than repeated concatenation).

### Data type conversion system

The package handles **JSON to R type conversion** through jsonlite's automatic type inference, supplemented by metadata-driven transformations:

**Automatic conversions from JSON**:
- JSON integers → R `int` (year: 2008, 2009)
- JSON strings → R `chr` (ncessch: "340606000122")
- JSON numbers → R `num` (handles large numeric IDs with proper precision)
- JSON nulls → R `NA` with appropriate type

**Factor conversion with add_labels=TRUE**: When enabled, the package queries the API metadata endpoints (`/api/v1/api-variables` and `/api/v1/api-endpoint-varlist`) to retrieve label mappings. It then converts integer-coded categorical variables to R factors with descriptive level names. For example, a `race` column with values 1, 2, 3 becomes a Factor with levels "White", "Black", "Hispanic", etc.

**Python equivalent**: Use pandas' categorical dtype for labeled variables. Query metadata endpoints to get label mappings, then create `pd.Categorical` objects with proper categories and ordering. Type hints should specify `pd.DataFrame` return types with optional schema validation using pandera or similar.

### Label addition architecture

The **add_labels parameter** triggers a sophisticated metadata integration process:

**Implementation flow**:
1. After retrieving raw data, identify which columns are coded categorical variables
2. Query API metadata endpoints to retrieve label definitions for the specific endpoint
3. Create mapping dictionaries from integer codes to string labels
4. Apply factor conversion using R's `factor()` function with explicit levels
5. Preserve original integer codes as underlying factor values for efficient operations

**Design rationale**: Labels remain optional (defaulting to FALSE) because they increase memory usage and can complicate certain analyses. Researchers working with large datasets often prefer raw codes for performance, adding labels only for final presentation or specific analyses.

**Python translation**: Implement as a post-processing step after retrieving data. Create a `LabelMapper` class that caches metadata queries and provides efficient label application. Consider offering both in-place labeling and a separate method returning a labeled copy for flexibility.

### Caching strategy (or lack thereof)

The package implements **no built-in caching mechanism**. Research found no references to memoise, cachem, or other R caching packages. This design choice reflects several considerations:

**Rationale for no caching**:
- Data updates regularly on the portal (new academic years, corrections)
- Fresh data preferred over potentially stale cached results
- CSV download option serves as an alternative for static/historical datasets
- Simplifies package maintenance and reduces dependencies
- Avoids cache invalidation complexity

**CSV as implicit caching**: The `csv=TRUE` parameter downloads complete datasets as CSV files, which users can save locally for repeated analysis. This manual caching approach gives users full control over data freshness vs performance trade-offs.

**Python recommendation**: Consider offering optional caching using requests-cache or similar, but make it **opt-in** rather than default behavior. Document clearly how to enable caching for development/testing versus production use. Allow cache TTL configuration so users control data freshness.

### Error handling patterns

The package implements **multi-layered error handling** with informative user-facing messages:

**Validation layer** (before API calls):
- Validates level, source, topic against allowed values
- Checks endpoint existence via metadata API
- Validates filter variables against endpoint schema
- Provides immediate feedback on typos or invalid combinations

**HTTP error handling**:
- Checks response status codes (404, 500, 503, 504)
- Handles network failures gracefully
- Detects timeout conditions
- Provides context-specific error messages referencing the specific endpoint and parameters

**Error message philosophy**: Uses `stop()` for fatal errors that prevent continuation, `warning()` for deprecated features (e.g., `by` → `subtopic` transition), and optional `message()` calls controlled by the `verbose` parameter for informational output.

**Example error patterns from related Stata code**:
```stata
"Error: You must enter the complete name of a dataset..."
"Error: The option you selected was invalid. The three options are..."
"Error: The name of the category is correct, but the dataset you chose is not."
```

**Python translation**: Use custom exception classes inheriting from appropriate base exceptions:
- `EducationDataError` (base exception)
- `EndpointNotFoundError` (invalid level/source/topic combination)
- `InvalidFilterError` (filter variable doesn't exist for endpoint)
- `APIConnectionError` (network/HTTP failures)

Use exception chaining (`raise ... from ...`) to preserve underlying error context while providing user-friendly messages.

### Progress indication system

The package implements **simple text-based progress reporting** controlled by the `verbose` parameter (added in version 0.1.4):

**Progress information displayed**:
- Initial message indicating data fetch is starting
- Current page number and total pages (calculated from record count)
- Endpoint information when multiple endpoints are queried
- Total records being fetched
- Suggestion to use CSV option if pagination is slow

**Implementation approach**: Uses R's `message()` or `cat()` functions to write to console, not a formal progress bar object. The Stata implementation shows the pattern:
```stata
printf("Getting data from %s, endpoint %s of %s (%s records).\n", 
       url, endpoint_num, total_endpoints, record_count)
printf("Endpoint %s of %s: On page %s of %s\n", 
       endpoint_num, total_endpoints, current_page, total_pages)
```

**Python translation**: Use `tqdm` for modern progress bars when verbose=True, or Rich's progress display for more sophisticated output. Provide clean output that shows:
- Overall progress bar for multi-page downloads
- Current page / total pages
- Records retrieved so far
- Estimated time remaining for large downloads

Ensure progress output goes to stderr (not stdout) so it doesn't interfere with data pipelines that capture stdout.

## Internal architecture and design patterns

### Functional programming paradigm

The package follows a **pure functional design** rather than object-oriented architecture. There are no custom S3 or S4 classes; functions operate on standard R data structures and return standard data.frames. This approach minimizes abstraction overhead and maximizes compatibility with the R ecosystem.

### Key architectural patterns

**Dispatcher pattern**: The main `get_education_data()` function acts as a router:
```r
get_education_data <- function(..., csv = FALSE) {
  # Validate inputs first
  validated_args <- validate_function_args(...)
  
  # Route based on download method
  if (csv) {
    return(get_education_data_csv(...))
  } else {
    return(get_education_data_json(...))
  }
}
```

**Metadata-driven validation**: Rather than hardcoding endpoint lists, the package queries API metadata at runtime. This creates a self-updating system that automatically supports new data years and endpoints as the API evolves.

**Graceful deprecation**: The package maintains backward compatibility while evolving the API. The `by` parameter was soft-deprecated in favor of `subtopic` using a warning message and automatic parameter mapping, giving users time to update code without breaking existing scripts.

**Separation of concerns**: The codebase separates:
- User-facing API (`get_education_data.R`, `get_education_data_summary.R`)
- Validation logic (`validate_function_args.R`)
- HTTP communication and JSON processing
- CSV download and filtering
- URL construction utilities
- Label mapping functionality

### Code organization structure

Based on analysis, the R/ directory contains approximately **13 source files**:

**Main API files**:
- `get_education_data.R` - Primary public function
- `get_education_data_summary.R` - Summary statistics function

**Internal implementation files**:
- `get_education_data_json.R` - JSON endpoint handler with pagination
- `get_education_data_csv.R` - CSV download handler
- `get_endpoint_info.R` - Metadata retrieval and endpoint discovery
- `validate_function_args.R` - Input validation against API metadata
- `build_endpoint_url.R` - URL construction with proper encoding
- `apply_filters.R` - Filter application logic
- `add_labels.R` - Factor conversion with label mapping
- `utils.R` - Shared utility functions
- Additional helpers for specific data transformations

**Python equivalent structure**:
```
educationdata/
├── __init__.py           # Public API exports
├── api.py                # Main get_education_data() function
├── summary.py            # get_education_data_summary() function
├── client.py             # HTTP client wrapper around requests
├── metadata.py           # Metadata fetching and caching
├── validation.py         # Parameter validation
├── pagination.py         # Pagination handling logic
├── labels.py             # Label mapping functionality
├── filters.py            # Filter construction and application
├── types.py              # Type definitions and dataclasses
└── exceptions.py         # Custom exception classes
```

## Complete dependency analysis

### Core dependencies (Imports)

The educationdata package has a **minimal dependency footprint**:

**httr** - HTTP client for R
- Purpose: All API communication
- Key functions: `GET()`, `content()`, `http_type()`, `http_error()`, `status_code()`
- Used for: Making requests, handling responses, error checking

**jsonlite** - JSON parsing
- Purpose: Converting API JSON responses to R objects
- Key function: `fromJSON()` with automatic simplification
- Used for: Parsing API responses into data.frames

**glue** (likely) - String interpolation
- Purpose: Clean URL construction
- Used for: Building API endpoint URLs with parameter substitution

**Standard R packages** (no external dependencies):
- Base R data manipulation
- Standard data.frame operations

### Python equivalent dependencies

For a modern Python implementation targeting Python 3.10+:

**Core dependencies**:
- **requests** or **httpx** - HTTP client (httpx recommended for async support)
- **pandas** - DataFrame manipulation (core data structure)
- **pydantic** - Data validation and settings (type-safe parameter validation)

**Optional dependencies** (in extras_require):
- **tqdm** - Progress bars (for verbose mode)
- **requests-cache** - Optional caching (if implemented)
- **pyarrow** - Fast CSV reading (faster than pandas default)

**Development dependencies**:
- **pytest** - Testing framework
- **pytest-cov** - Coverage reporting
- **httpretty** or **responses** - HTTP mocking for tests
- **black** - Code formatting
- **mypy** - Static type checking
- **sphinx** - Documentation generation

### Dependency rationale

The R package's minimal dependencies reflect a philosophy of **simplicity and stability**. By relying only on well-established, stable packages (httr and jsonlite), the package minimizes maintenance burden and dependency conflicts. This approach should guide the Python equivalent - prefer fewer, well-maintained dependencies over numerous specialized packages.

## Helper functions and internal utilities

### Internal function inventory

While only two functions are user-facing, the package contains numerous internal utilities:

**get_endpoint_info()** - Metadata retrieval
- Queries API metadata endpoints
- Returns available levels, sources, topics, subtopics
- Provides variable lists and required/optional parameters
- Used by validation logic to check user inputs

**validate_function_args()** - Input validation
- Cross-references user parameters against endpoint metadata
- Validates level + source + topic combinations exist
- Checks filter variables are valid for the endpoint
- Returns validated and normalized parameters

**URL builders** - Endpoint URL construction
- Builds API URLs following the pattern: `{base}/api/v1/{level}/{source}/{topic}/{year}/{disaggregators}/?{filters}`
- Properly encodes query parameters
- Handles list filters (e.g., grade=9&grade=10&grade=11)
- Constructs CSV download URLs

**Filter processors** - Query parameter handling
- Converts R list filters to API query parameters
- Handles vectorized inputs (year = 2004:2008)
- Processes special filter types (grade strings like 'grade-pk')
- For CSV mode, applies filters post-download to the data.frame

**Label mappers** - Factor conversion
- Queries variable metadata for label definitions
- Creates factor objects with proper level ordering
- Preserves original integer values as underlying codes
- Applies to multiple categorical variables efficiently

**Pagination handlers** - Multi-page data retrieval
- Calculates total pages from record count
- Iterates through paginated responses
- Accumulates data.frames efficiently
- Handles edge cases (empty results, single page)

**CSV processors** - Bulk data handling
- Downloads complete CSV files from API
- Uses efficient CSV reading (likely data.table::fread or readr::read_csv)
- Applies filters post-download
- Handles large files efficiently

### Python implementation strategy

For each R helper function, create a corresponding Python function or class:

```python
# metadata.py
class MetadataClient:
    """Handles API metadata queries with caching."""
    def get_endpoint_info(self, level, source, topic) -> EndpointInfo:
        """Retrieve and validate endpoint metadata."""
        
# validation.py
def validate_parameters(level: str, source: str, topic: str, 
                       filters: dict = None) -> ValidatedParams:
    """Validate parameters against API metadata."""

# url_builder.py
class URLBuilder:
    """Constructs API endpoint URLs."""
    def build_data_url(self, params: ValidatedParams) -> str:
        """Build URL for data endpoint."""
    def build_csv_url(self, params: ValidatedParams) -> str:
        """Build URL for CSV download."""

# labels.py
class LabelMapper:
    """Applies labels to coded categorical variables."""
    def get_label_mappings(self, endpoint: str) -> dict:
        """Retrieve label definitions from metadata."""
    def apply_labels(self, df: pd.DataFrame, mappings: dict) -> pd.DataFrame:
        """Convert coded columns to categoricals with labels."""
```

## Practical usage patterns and workflows

### Most common usage pattern

The typical workflow starts simple and adds complexity as needed:

**Basic query** - Retrieve all available data:
```r
df <- get_education_data(
  level = 'schools',
  source = 'ccd',
  topic = 'enrollment'
)
```

**Add disaggregation** - Break down by demographics:
```r
df <- get_education_data(
  level = 'schools',
  source = 'ccd',
  topic = 'enrollment',
  subtopic = list('race', 'sex')
)
```

**Apply filters** - Subset to specific years/grades:
```r
df <- get_education_data(
  level = 'schools',
  source = 'ccd',
  topic = 'enrollment',
  subtopic = list('race', 'sex'),
  filters = list(year = 2008, grade = 9:12)
)
```

**Add labels** - Get human-readable categories:
```r
df <- get_education_data(
  level = 'schools',
  source = 'ccd',
  topic = 'enrollment',
  subtopic = list('race', 'sex'),
  filters = list(year = 2008, grade = 9:12),
  add_labels = TRUE
)
```

**Use CSV for bulk data** - Faster for large datasets:
```r
df <- get_education_data(
  level = 'schools',
  source = 'ccd',
  topic = 'directory',
  filters = list(year = 2020),
  csv = TRUE
)
```

### Advanced patterns

**Summary statistics** - Aggregated data from server:
```r
totals <- get_education_data_summary(
  level = "schools",
  source = "ccd",
  topic = "enrollment",
  stat = "sum",
  var = "enrollment",
  by = "fips",
  filters = list(year = 2020)
)
```

**Multiple filter values** - States, years, grades:
```r
df <- get_education_data(
  level = 'schools',
  source = 'ccd',
  topic = 'directory',
  filters = list(
    year = 2015:2020,
    fips = c(6, 17, 36),  # CA, IL, NY
    school_level = 3       # High schools
  )
)
```

**Complete analysis workflow**:
```r
library(educationdata)
library(dplyr)

# Get school metadata
schools <- get_education_data(
  level = 'schools',
  source = 'ccd',
  topic = 'directory',
  filters = list(year = 2020, fips = 6),
  add_labels = TRUE
)

# Get enrollment by demographics
enrollment <- get_education_data(
  level = 'schools',
  source = 'ccd',
  topic = 'enrollment',
  subtopic = list('race', 'sex'),
  filters = list(year = 2020, fips = 6),
  add_labels = TRUE
)

# Join and analyze
analysis <- enrollment %>%
  left_join(schools, by = c("ncessch", "year")) %>%
  group_by(school_type, race) %>%
  summarize(total = sum(enrollment, na.rm = TRUE))
```

### Performance best practices

**Use main filters**: Variables marked as "main filters" (typically year and grade) enable server-side optimization:
```r
# Fast: Uses main filters
df <- get_education_data(..., filters = list(year = 2008, grade = 9))

# Slower: Other filters applied after initial retrieval
df <- get_education_data(..., filters = list(ncessch = '340606000122'))
```

**Choose CSV vs JSON strategically**:
- **JSON (default)**: Small filtered queries, specific schools/districts
- **CSV**: Complete datasets, large subsets, repeated analysis of same year

**Use summary endpoints**: For aggregations, let the server compute:
```r
# Fast: Server-side aggregation
totals <- get_education_data_summary(
  level = "schools",
  source = "ccd",
  topic = "enrollment",
  stat = "sum",
  var = "enrollment",
  by = "fips"
)

# Slow: Download all records then aggregate locally
all_data <- get_education_data(level = "schools", source = "ccd", topic = "enrollment")
totals <- aggregate(enrollment ~ fips, data = all_data, FUN = sum)
```

## File and directory structure

### Standard R package layout

The repository follows **R package development conventions** exactly:

```
education-data-package-r/
├── .github/
│   └── workflows/
│       ├── R-CMD-check.yaml    # CI: Run tests on push/PR
│       └── pkgdown.yaml        # CI: Build and deploy docs
├── R/
│   ├── get_education_data.R
│   ├── get_education_data_summary.R
│   ├── get_education_data_json.R
│   ├── get_education_data_csv.R
│   ├── get_endpoint_info.R
│   ├── validate_function_args.R
│   ├── utils.R
│   └── [~6 additional source files]
├── man/
│   ├── get_education_data.Rd
│   ├── get_education_data_summary.Rd
│   └── [generated from roxygen2]
├── tests/
│   ├── testthat.R
│   └── testthat/
│       ├── test-get-education-data.R
│       ├── test-validation.R
│       └── [additional test files]
├── vignettes/
│   └── introducing-educationdata.Rmd
├── DESCRIPTION              # Package metadata, dependencies
├── NAMESPACE               # Exported functions (auto-generated)
├── LICENSE.md              # MIT License
├── NEWS.md                 # Version history changelog
├── README.md               # Primary documentation
└── _pkgdown.yml           # Website configuration
```

### Python equivalent structure

For a modern Python package with similar organization:

```
educationdata-python/
├── .github/
│   └── workflows/
│       ├── tests.yml           # CI: Run pytest on multiple Python versions
│       ├── lint.yml            # CI: Run black, mypy, flake8
│       └── docs.yml            # CI: Build and deploy Sphinx docs
├── educationdata/
│   ├── __init__.py            # Public API exports
│   ├── api.py                 # get_education_data()
│   ├── summary.py             # get_education_data_summary()
│   ├── client.py              # HTTP client wrapper
│   ├── metadata.py            # Metadata fetching
│   ├── validation.py          # Parameter validation
│   ├── pagination.py          # Pagination logic
│   ├── labels.py              # Label mapping
│   ├── filters.py             # Filter construction
│   ├── url_builder.py         # URL construction
│   ├── types.py               # Type definitions, dataclasses
│   ├── exceptions.py          # Custom exceptions
│   └── py.typed               # PEP 561 marker for type hints
├── tests/
│   ├── __init__.py
│   ├── test_api.py
│   ├── test_validation.py
│   ├── test_pagination.py
│   ├── test_labels.py
│   ├── conftest.py            # Pytest fixtures
│   └── fixtures/              # Mock API responses
├── docs/
│   ├── conf.py                # Sphinx configuration
│   ├── index.rst              # Documentation homepage
│   ├── api.rst                # API reference
│   ├── quickstart.rst         # Getting started guide
│   └── examples.rst           # Usage examples
├── examples/
│   └── notebooks/
│       └── tutorial.ipynb     # Jupyter notebook examples
├── pyproject.toml             # PEP 518 build config, dependencies
├── setup.py                   # Package setup (if needed for editable install)
├── CHANGELOG.md               # Version history
├── README.md                  # Primary documentation
├── LICENSE                    # MIT License
└── .readthedocs.yml          # Read the Docs configuration
```

### Key organizational principles

**Flat module structure**: The R package uses a flat R/ directory with ~13 files. The Python equivalent should similarly avoid deep nesting - one level of modules is sufficient.

**Clear public API**: Use `__init__.py` to explicitly export public functions:
```python
# educationdata/__init__.py
from educationdata.api import get_education_data
from educationdata.summary import get_education_data_summary

__all__ = ['get_education_data', 'get_education_data_summary']
__version__ = '0.1.0'
```

**Separate tests from source**: Tests in a parallel tests/ directory, not mixed with source code.

**Documentation as code**: Vignettes in R map to Jupyter notebooks or RST files with executable examples in Python.

## Testing approach and framework

### Testing infrastructure

The package uses **testthat**, R's de facto standard testing framework:

**Test organization**:
```
tests/
├── testthat.R               # Test runner
└── testthat/
    ├── test-get-education-data.R
    ├── test-validation.R
    ├── test-csv-download.R
    └── [additional test files]
```

**Test structure pattern**:
```r
test_that("get_education_data returns data.frame", {
  df <- get_education_data(
    level = 'schools',
    source = 'ccd',
    topic = 'enrollment',
    filters = list(year = 2008, grade = 9)
  )
  expect_s3_class(df, "data.frame")
  expect_true(nrow(df) > 0)
  expect_true("enrollment" %in% colnames(df))
})

test_that("invalid level throws error", {
  expect_error(
    get_education_data(level = 'invalid', source = 'ccd', topic = 'enrollment'),
    "Level must be one of"
  )
})
```

### Continuous integration

**GitHub Actions** runs automated checks:

**R-CMD-check workflow**:
- Runs on: Linux, macOS, Windows
- Tests multiple R versions
- Executes full package check including:
  - Build package
  - Run all tests
  - Check documentation
  - Verify CRAN compliance

**Recent updates**: Tests modified to handle internet resource unavailability gracefully (CRAN policy requirement).

### Test coverage areas

Based on package functionality, tests cover:

**API integration tests**:
- Successful data retrieval from various endpoints
- Pagination handling for large result sets
- CSV vs JSON download modes
- Summary endpoint functionality

**Parameter validation tests**:
- Valid parameter combinations
- Invalid level/source/topic combinations
- Filter validation
- Deprecated parameter warnings

**Data processing tests**:
- Correct data type conversions
- Label addition functionality
- Filter application (especially for CSV mode)
- Grade and level_of_study special handling

**Error handling tests**:
- HTTP error responses (404, 500, 503)
- Network failures
- Invalid API responses
- Empty result sets

### Python testing equivalent

**Use pytest** as the testing framework:

```python
# tests/test_api.py
import pytest
import pandas as pd
from educationdata import get_education_data
from educationdata.exceptions import EndpointNotFoundError

def test_get_education_data_returns_dataframe():
    """Test basic data retrieval returns DataFrame."""
    df = get_education_data(
        level='schools',
        source='ccd',
        topic='enrollment',
        filters={'year': 2008, 'grade': 9}
    )
    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0
    assert 'enrollment' in df.columns

def test_invalid_level_raises_error():
    """Test that invalid level raises appropriate exception."""
    with pytest.raises(EndpointNotFoundError, match="Level must be one of"):
        get_education_data(level='invalid', source='ccd', topic='enrollment')

@pytest.mark.parametrize("year,grade", [
    (2008, 9),
    (2010, [9, 10, 11, 12]),
    ([2008, 2009], 9),
])
def test_filters_work_correctly(year, grade):
    """Test various filter combinations."""
    df = get_education_data(
        level='schools',
        source='ccd',
        topic='enrollment',
        filters={'year': year, 'grade': grade}
    )
    assert isinstance(df, pd.DataFrame)
```

**Mock API responses** for unit tests:
```python
# tests/conftest.py
import pytest
import responses

@pytest.fixture
def mock_api():
    """Fixture to mock API responses."""
    with responses.RequestsMock() as rsps:
        rsps.add(
            responses.GET,
            'https://educationdata.urban.org/api/v1/schools/ccd/enrollment',
            json={
                'count': 100,
                'results': [
                    {'year': 2008, 'enrollment': 500, 'ncessch': '123456789012'}
                ],
                'next': None
            },
            status=200
        )
        yield rsps
```

**CI/CD with GitHub Actions**:
```yaml
# .github/workflows/tests.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        python-version: ['3.10', '3.11', '3.12']
    
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -e ".[dev]"
    - name: Run tests with coverage
      run: |
        pytest tests/ -v --cov=educationdata --cov-report=xml
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
```

## Documentation standards and patterns

### Documentation framework

The package uses **roxygen2** for function documentation:

**Roxygen2 comment structure**:
```r
#' Obtain data from the Urban Institute Education Data Portal API
#'
#' Retrieves data from the Urban Institute's Education Data Portal API
#' and returns it as a data.frame for analysis.
#'
#' @param level API data level to query
#' @param source API data source to query
#' @param topic API data topic to query
#' @param subtopic Optional 'list' of grouping parameters to pass to an API call
#' @param filters Optional 'list' of query values to filter an API call
#' @param add_labels Add variable labels (when applicable)? Defaults to FALSE.
#' @param csv Download the full csv file? Defaults to FALSE.
#' @param verbose Print messages and warnings? Defaults to TRUE.
#'
#' @return A `data.frame` of education data
#'
#' @examples
#' \dontrun{
#' df <- get_education_data(
#'   level = 'schools',
#'   source = 'ccd',
#'   topic = 'enrollment',
#'   filters = list(year = 2008, grade = 9)
#' )
#' }
#'
#' @export
get_education_data <- function(level, source, topic, ...) {
  # Implementation
}
```

**Generated .Rd files**: Roxygen2 automatically generates man/*.Rd files in R documentation format from these comments.

### Documentation components

**README.md** contains:
- Package overview and purpose
- Installation instructions (CRAN and GitHub)
- Quick start examples showing basic usage
- Table of all available endpoints
- Links to full documentation
- Data policy notice

**NEWS.md** tracks changes:
```markdown
# educationdata 0.1.4

* Bumped version for CRAN submission
* Added `verbose` argument to `get_education_data()`
* Updated package documentation
* Bug fixes for filtering when downloading from CSV

# educationdata 0.1.3

* Added `get_education_data_summary()` function
* Soft-deprecated `by` argument in favor of `subtopic`
```

**Vignettes** provide tutorials:
- `introducing-educationdata.Rmd` - Comprehensive tutorial
- Shows real workflows with multiple examples
- Explains endpoint structure and filtering
- Demonstrates parameter combinations

**pkgdown website** (https://urbaninstitute.github.io/education-data-package-r/):
- Auto-generated from package documentation
- Function reference organized alphabetically
- Vignettes rendered as articles
- Changelog from NEWS.md
- Configured via _pkgdown.yml

### Python documentation equivalent

**Use docstrings** (Google or NumPy style):

```python
def get_education_data(
    level: str,
    source: str,
    topic: str,
    subtopic: Optional[List[str]] = None,
    filters: Optional[Dict[str, Any]] = None,
    add_labels: bool = False,
    csv: bool = False,
    verbose: bool = True
) -> pd.DataFrame:
    """
    Obtain data from the Urban Institute Education Data Portal API.
    
    Retrieves education data from specified API endpoints and returns
    it as a pandas DataFrame for analysis.
    
    Parameters
    ----------
    level : str
        API data level to query. Must be one of 'schools', 
        'school-districts', or 'college-university'.
    source : str
        API data source to query (e.g., 'ccd', 'ipeds', 'crdc').
    topic : str
        API data topic to query (e.g., 'enrollment', 'directory').
    subtopic : list of str, optional
        Grouping parameters for disaggregation (e.g., ['race', 'sex']).
    filters : dict, optional
        Query values to filter results. Common keys include 'year',
        'grade', 'fips', 'ncessch'.
    add_labels : bool, default False
        If True, convert integer-coded variables to categorical with
        descriptive labels.
    csv : bool, default False
        If True, download full CSV file instead of using JSON API.
        Faster for large datasets, slower for small filtered queries.
    verbose : bool, default True
        If True, display progress messages during data retrieval.
    
    Returns
    -------
    pandas.DataFrame
        Education data from the specified endpoint with columns
        representing endpoint variables.
    
    Raises
    ------
    EndpointNotFoundError
        If the level/source/topic combination doesn't exist.
    InvalidFilterError
        If filter variables are invalid for the endpoint.
    APIConnectionError
        If the API request fails.
    
    Examples
    --------
    Basic usage with filters:
    
    >>> df = get_education_data(
    ...     level='schools',
    ...     source='ccd',
    ...     topic='enrollment',
    ...     filters={'year': 2020, 'grade': [9, 10, 11, 12]}
    ... )
    >>> df.shape
    (15420, 8)
    
    With demographic disaggregation:
    
    >>> df = get_education_data(
    ...     level='schools',
    ...     source='ccd',
    ...     topic='enrollment',
    ...     subtopic=['race', 'sex'],
    ...     filters={'year': 2020, 'grade': 9},
    ...     add_labels=True
    ... )
    >>> df['race'].dtype
    CategoricalDtype(categories=['White', 'Black', 'Hispanic', ...], ordered=False)
    
    See Also
    --------
    get_education_data_summary : Retrieve aggregated summary statistics
    
    Notes
    -----
    By using this package, you agree to the Urban Institute Education
    Data Portal's Data Policy and Terms of Use.
    
    For best performance with large datasets, use csv=True. For small
    filtered queries, the default JSON API is faster.
    """
```

**Sphinx for documentation generation**:

```python
# docs/conf.py
project = 'educationdata'
extensions = [
    'sphinx.ext.autodoc',      # Auto-generate from docstrings
    'sphinx.ext.napoleon',     # Support Google/NumPy style
    'sphinx.ext.viewcode',     # Add source code links
    'sphinx.ext.intersphinx',  # Link to other docs
    'sphinx_autodoc_typehints', # Use type hints in docs
]

# Type hints configuration
autodoc_typehints = 'description'
napoleon_google_docstring = True
napoleon_include_init_with_doc = True
```

**Documentation structure**:
```
docs/
├── index.rst              # Homepage
├── quickstart.rst         # Getting started guide
├── api.rst                # API reference
├── examples.rst           # Usage examples
├── endpoints.rst          # Available endpoints
├── changelog.rst          # Version history
└── contributing.rst       # Development guide
```

## Key design decisions for Python implementation

### Modern Python patterns to adopt

**Type hints everywhere** (Python 3.10+ syntax):
```python
from typing import Literal

def get_education_data(
    level: Literal['schools', 'school-districts', 'college-university'],
    source: str,
    topic: str,
    subtopic: list[str] | None = None,
    filters: dict[str, Any] | None = None,
    add_labels: bool = False,
    csv: bool = False,
    verbose: bool = True
) -> pd.DataFrame:
    ...
```

**Dataclasses for structured data**:
```python
from dataclasses import dataclass

@dataclass
class EndpointInfo:
    """Metadata about an API endpoint."""
    level: str
    source: str
    topic: str
    subtopic: list[str] | None
    years_available: list[int]
    main_filters: list[str]
    optional_filters: list[str]
    csv_available: bool

@dataclass
class ValidatedParams:
    """Validated and normalized parameters."""
    endpoint: EndpointInfo
    filters: dict[str, Any]
    add_labels: bool
    csv: bool
```

**Pydantic for validation**:
```python
from pydantic import BaseModel, Field, validator

class GetEducationDataParams(BaseModel):
    """Parameter validation for get_education_data."""
    level: Literal['schools', 'school-districts', 'college-university']
    source: str
    topic: str
    subtopic: list[str] | None = None
    filters: dict[str, Any] = Field(default_factory=dict)
    add_labels: bool = False
    csv: bool = False
    verbose: bool = True
    
    @validator('source')
    def validate_source(cls, v, values):
        # Custom validation logic
        return v
```

**Context managers for resource handling**:
```python
class EducationDataClient:
    """Client for Education Data API."""
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        # Cleanup if needed
        pass

# Usage
with EducationDataClient() as client:
    df = client.get_education_data(...)
```

**Async support for concurrent requests** (optional):
```python
import asyncio
import httpx

async def get_education_data_async(
    level: str,
    source: str,
    topic: str,
    **kwargs
) -> pd.DataFrame:
    """Async version using httpx."""
    async with httpx.AsyncClient() as client:
        # Implementation
        pass

# Allow fetching multiple endpoints concurrently
async def get_multiple_endpoints(endpoints: list) -> list[pd.DataFrame]:
    tasks = [get_education_data_async(**ep) for ep in endpoints]
    return await asyncio.gather(*tasks)
```

### Architecture recommendations

**Configuration management**:
```python
# educationdata/config.py
from dataclasses import dataclass

@dataclass
class Config:
    """Package configuration."""
    api_base_url: str = "https://educationdata.urban.org"
    api_version: str = "v1"
    timeout: int = 30
    max_retries: int = 3
    cache_enabled: bool = False
    cache_ttl: int = 3600
    
# Global config instance
config = Config()
```

**Logging instead of print statements**:
```python
import logging

logger = logging.getLogger(__name__)

def get_education_data(..., verbose: bool = True):
    if verbose:
        logger.info(f"Fetching data from {level}/{source}/{topic}")
        logger.info(f"Retrieving page {page} of {total_pages}")
```

**Proper exception hierarchy**:
```python
class EducationDataError(Exception):
    """Base exception for educationdata package."""

class EndpointNotFoundError(EducationDataError):
    """Raised when endpoint doesn't exist."""

class InvalidFilterError(EducationDataError):
    """Raised when filter is invalid for endpoint."""

class APIConnectionError(EducationDataError):
    """Raised when API request fails."""

class PaginationError(EducationDataError):
    """Raised when pagination handling fails."""
```

## Critical implementation considerations

### Maintain API design simplicity

The R package succeeds because of its **minimalist API**. Users need to learn only one main function with intuitive parameters. The Python version should maintain this simplicity:

```python
# Good: Simple, clear API
df = get_education_data(
    level='schools',
    source='ccd',
    topic='enrollment',
    filters={'year': 2020}
)

# Bad: Over-engineered OOP
client = EducationDataClient(api_key=None)
request = EnrollmentRequest(level='schools', source='ccd')
request.add_filter('year', 2020)
df = client.execute(request)
```

### Performance optimization strategies

**Efficient pagination**:
- Accumulate DataFrames in a list
- Use `pd.concat()` once at the end
- Never repeatedly concatenate inside loops

```python
# Good
dfs = []
while next_url:
    response = client.get(next_url)
    dfs.append(pd.DataFrame(response['results']))
    next_url = response['next']
return pd.concat(dfs, ignore_index=True)

# Bad
df = pd.DataFrame()
while next_url:
    response = client.get(next_url)
    df = pd.concat([df, pd.DataFrame(response['results'])])  # Slow!
```

**CSV handling with pyarrow**:
```python
import pyarrow.csv as pv

# Faster CSV reading
table = pv.read_csv(csv_file)
df = table.to_pandas()
```

**Batch label mapping**:
```python
# Apply all label mappings at once
label_cols = get_labeled_columns(endpoint)
for col in label_cols:
    mapping = get_label_mapping(col)
    df[col] = pd.Categorical.from_codes(
        df[col], 
        categories=[mapping[i] for i in range(len(mapping))]
    )
```

### Testing strategy

**Unit tests with mocked API**:
- Use `responses` or `httpretty` to mock HTTP calls
- Test all parameter combinations
- Verify error handling

**Integration tests against real API**:
- Mark with `@pytest.mark.integration`
- Run less frequently
- Test actual data retrieval
- Handle API availability gracefully

**Property-based testing**:
```python
from hypothesis import given, strategies as st

@given(
    year=st.integers(min_value=1980, max_value=2025),
    grade=st.integers(min_value=9, max_value=12)
)
def test_filters_accept_valid_ranges(year, grade):
    """Property test: valid year/grade ranges should work."""
    df = get_education_data(
        level='schools',
        source='ccd',
        topic='enrollment',
        filters={'year': year, 'grade': grade}
    )
    assert isinstance(df, pd.DataFrame)
```

### Documentation priorities

**README should enable immediate success**:
1. One-line description
2. Installation command
3. Minimal working example
4. Link to full docs

**API reference should be exhaustive**:
- Every parameter documented
- Type information clear
- Examples for each function
- Common errors explained

**Tutorials should follow learning path**:
1. Quickstart: Basic usage in 5 minutes
2. Guide: Understanding endpoints and filters
3. Examples: Real-world analysis workflows
4. Advanced: Performance optimization, async usage

## Conclusion and implementation roadmap

The educationdata R package demonstrates excellent API client design through simplicity, robust error handling, and comprehensive documentation. The Python equivalent should:

**Preserve the strengths**:
- Minimalist two-function public API
- Automatic pagination handling
- Metadata-driven validation
- Optional label addition
- CSV vs JSON flexibility

**Enhance with modern Python**:
- Type hints for IDE support and validation
- Dataclasses for structured data
- Better exception hierarchy
- Optional async support
- More sophisticated progress indicators

**Maintain the philosophy**:
- Simplicity over complexity
- Explicit over implicit
- Performance where it matters
- Comprehensive documentation
- Minimal dependencies

The resulting Python package will provide researchers with a powerful, intuitive tool for accessing education data that feels native to the Python ecosystem while maintaining the thoughtful design decisions that make the R package successful.