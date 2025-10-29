# pyeducationdata Examples

This directory contains practical examples demonstrating how to use the `pyeducationdata` package.

## Quick Start

To run these examples, first make sure the package is installed:

```bash
# Install the package
uv pip install -e .

# Or with pip
pip install -e .
```

Then run any example:

```bash
python examples/01_simple_example.py
```

## Examples Overview

### 1. Simple Example (`01_simple_example.py`)
**Start here!** The simplest possible example to verify the package works.

- Fetches basic school directory data
- Uses a small state (Delaware) for quick results
- Perfect for testing your installation

**Run time:** ~5-10 seconds

```bash
python examples/01_simple_example.py
```

### 2. Enrollment Analysis (`02_enrollment_analysis.py`)
Demonstrates working with enrollment data and filters.

**Features:**
- Filtering by grade level (high school grades)
- Multi-year trend analysis
- Basic data analysis with pandas
- Grouping and aggregation

**Run time:** ~15-30 seconds

```bash
python examples/02_enrollment_analysis.py
```

### 3. Summary Statistics (`03_summary_statistics.py`)
Shows how to use the summary endpoints for fast aggregations.

**Features:**
- State-level totals (sum)
- Average school size (avg)
- School counts (count)
- Multi-dimensional grouping

**Run time:** ~10-20 seconds

```bash
python examples/03_summary_statistics.py
```

### 4. College Data (`04_college_data.py`)
Demonstrates working with postsecondary education data (IPEDS).

**Features:**
- College directory information
- Enrollment by level (undergraduate/graduate)
- Completions/degrees data
- State-level summaries

**Run time:** ~15-30 seconds

```bash
python examples/04_college_data.py
```

### 5. Error Handling (`05_error_handling.py`)
Shows how to handle errors and edge cases gracefully.

**Features:**
- Catching validation errors
- Handling non-existent endpoints
- Dealing with empty results
- Production-ready error handling patterns

**Run time:** ~5-10 seconds

```bash
python examples/05_error_handling.py
```

### 6. Basic Usage (`basic_usage.py`)
Comprehensive example with multiple use cases.

**Features:**
- School directory data
- Enrollment by demographics
- Summary statistics
- College data
- Multi-year trends

**Run time:** ~1-2 minutes (multiple API calls)

```bash
python examples/basic_usage.py
```

## Running All Examples

To run all examples in sequence:

```bash
for file in examples/0*.py; do
    echo "Running $file..."
    python "$file"
    echo ""
done
```

## What to Expect

### Success Output
When examples run successfully, you'll see:
- ✓ Success messages
- Data summaries and tables
- Record counts and statistics

### Common Issues

**Connection Errors:**
```
✗ Error: Network error: ...
```
→ Check your internet connection

**404 Errors:**
```
✗ Error: Endpoint not found (404): ...
```
→ The endpoint may not be available in the API
→ Check the API documentation

**Empty Results:**
```
✓ Retrieved 0 records
```
→ Your filters may be too restrictive
→ The data may not exist for that combination

## Tips for Testing

1. **Start with the simple example** (`01_simple_example.py`) to verify installation
2. **Use small states** (like Delaware, Rhode Island) for faster testing
3. **Recent years** tend to have more complete data
4. **Check the API documentation** for available endpoints: https://educationdata.urban.org/documentation/
5. **Be patient** - some queries can take 30-60 seconds depending on data size

## Modifying Examples

Feel free to modify these examples:

```python
# Change the state (FIPS code)
filters={'year': 2020, 'fips': 6}  # California instead of Delaware

# Change the year
filters={'year': 2019}  # Use 2019 instead of 2020

# Add more filters
filters={'year': 2020, 'fips': 36, 'charter': 1}  # Only charter schools in NY

# Change grade levels
filters={'grade': [6, 7, 8]}  # Middle school grades
```

## State FIPS Codes (Reference)

Common state FIPS codes for testing:

- 6 = California (large state, lots of data)
- 9 = Connecticut (medium state)
- 10 = Delaware (small state, fast queries)
- 13 = Georgia
- 17 = Illinois
- 36 = New York (large state)
- 44 = Rhode Island (small state, fast queries)
- 48 = Texas (large state, lots of data)

Full list: https://www.census.gov/library/reference/code-lists/ansi/ansi-codes-for-states.html

## Need Help?

- **Package Documentation:** See the main [README.md](../README.md)
- **API Documentation:** https://educationdata.urban.org/documentation/
- **Issue Tracker:** Report bugs or ask questions on GitHub

## Data Attribution

When using data from these examples in publications, provide attribution:

> Data from the Education Data Portal (Version 0.23.0), Urban Institute,
> accessed [Date], https://educationdata.urban.org/documentation/,
> made available under the ODC Attribution License.
