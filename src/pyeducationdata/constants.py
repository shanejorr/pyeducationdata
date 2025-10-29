"""Constants for the pyeducationdata package.

This module contains all constant values used throughout the package,
including API URLs, valid parameter values, and configuration defaults.
"""

# API Configuration
API_BASE_URL = "https://educationdata.urban.org"
API_VERSION = "v1"
API_ENDPOINT = f"{API_BASE_URL}/api/{API_VERSION}"

# Request Configuration
DEFAULT_TIMEOUT = 30  # seconds
MAX_RETRIES = 3
PAGE_SIZE_LIMIT = 10000  # API maximum records per page

# Valid Parameter Values
VALID_LEVELS = ["schools", "school-districts", "college-university"]

# Common data sources by level
SCHOOL_SOURCES = ["ccd", "crdc", "edfacts", "nhgis", "meps"]
DISTRICT_SOURCES = ["ccd", "edfacts", "saipe"]
COLLEGE_SOURCES = ["ipeds", "scorecard", "fsa", "eada", "nacubo", "nccs", "campus-crime", "nhgis"]

# All valid sources (comprehensive list)
VALID_SOURCES = list(set(SCHOOL_SOURCES + DISTRICT_SOURCES + COLLEGE_SOURCES))

# Valid statistics for summary endpoints
VALID_STATISTICS = ["sum", "avg", "mean", "median", "max", "min", "count", "stddev", "variance"]

# Grade values for K-12 endpoints
GRADE_VALUES = {
    "pk": "Pre-kindergarten",
    "1": "Grade 1",
    "2": "Grade 2",
    "3": "Grade 3",
    "4": "Grade 4",
    "5": "Grade 5",
    "6": "Grade 6",
    "7": "Grade 7",
    "8": "Grade 8",
    "9": "Grade 9",
    "10": "Grade 10",
    "11": "Grade 11",
    "12": "Grade 12",
    "13": "Grade 13",
    "14": "Adult education",
    "15": "Ungraded",
    "16": "K-12 total",
    "20": "Grades 7-8 combined",
    "21": "Grades 9-10 combined",
    "22": "Grades 11-12 combined",
    "99": "Total all grades",
}

# Level of study values for college endpoints
LEVEL_OF_STUDY_VALUES = {
    "undergraduate": "Undergraduate students",
    "graduate": "Graduate students",
    "first-professional": "First-professional (law, medicine, etc.)",
}

# Common filter variables
MAIN_FILTERS = ["year", "grade", "fips", "ncessch", "leaid", "unitid"]

# State FIPS codes (for reference and validation)
STATE_FIPS = {
    1: "Alabama", 2: "Alaska", 4: "Arizona", 5: "Arkansas", 6: "California",
    8: "Colorado", 9: "Connecticut", 10: "Delaware", 11: "District of Columbia",
    12: "Florida", 13: "Georgia", 15: "Hawaii", 16: "Idaho", 17: "Illinois",
    18: "Indiana", 19: "Iowa", 20: "Kansas", 21: "Kentucky", 22: "Louisiana",
    23: "Maine", 24: "Maryland", 25: "Massachusetts", 26: "Michigan",
    27: "Minnesota", 28: "Mississippi", 29: "Missouri", 30: "Montana",
    31: "Nebraska", 32: "Nevada", 33: "New Hampshire", 34: "New Jersey",
    35: "New Mexico", 36: "New York", 37: "North Carolina", 38: "North Dakota",
    39: "Ohio", 40: "Oklahoma", 41: "Oregon", 42: "Pennsylvania",
    44: "Rhode Island", 45: "South Carolina", 46: "South Dakota", 47: "Tennessee",
    48: "Texas", 49: "Utah", 50: "Vermont", 51: "Virginia", 53: "Washington",
    54: "West Virginia", 55: "Wisconsin", 56: "Wyoming", 60: "American Samoa",
    66: "Guam", 69: "Northern Mariana Islands", 72: "Puerto Rico",
    78: "Virgin Islands"
}

# CSV download base URL
CSV_DOWNLOAD_URL = f"{API_BASE_URL}/csv"

# Metadata endpoints
METADATA_ENDPOINTS = {
    "endpoints": f"{API_ENDPOINT}/api-endpoints/",
    "variables": f"{API_ENDPOINT}/api-variables/",
    "endpoint_varlist": f"{API_ENDPOINT}/api-endpoint-varlist/",
    "downloads": f"{API_ENDPOINT}/api-downloads/",
    "changes": f"{API_ENDPOINT}/api-changes/",
}

# HTTP Headers
DEFAULT_HEADERS = {
    "User-Agent": "pyeducationdata/0.1.0 (Python)",
    "Accept": "application/json",
}

# Data type mappings for pandas
PANDAS_DTYPES = {
    "year": "int64",
    "fips": "int64",
    "ncessch": "str",
    "leaid": "str",
    "unitid": "int64",
    "enrollment": "float64",
}
