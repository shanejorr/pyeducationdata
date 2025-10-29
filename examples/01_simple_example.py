"""Simple example demonstrating basic package usage.

This is the simplest possible example to verify the package works.
Run this first to test your installation.
"""

import pyeducationdata as ped

print("=" * 80)
print("Simple Example: Getting School Directory Data")
print("=" * 80)

# Get basic school directory information for one state
# This is a simple query that should return quickly
print("\nFetching directory data for schools in Delaware (FIPS=10) for 2020...")

try:
    schools = ped.get_education_data(
        level='schools',
        source='ccd',
        topic='directory',
        filters={
            'year': 2020,
            'fips': 10  # Delaware (small state for quick testing)
        }
    )

    print(f"\n✓ Successfully retrieved {len(schools):,} schools")
    print(f"\nColumns available: {len(schools.columns)} columns")
    print(f"First 5 column names: {', '.join(schools.columns[:5])}")

    print("\nFirst 3 schools:")
    print(schools[['ncessch', 'school_name', 'city_location', 'state_location']].head(3).to_string())

    print("\n✓ Example completed successfully!")

except Exception as e:
    print(f"\n✗ Error: {e}")
    print("\nIf you see a connection error, check your internet connection.")
    print("If you see a 404 error, the endpoint may not be available.")
