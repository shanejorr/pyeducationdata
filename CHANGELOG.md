# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-10-29

Initial alpha release.

### Added
- Initial release of pyeducationdata
- Core functionality for accessing the Urban Institute Education Data Portal API
- Two main functions: `get_education_data()` and `get_education_data_summary()`
- Automatic pagination handling for large datasets
- Parameter validation using pydantic v2
- Type hints throughout the codebase
- Comprehensive test suite using pytest and respx
- CI/CD configuration with GitHub Actions
- Full documentation and usage examples

### Features
- **Data Retrieval**: Access 160+ education data endpoints
- **Pagination**: Automatic handling of paginated API responses (10,000 record limit per page)
- **Filtering**: Server-side filtering by year, grade, location, and more
- **Summary Statistics**: Server-side aggregation (sum, avg, median, max, min, count, etc.)
- **Label Mapping**: Convert integer codes to descriptive categorical labels (placeholder implementation)
- **CSV Support**: Option to download complete datasets as CSV for better performance on large queries
- **Error Handling**: Clear, actionable error messages with custom exception hierarchy
- **HTTP Client**: Built on httpx with connection pooling, retries, and timeout handling

### Technical Details
- Python 3.9+ support
- Dependencies: httpx, pandas, pydantic v2
- Synchronous implementation (async support may be added in future)
- Type-safe with full type hints
- Comprehensive test coverage
- Modern packaging with pyproject.toml
