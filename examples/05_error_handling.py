"""Example: Error handling and debugging.

This example demonstrates:
- Common error scenarios
- How to handle exceptions
- Debugging tips
"""

import pyeducationdata as ped
from pyeducationdata import (
    APIConnectionError,
    EndpointNotFoundError,
    ValidationError,
)

print("=" * 80)
print("Error Handling Examples")
print("=" * 80)

# Example 1: Invalid level parameter
print("\n" + "-" * 80)
print("Example 1: Handling Invalid Parameters")
print("-" * 80)

try:
    df = ped.get_education_data(
        level='invalid_level',  # This is wrong
        source='ccd',
        topic='enrollment'
    )
except ValidationError as e:
    print("✓ Caught ValidationError (as expected):")
    print(f"  {e}")


# Example 2: Invalid endpoint combination
print("\n" + "-" * 80)
print("Example 2: Handling Non-existent Endpoints")
print("-" * 80)

try:
    df = ped.get_education_data(
        level='schools',
        source='ccd',
        topic='nonexistent_topic'  # This endpoint doesn't exist
    )
except (EndpointNotFoundError, APIConnectionError) as e:
    print("✓ Caught endpoint error (as expected):")
    print(f"  {e}")


# Example 3: Using correct parameters
print("\n" + "-" * 80)
print("Example 3: Correct Usage")
print("-" * 80)

try:
    df = ped.get_education_data(
        level='schools',
        source='ccd',
        topic='directory',
        filters={'year': 2020, 'fips': 10}  # Delaware, small state
    )
    print(f"✓ Success! Retrieved {len(df)} records")

except Exception as e:
    print(f"✗ Unexpected error: {e}")


# Example 4: Handling empty results
print("\n" + "-" * 80)
print("Example 4: Handling Empty Results")
print("-" * 80)

try:
    # Query that might return no results
    df = ped.get_education_data(
        level='schools',
        source='ccd',
        topic='enrollment',
        filters={
            'year': 2020,
            'fips': 10,
            'grade': 99,
            'ncessch': '999999999999'  # Non-existent school
        }
    )

    if df.empty:
        print("✓ Query succeeded but returned no results (empty DataFrame)")
        print("  This is expected - the school ID doesn't exist")
    else:
        print(f"Retrieved {len(df)} records")

except Exception as e:
    print(f"Error: {e}")


# Example 5: Graceful error handling in production code
print("\n" + "-" * 80)
print("Example 5: Production-Ready Error Handling")
print("-" * 80)


def safe_get_data(level, source, topic, **kwargs):
    """Example of production-ready error handling."""
    try:
        df = ped.get_education_data(
            level=level,
            source=source,
            topic=topic,
            **kwargs
        )

        if df.empty:
            print("Warning: Query returned no results")
            return None

        return df

    except ValidationError as e:
        print(f"Configuration error: {e}")
        print("Check your parameters and try again")
        return None

    except EndpointNotFoundError as e:
        print(f"Endpoint not found: {e}")
        print("Check the API documentation for valid combinations")
        return None

    except APIConnectionError as e:
        print(f"Connection error: {e}")
        print("Check your internet connection or try again later")
        return None

    except Exception as e:
        print(f"Unexpected error: {e}")
        return None


# Test the safe function
print("\nTesting safe_get_data function...")
result = safe_get_data(
    level='schools',
    source='ccd',
    topic='directory',
    filters={'year': 2020, 'fips': 10}
)

if result is not None:
    print(f"✓ Successfully retrieved {len(result)} records")
else:
    print("✗ Failed to retrieve data")


print("\n" + "=" * 80)
print("Error Handling Tips:")
print("=" * 80)
print("""
1. Always catch specific exceptions (ValidationError, EndpointNotFoundError, etc.)
2. Check for empty DataFrames after successful queries
3. Validate parameters before making API calls
4. Handle network errors gracefully with retries
5. Log errors for debugging in production
6. Check the API documentation for valid endpoints:
   https://educationdata.urban.org/documentation/

Common Issues:
- Invalid level/source/topic combinations → Check API docs
- 404 errors → Endpoint doesn't exist or wrong parameters
- Empty results → Filters too restrictive or no data for that combination
- Connection timeouts → API may be slow, increase timeout or retry
""")
