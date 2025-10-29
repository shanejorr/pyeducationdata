"""Basic usage examples for pyeducationdata.

This script demonstrates common usage patterns for the pyeducationdata package.
Run this after installing the package to verify it's working correctly.
"""

import pyeducationdata as ped


def example_1_school_directory():
    """Example 1: Get school directory information."""
    print("=" * 80)
    print("Example 1: School Directory Data for California (2020)")
    print("=" * 80)

    # Get directory information for schools in California
    schools = ped.get_education_data(
        level="schools",
        source="ccd",
        topic="directory",
        filters={"year": 2020, "fips": 6},  # fips=6 is California
    )

    print(f"\nRetrieved {len(schools):,} schools")
    print(f"\nColumns: {', '.join(schools.columns[:10])}...")
    print("\nFirst few records:")
    print(schools[["school_name", "city", "charter", "latitude", "longitude"]].head())


def example_2_enrollment_by_demographics():
    """Example 2: Get enrollment data with demographic breakdowns."""
    print("\n" + "=" * 80)
    print("Example 2: Enrollment by Race and Sex for High Schools in Georgia")
    print("=" * 80)

    # Get enrollment by race and sex for high school grades
    enrollment = ped.get_education_data(
        level="schools",
        source="ccd",
        topic="enrollment",
        subtopic=["race", "sex"],
        filters={
            "year": 2020,
            "grade": [9, 10, 11, 12],  # High school grades
            "fips": 13,  # Georgia
        },
    )

    print(f"\nRetrieved {len(enrollment):,} records")
    print("\nTotal enrollment by grade:")
    print(enrollment.groupby("grade")["enrollment"].sum())


def example_3_summary_statistics():
    """Example 3: Get summary statistics."""
    print("\n" + "=" * 80)
    print("Example 3: State-Level Enrollment Totals (Top 10 States)")
    print("=" * 80)

    # Get state-level enrollment totals
    state_totals = ped.get_education_data_summary(
        level="schools",
        source="ccd",
        topic="enrollment",
        stat="sum",
        var="enrollment",
        by="fips",
        filters={"year": 2020},
    )

    print("\nTop 10 states by enrollment:")
    top_states = state_totals.nlargest(10, "enrollment")
    print(top_states)


def example_4_college_data():
    """Example 4: Get college/university data."""
    print("\n" + "=" * 80)
    print("Example 4: IPEDS College Directory Data")
    print("=" * 80)

    # Get college directory data
    colleges = ped.get_education_data(
        level="college-university", source="ipeds", topic="directory", filters={"year": 2023}
    )

    print(f"\nRetrieved {len(colleges):,} institutions")
    print(f"\nColumns: {', '.join(colleges.columns[:10])}...")


def example_5_multi_year_trends():
    """Example 5: Analyze trends across multiple years."""
    print("\n" + "=" * 80)
    print("Example 5: Enrollment Trends 2015-2020 in Illinois")
    print("=" * 80)

    # Get enrollment data for multiple years
    trends = ped.get_education_data(
        level="schools",
        source="ccd",
        topic="enrollment",
        filters={
            "year": [2015, 2016, 2017, 2018, 2019, 2020],
            "grade": 99,  # Total all grades
            "fips": 17,  # Illinois
        },
    )

    print(f"\nRetrieved {len(trends):,} records")
    print("\nYearly total enrollment:")
    yearly = trends.groupby("year")["enrollment"].sum()
    for year, total in yearly.items():
        print(f"  {year}: {total:,}")


def main():
    """Run all examples."""
    print("\n" + "=" * 80)
    print("pyeducationdata Usage Examples")
    print("=" * 80)
    print(
        "\nThese examples demonstrate basic usage of the pyeducationdata package."
        "\nNote: Examples make real API calls and may take a moment to complete."
        "\n"
    )

    try:
        # Run examples
        example_1_school_directory()
        example_2_enrollment_by_demographics()
        example_3_summary_statistics()
        example_4_college_data()
        example_5_multi_year_trends()

        print("\n" + "=" * 80)
        print("All examples completed successfully!")
        print("=" * 80)

    except Exception as e:
        print(f"\n\nError running examples: {e}")
        print(
            "\nIf you're seeing connection errors, check your internet connection "
            "and that the Education Data Portal API is accessible."
        )
        raise


if __name__ == "__main__":
    main()
