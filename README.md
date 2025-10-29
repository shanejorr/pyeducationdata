# pyeducationdata

Python package for accessing the Urban Institute's Education Data Portal API.

[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

`pyeducationdata` is a Python client library for the [Urban Institute's Education Data Portal API](https://educationdata.urban.org/). It provides convenient access to comprehensive US education data from kindergarten through postsecondary education, covering decades of data from multiple federal sources.

This package is a Python implementation inspired by the Urban Institute's [R package `educationdata`](https://github.com/UrbanInstitute/education-data-package-r), designed to provide the same functionality with a Pythonic interface.

## Features

- **Simple API**: Two main functions mirror the R package design
- **Automatic pagination**: Handles the API's 10,000 record limit transparently
- **Type-safe**: Full type hints and pydantic validation
- **Flexible filtering**: Filter by year, grade, location, and more
- **Label mapping**: Convert integer codes to human-readable labels
- **CSV support**: Download complete datasets efficiently
- **Summary statistics**: Server-side aggregation for fast statistics

## Installation

### Using pip

```bash
pip install pyeducationdata
```

### Using uv

```bash
uv add pyeducationdata
```

### Development installation

```bash
git clone https://github.com/shaneorr/pyeducationdata.git
cd pyeducationdata
uv pip install -e ".[dev]"
```

## Quick Start

```python
import pyeducationdata as ped

# Get school enrollment data with demographic breakdowns
df = ped.get_education_data(
    level='schools',
    source='ccd',
    topic='enrollment',
    subtopic=['race', 'sex'],
    filters={'year': 2020, 'grade': [9, 10, 11, 12], 'fips': 13},
    add_labels=True
)

print(df.head())
```

## Main Functions

### `get_education_data()`

Retrieve data from the Education Data Portal API.

**Parameters:**
- `level` (str, required): API data level - `'schools'`, `'school-districts'`, or `'college-university'`
- `source` (str, required): Data source - `'ccd'`, `'crdc'`, `'ipeds'`, `'edfacts'`, etc.
- `topic` (str, required): Data topic - `'enrollment'`, `'directory'`, `'finance'`, etc.
- `subtopic` (list[str] | None): Grouping parameters like `['race', 'sex']`
- `filters` (dict | None): Query filters like `{'year': 2020, 'grade': 9}`
- `add_labels` (bool): Convert integer codes to descriptive labels (default: `False`)
- `csv` (bool): Download full CSV instead of using JSON API (default: `False`)

**Returns:** `pandas.DataFrame`

### `get_education_data_summary()`

Retrieve aggregated summary statistics from the API.

**Parameters:**
- `level`, `source`, `topic`, `subtopic`: Same as `get_education_data()`
- `stat` (str, required): Statistic to compute - `'sum'`, `'avg'`, `'median'`, `'max'`, `'min'`, `'count'`
- `var` (str, required): Variable to aggregate
- `by` (str | list[str]): Variables to group by
- `filters` (dict | None): Query filters

**Returns:** `pandas.DataFrame`

## Usage Examples

### Example 1: School Directory Data

Get information about schools in California for 2020:

```python
import pyeducationdata as ped

schools = ped.get_education_data(
    level='schools',
    source='ccd',
    topic='directory',
    filters={'year': 2020, 'fips': 6},  # fips=6 is California
    add_labels=True
)

print(f"Found {len(schools)} schools")
print(schools[['school_name', 'city', 'charter', 'school_level']].head())
```

### Example 2: Enrollment by Demographics

Get enrollment by race and sex for high school grades:

```python
enrollment = ped.get_education_data(
    level='schools',
    source='ccd',
    topic='enrollment',
    subtopic=['race', 'sex'],
    filters={
        'year': 2020,
        'grade': [9, 10, 11, 12],
        'fips': 36  # New York
    },
    add_labels=True
)

# Analyze enrollment patterns
enrollment_summary = enrollment.groupby(['race', 'sex'])['enrollment'].sum()
print(enrollment_summary)
```

### Example 3: College/University Data

Get IPEDS data for 4-year public universities:

```python
colleges = ped.get_education_data(
    level='college-university',
    source='ipeds',
    topic='directory',
    filters={'year': 2023}
)

# Filter to 4-year public institutions
public_4year = colleges[
    (colleges['inst_level'] == 1) &  # 4-year
    (colleges['inst_control'] == 1)   # Public
]
print(f"Found {len(public_4year)} public 4-year institutions")
```

### Example 4: Summary Statistics

Get state-level enrollment totals:

```python
state_totals = ped.get_education_data_summary(
    level='schools',
    source='ccd',
    topic='enrollment',
    stat='sum',
    var='enrollment',
    by='fips',
    filters={'year': 2020}
)

print(state_totals.sort_values('enrollment', ascending=False).head(10))
```

### Example 5: Multi-Year Analysis

Get enrollment trends over multiple years:

```python
trends = ped.get_education_data(
    level='schools',
    source='ccd',
    topic='enrollment',
    filters={
        'year': [2015, 2016, 2017, 2018, 2019, 2020],
        'grade': 99,  # All grades total
        'fips': 17    # Illinois
    }
)

# Analyze yearly trends
yearly_totals = trends.groupby('year')['enrollment'].sum()
print(yearly_totals)
```

## Available Data

The Education Data Portal provides 160+ endpoints across three institutional levels:

### Schools (K-12 school level)
- **CCD (Common Core of Data)**: School directory, enrollment, demographics (1986-2023)
- **CRDC (Civil Rights Data Collection)**: Discipline, advanced coursework, school characteristics (2011-2020, biennial)
- **EdFacts**: Assessment results, graduation rates (2009-2020)
- **NHGIS**: Census data at school locations

### School Districts (K-12 district level)
- **CCD**: District directory, enrollment, finance data (1986-2023)
- **EdFacts**: District assessments and graduation rates
- **SAIPE**: Poverty estimates for school-age children (1995-2023)

### Colleges and Universities
- **IPEDS**: Comprehensive postsecondary data - admissions, enrollment, completions, finance, student aid (1980-2023)
- **College Scorecard**: Student outcomes, earnings, loan repayment (1996-2020)
- **FSA**: Federal student aid data
- **Other**: Campus crime, athletics, endowments

## API Structure

The Education Data Portal API is organized hierarchically:

```
https://educationdata.urban.org/api/v1/{level}/{source}/{topic}/{subtopic}/{year}/
```

For example:
```
https://educationdata.urban.org/api/v1/schools/ccd/enrollment/race/2020/
```

This package handles URL construction, pagination, and data formatting automatically.

## Data Attribution

By using this package, you agree to the Urban Institute's Data Policy and Terms of Use. The data is provided under the Open Data Commons Attribution License (ODC-By) v1.0.

**When using the data in publications, please provide attribution:**

```
[Dataset names], Education Data Portal (Version 0.23.0), Urban Institute,
accessed [Month DD, YYYY], https://educationdata.urban.org/documentation/,
made available under the ODC Attribution License.
```

## Comparison to R Package

This package aims for feature parity with the Urban Institute's R `educationdata` package:

| Feature | R Package | Python Package |
|---------|-----------|----------------|
| Main function | `get_education_data()` | `get_education_data()` |
| Summary function | `get_education_data_summary()` | `get_education_data_summary()` |
| Automatic pagination | ✓ | ✓ |
| Label mapping | ✓ | ✓ |
| CSV downloads | ✓ | ✓ |
| Type safety | R types | Python type hints + pydantic |
| Async support | N/A | Not yet (sync only) |

## Technical Details

### Implementation

- **HTTP Client**: Uses `httpx` for reliable HTTP communication
- **Data Handling**: Returns `pandas.DataFrame` objects
- **Validation**: Uses `pydantic` v2 for parameter validation
- **Sync Only**: Currently synchronous implementation (async may be added in future)

### Requirements

- Python 3.9+
- httpx >= 0.27.0
- pandas >= 2.0.0
- pydantic >= 2.0.0

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Development

```bash
# Clone the repository
git clone https://github.com/shaneorr/pyeducationdata.git
cd pyeducationdata

# Install with development dependencies
uv pip install -e ".[dev]"

# Run tests
pytest

# Run linting
ruff check .

# Format code
ruff format .
```

## License

This package is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

The data accessed through this package is provided by the Urban Institute under the Open Data Commons Attribution License (ODC-By) v1.0.

## Links

- **Education Data Portal**: https://educationdata.urban.org/
- **API Documentation**: https://educationdata.urban.org/documentation/
- **R Package**: https://github.com/UrbanInstitute/education-data-package-r
- **Urban Institute**: https://www.urban.org/

## Support

For questions about the package, please open an issue on GitHub.

For questions about the data or API, contact the Urban Institute at educationdata@urban.org.
