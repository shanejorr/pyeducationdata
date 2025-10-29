"""Example: Working with college/university data (IPEDS).

This example demonstrates:
- Accessing postsecondary education data
- Different level/source/topic combinations
- Working with college-specific variables
"""


import pyeducationdata as ped

print("=" * 80)
print("College/University Data Examples (IPEDS)")
print("=" * 80)

# Example 1: College directory information
print("\n" + "-" * 80)
print("Example 1: College Directory Data for Connecticut")
print("-" * 80)

try:
    colleges = ped.get_education_data(
        level='college-university',
        source='ipeds',
        topic='directory',
        filters={
            'year': 2021,
            'fips': 9  # Connecticut
        }
    )

    print(f"\n✓ Retrieved {len(colleges)} institutions")

    if not colleges.empty:
        print(f"\nColumns available: {len(colleges.columns)}")
        print(f"Sample columns: {', '.join(colleges.columns[:10])}")

        # Show some institutions
        if 'inst_name' in colleges.columns:
            print("\nSample institutions:")
            for _idx, row in colleges.head(5).iterrows():
                name = row.get('inst_name', 'Unknown')
                city = row.get('city', 'Unknown')
                print(f"  - {name} ({city})")

except Exception as e:
    print(f"\n✗ Error: {e}")


# Example 2: College enrollment data
print("\n" + "-" * 80)
print("Example 2: College Fall Enrollment")
print("-" * 80)

try:
    # Note: IPEDS uses 'fall-enrollment' not just 'enrollment'
    # and requires level_of_study in the path (e.g., undergraduate, graduate)
    enrollment = ped.get_education_data(
        level='college-university',
        source='ipeds',
        topic='fall-enrollment',
        subtopic=['undergraduate', 'race', 'sex'],
        filters={
            'year': 2020,  # 2021 may not be available yet
            'fips': 9  # Connecticut
        }
    )

    print(f"\n✓ Retrieved {len(enrollment)} records")

    if not enrollment.empty:
        print(f"\nAvailable columns: {', '.join(enrollment.columns[:10])}")

        # Summarize by level if possible
        if 'enrolled' in enrollment.columns:
            total = enrollment['enrolled'].sum()
            print(f"\nTotal undergraduate enrollment: {total:,} students")
        elif 'enrollment' in enrollment.columns:
            total = enrollment['enrollment'].sum()
            print(f"\nTotal undergraduate enrollment: {total:,} students")

except Exception as e:
    print(f"\n✗ Error: {e}")
    print("\nNote: IPEDS endpoints use specific structures like 'fall-enrollment'.")
    print("Check the API documentation for available endpoints.")


# Example 3: Aggregate fall enrollment data locally
print("\n" + "-" * 80)
print("Example 3: Analyzing Fall Enrollment Data")
print("-" * 80)

try:
    # Using the fall-enrollment data we already fetched in Example 2
    print("\nNote: For IPEDS data, aggregate locally using pandas.")
    print("This gives you flexibility and avoids API endpoint limitations.")

    # Get a smaller dataset for demonstration
    enrollment = ped.get_education_data(
        level='college-university',
        source='ipeds',
        topic='fall-enrollment',
        subtopic=['undergraduate', 'race', 'sex'],
        filters={
            'year': 2020,
            'fips': 9  # Connecticut
        }
    )

    if not enrollment.empty:
        print(f"\n✓ Retrieved {len(enrollment):,} records")

        # Aggregate by institution
        if 'enrollment_fall' in enrollment.columns and 'unitid' in enrollment.columns:
            institution_totals = enrollment.groupby('unitid')['enrollment_fall'].sum()
            print(f"\nTotal institutions in dataset: {len(institution_totals)}")
            print(f"Total undergraduate fall enrollment: {institution_totals.sum():,.0f}")
            print(f"Average enrollment per institution: {institution_totals.mean():,.0f}")

except Exception as e:
    print(f"\n✗ Error: {e}")


# Example 4: Summary statistics for colleges
print("\n" + "-" * 80)
print("Example 4: Summary - Not Available for Most IPEDS Endpoints")
print("-" * 80)

print("\nNote: Summary endpoints are primarily available for K-12 CCD data.")
print("For IPEDS college data, you typically need to:")
print("  1. Download the full dataset using get_education_data()")
print("  2. Aggregate locally using pandas groupby() and sum()")
print("\nExample aggregation approach:")
print("  df = ped.get_education_data(...)")
print("  state_totals = df.groupby('fips')['enrolled'].sum()")


print("\n" + "=" * 80)
print("College data examples completed!")
print("=" * 80)
print("\nNote: IPEDS has many endpoints and variables.")
print("Check the API documentation for available options:")
print("https://educationdata.urban.org/documentation/")
