"""Example: Using summary statistics endpoints.

This example demonstrates:
- Checking if summary endpoints are available
- Alternative: Aggregating data locally with pandas
- Working with directory data that supports simpler aggregation
"""

import pyeducationdata as ped
import pandas as pd

print("=" * 80)
print("Summary Statistics Examples")
print("=" * 80)

print("\n" + "=" * 80)
print("IMPORTANT NOTE:")
print("=" * 80)
print("Summary endpoints (with /summaries/) are not widely available in the API.")
print("For enrollment and other detailed data, use get_education_data() and")
print("aggregate locally with pandas. This gives you more control and reliability.")
print("=" * 80)

# Example 1: Local aggregation approach (RECOMMENDED)
print("\n" + "-" * 80)
print("Example 1: Get Data and Aggregate Locally (RECOMMENDED)")
print("-" * 80)

try:
    print("\nFetching school directory data for analysis...")
    print("Note: Fetching each state separately and combining results...")

    # Fetch each state separately (API doesn't properly handle multiple FIPS in one request)
    state_names = {6: 'California', 36: 'New York', 48: 'Texas'}
    all_schools = []

    for fips in [6, 36, 48]:  # CA, NY, TX
        state_data = ped.get_education_data(
            level='schools',
            source='ccd',
            topic='directory',
            filters={'year': 2020, 'fips': fips}
        )
        if not state_data.empty:
            all_schools.append(state_data)

    if all_schools:
        schools = pd.concat(all_schools, ignore_index=True)
        print(f"\n✓ Retrieved {len(schools):,} schools total")

        # Aggregate by state
        schools_by_state = schools.groupby('fips').size().sort_values(ascending=False)
        print("\nNumber of schools by state:")
        for fips, count in schools_by_state.items():
            state_name = state_names.get(fips, f'FIPS {fips}')
            print(f"  {state_name}: {count:,} schools")
    else:
        print("\n✗ No data retrieved")

except Exception as e:
    print(f"\n✗ Error: {e}")


# Example 2: Analyzing enrollment data locally
print("\n" + "-" * 80)
print("Example 2: Enrollment Analysis with Local Aggregation")
print("-" * 80)

try:
    print("\nFetching enrollment data for grade 9 in Rhode Island...")
    enrollment = ped.get_education_data(
        level='schools',
        source='ccd',
        topic='enrollment',
        subtopic=['grade-9'],
        filters={'year': 2020, 'fips': 44}  # Rhode Island
    )

    if not enrollment.empty:
        print(f"\n✓ Retrieved {len(enrollment):,} records")

        # Calculate statistics
        total_enrollment = enrollment['enrollment'].sum()
        avg_enrollment = enrollment['enrollment'].mean()
        schools_count = len(enrollment)

        print(f"\nGrade 9 Statistics for Rhode Island:")
        print(f"  Total students: {total_enrollment:,}")
        print(f"  Number of schools: {schools_count:,}")
        print(f"  Average per school: {avg_enrollment:.1f}")

except Exception as e:
    print(f"\n✗ Error: {e}")


# Example 3: Why local aggregation is better
print("\n" + "-" * 80)
print("Example 3: Benefits of Local Aggregation")
print("-" * 80)

print("\nWhy aggregate locally instead of using summary endpoints?")
print("  1. More reliable - doesn't depend on API summary support")
print("  2. More flexible - use any pandas operation")
print("  3. Better control - filter and transform data as needed")
print("  4. Works with all endpoints - not limited to specific topics")
print("\nExample code pattern:")
print("  df = ped.get_education_data(level='schools', source='ccd',")
print("                               topic='directory', filters={...})")
print("  summary = df.groupby('fips').agg({")
print("      'school_id': 'count',")
print("      'some_column': 'sum'")
print("  })")
print("\n✓ This approach works consistently across all data types!")


print("\n" + "=" * 80)
print("Summary statistics examples completed!")
print("=" * 80)
print("\nKey Takeaway: While the API theoretically supports /summaries/ endpoints,")
print("they are not reliably available for all data types. The recommended approach")
print("is to use get_education_data() and aggregate locally with pandas, which gives")
print("you full control and works consistently across all endpoints.")
