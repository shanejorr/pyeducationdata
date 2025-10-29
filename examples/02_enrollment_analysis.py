"""Example: Analyzing school enrollment data with filters.

This example demonstrates:
- Using filters to narrow down data
- Working with grade-level data
- Basic data analysis with pandas
"""

import pandas as pd

import pyeducationdata as ped

print("=" * 80)
print("Enrollment Analysis Example")
print("=" * 80)

# Example 1: Get enrollment for all high school grades in a state
print("\n" + "-" * 80)
print("Example 1: High School Enrollment in Rhode Island")
print("-" * 80)

try:
    # Note: Enrollment endpoints require grade in the URL path
    # For multiple grades, we need to fetch each grade separately and combine
    grades = [9, 10, 11, 12]
    all_enrollment = []

    for grade in grades:
        grade_data = ped.get_education_data(
            level='schools',
            source='ccd',
            topic='enrollment',
            subtopic=[f'grade-{grade}'],  # Grade must be in the path
            filters={
                'year': 2020,
                'fips': 44,  # Rhode Island
            }
        )
        if not grade_data.empty:
            all_enrollment.append(grade_data)

    if all_enrollment:
        enrollment = pd.concat(all_enrollment, ignore_index=True)
        print(f"\n✓ Retrieved {len(enrollment):,} records")

        # Analyze by grade
        print("\nEnrollment by grade:")
        grade_totals = enrollment.groupby('grade')['enrollment'].sum().sort_index()
        for grade, total in grade_totals.items():
            print(f"  Grade {grade:2d}: {total:>8,} students")

        print(f"\nTotal high school enrollment: {enrollment['enrollment'].sum():,} students")
        print(f"Number of schools: {enrollment['ncessch'].nunique():,}")
    else:
        print("\n✗ No enrollment data found")

except Exception as e:
    print(f"\n✗ Error: {e}")


# Example 2: Compare enrollment across multiple years
print("\n" + "-" * 80)
print("Example 2: Enrollment Trends (2018-2020)")
print("-" * 80)

try:
    # Note: For total enrollment (all grades), use grade-99
    # For multiple years, we need to fetch each year separately
    years = [2018, 2019, 2020]
    all_trends = []

    for year in years:
        year_data = ped.get_education_data(
            level='schools',
            source='ccd',
            topic='enrollment',
            subtopic=['grade-99'],  # All grades total
            filters={
                'year': year,
                'fips': 44,  # Rhode Island
            }
        )
        if not year_data.empty:
            all_trends.append(year_data)

    if all_trends:
        trends = pd.concat(all_trends, ignore_index=True)
        print(f"\n✓ Retrieved {len(trends):,} records")

        print("\nTotal enrollment by year:")
        yearly = trends.groupby('year')['enrollment'].sum().sort_index()
        for year, total in yearly.items():
            print(f"  {year}: {total:>8,} students")

        # Calculate year-over-year change
        if len(yearly) > 1:
            pct_change = ((yearly.iloc[-1] - yearly.iloc[0]) / yearly.iloc[0])
            pct_change *= 100
            print(f"\nChange 2018-2020: {pct_change:+.2f}%")
    else:
        print("\n✗ No enrollment data found")

except Exception as e:
    print(f"\n✗ Error: {e}")


# Example 3: Filter by specific schools
print("\n" + "-" * 80)
print("Example 3: School-Specific Data")
print("-" * 80)

try:
    # First get directory to find some school IDs
    directory = ped.get_education_data(
        level='schools',
        source='ccd',
        topic='directory',
        filters={'year': 2020, 'fips': 44}
    )

    if not directory.empty:
        # Get first 3 schools
        sample_schools = directory.head(3)
        print("\nSample schools:")
        for _, school in sample_schools.iterrows():
            city = school.get('city_location', school.get('city', 'Unknown'))
            print(f"  - {school['school_name']} ({city})")

except Exception as e:
    print(f"\n✗ Error: {e}")

print("\n" + "=" * 80)
print("Analysis completed!")
print("=" * 80)
