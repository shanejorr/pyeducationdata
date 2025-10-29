# Urban Institute Education Data Portal API: Complete Tutorial

The Urban Institute's Education Data Portal API provides comprehensive access to decades of US education data from kindergarten through postsecondary education. This open, free-to-use API aggregates data from multiple federal sources into a unified, standardized interface.

## Overview and getting started

The Education Data Portal API is a **REST-based API** built on Django REST Framework that returns data in **JSON format**. The API requires **no authentication, registration, or API keys**—all endpoints are publicly accessible. Data is licensed under the **Open Data Commons Attribution License (ODC-By) v1.0**, requiring proper attribution when used.

**Base URL:** `https://educationdata.urban.org/api/v1/`

**Official Documentation:** https://educationdata.urban.org/documentation/

**Technical specifications:**
- Response format: JSON (all endpoints)
- API version: v1 (current)
- Data portal version: 0.23.0
- Technology: Django REST Framework with PostgreSQL database
- No special requirements beyond standard HTTP capabilities

## API structure and architecture

All API requests follow a hierarchical URL structure with consistent patterns across endpoints:

```
https://educationdata.urban.org/api/v1/{level}/{source}/{topic}/{year}/[specifiers]/[filters]
```

**URL components:**
- **level**: Geographic/institutional level (schools, school-districts, college-university)
- **source**: Data source (ccd, crdc, ipeds, edfacts, saipe, scorecard, etc.)
- **topic**: Specific dataset (directory, enrollment, finance, etc.)
- **year**: Academic year (required for most endpoints)
- **specifiers**: Optional disaggregation parameters (grade, race, sex combinations)
- **filters**: Query string parameters for filtering results

**Example URLs:**
```
https://educationdata.urban.org/api/v1/schools/ccd/directory/2020/
https://educationdata.urban.org/api/v1/schools/ccd/enrollment/2013/grade-3/?charter=1&fips=11
https://educationdata.urban.org/api/v1/college-university/ipeds/directory/2023/
```

The API organizes education data into three main levels, each containing data from multiple federal sources.

## Complete list of API endpoints

The Education Data Portal includes approximately **160+ unique data endpoints** across all three institutional levels.

### Schools endpoints (K-12 school level)

**Common Core of Data (CCD) - Years: 1986-2023**

- `/schools/ccd/directory/{year}` - School names, addresses, characteristics, charter/magnet status, grade levels, operational status, school type, Title I status, virtual school indicators
- `/schools/ccd/enrollment/{year}/{grade}` - Total enrollment by grade (PK through grade 12, ungraded, totals)
- `/schools/ccd/enrollment/race/{year}/{grade}` - Enrollment by race/ethnicity and grade
- `/schools/ccd/enrollment/race-sex/{year}/{grade}` - Enrollment by race, sex, and grade
- `/schools/ccd/enrollment/sex/{year}/{grade}` - Enrollment by sex and grade

**Civil Rights Data Collection (CRDC) - Years: 2011, 2013, 2015, 2017, 2020**

*Enrollment:*
- `/schools/crdc/directory/{year}` - CRDC school directory information
- `/schools/crdc/enrollment/disability-sex/{year}` - Enrollment by disability status and sex
- `/schools/crdc/enrollment/lep-sex/{year}` - Limited English Proficient (LEP) enrollment by sex
- `/schools/crdc/enrollment/race-sex/{year}` - Enrollment by race and sex

*Advanced coursework:*
- `/schools/crdc/algebra1/disability-sex/{year}` - Algebra 1 enrollment by disability and sex
- `/schools/crdc/algebra1/lep-sex/{year}` - Algebra 1 enrollment by LEP status and sex
- `/schools/crdc/algebra1/race-sex/{year}` - Algebra 1 enrollment by race and sex
- `/schools/crdc/ap-exams/disability-sex/{year}` - AP exam participation by disability and sex
- `/schools/crdc/ap-exams/lep-sex/{year}` - AP exam participation by LEP status and sex
- `/schools/crdc/ap-exams/race-sex/{year}` - AP exam participation by race and sex
- `/schools/crdc/ap-ib-enrollment/disability-sex/{year}` - AP/IB course enrollment by disability and sex
- `/schools/crdc/ap-ib-enrollment/lep-sex/{year}` - AP/IB course enrollment by LEP status and sex
- `/schools/crdc/ap-ib-enrollment/race-sex/{year}` - AP/IB course enrollment by race and sex
- `/schools/crdc/math-and-science/disability-sex/{year}` - Advanced math/science enrollment by disability and sex
- `/schools/crdc/math-and-science/lep-sex/{year}` - Advanced math/science enrollment by LEP status and sex
- `/schools/crdc/math-and-science/race-sex/{year}` - Advanced math/science enrollment by race and sex

*Discipline and safety:*
- `/schools/crdc/discipline-instances/{year}` - Total discipline instances by type
- `/schools/crdc/discipline/disability-lep-sex/{year}` - Discipline by disability, LEP, and sex
- `/schools/crdc/discipline/disability-race-sex/{year}` - Discipline by disability, race, and sex
- `/schools/crdc/discipline/disability-sex/{year}` - Discipline by disability and sex (in-school suspensions, out-of-school suspensions, expulsions, corporal punishment, law enforcement referrals, arrests)
- `/schools/crdc/restraint-and-seclusion/disability-lep-sex/{year}` - Restraint/seclusion by disability, LEP, and sex
- `/schools/crdc/restraint-and-seclusion/disability-race-sex/{year}` - Restraint/seclusion by disability, race, and sex
- `/schools/crdc/restraint-and-seclusion/disability-sex/{year}` - Restraint/seclusion by disability and sex
- `/schools/crdc/restraint-and-seclusion/instances/{year}` - Total restraint and seclusion instances
- `/schools/crdc/harassment-or-bullying/allegations/{year}` - Harassment/bullying allegations
- `/schools/crdc/harassment-or-bullying/disability-sex/{year}` - Harassment/bullying by disability and sex
- `/schools/crdc/harassment-or-bullying/lep-sex/{year}` - Harassment/bullying by LEP status and sex
- `/schools/crdc/harassment-or-bullying/race-sex/{year}` - Harassment/bullying by race and sex
- `/schools/crdc/offenses/{year}` - School offenses and incidents

*Other outcomes:*
- `/schools/crdc/chronic-absenteeism/disability-sex/{year}` - Chronic absenteeism by disability and sex
- `/schools/crdc/chronic-absenteeism/lep-sex/{year}` - Chronic absenteeism by LEP status and sex
- `/schools/crdc/chronic-absenteeism/race-sex/{year}` - Chronic absenteeism by race and sex
- `/schools/crdc/retention/disability-sex/{year}/{grade}` - Grade retention by disability and sex
- `/schools/crdc/retention/lep-sex/{year}/{grade}` - Grade retention by LEP status and sex
- `/schools/crdc/retention/race-sex/{year}/{grade}` - Grade retention by race and sex
- `/schools/crdc/sat-act-participation/disability-sex/{year}` - SAT/ACT participation by disability and sex
- `/schools/crdc/sat-act-participation/lep-sex/{year}` - SAT/ACT participation by LEP status and sex
- `/schools/crdc/sat-act-participation/race-sex/{year}` - SAT/ACT participation by race and sex
- `/schools/crdc/dual-enrollment/disability-sex/{year}` - Dual enrollment by disability and sex
- `/schools/crdc/dual-enrollment/lep-sex/{year}` - Dual enrollment by LEP status and sex
- `/schools/crdc/dual-enrollment/race-sex/{year}` - Dual enrollment by race and sex

*School characteristics:*
- `/schools/crdc/teachers-staff/{year}` - Teacher and staff characteristics
- `/schools/crdc/school-finance/{year}` - School-level finance data
- `/schools/crdc/offerings/{year}` - Course and program offerings
- `/schools/crdc/credit-recovery/{year}` - Credit recovery program data
- `/schools/crdc/internet-access/{year}` - School internet access indicators
- `/schools/crdc/covid-indicators/{year}` - COVID-19 related school indicators (2020 only)
- `/schools/crdc/suspensions-days/disability-sex/{year}` - Suspension days by disability and sex
- `/schools/crdc/suspensions-days/lep-sex/{year}` - Suspension days by LEP status and sex
- `/schools/crdc/suspensions-days/race-sex/{year}` - Suspension days by race and sex

**EdFacts - Years: 2009-2020**

- `/schools/edfacts/assessments/{year}/{grade_edfacts}` - State assessment proficiency rates
- `/schools/edfacts/assessments/race/{year}/{grade_edfacts}` - Assessments by race
- `/schools/edfacts/assessments/sex/{year}/{grade_edfacts}` - Assessments by sex
- `/schools/edfacts/assessments/special-populations/{year}/{grade_edfacts}` - Assessments by special populations
- `/schools/edfacts/grad-rates/{year}` - School graduation rates (4-year adjusted cohort)

**National Historical Geographic Information System (NHGIS) - Years: 1986-2023**

- `/schools/nhgis/census-1990/{year}` - 1990 Census data for school locations
- `/schools/nhgis/census-2000/{year}` - 2000 Census data for school locations
- `/schools/nhgis/census-2010/{year}` - 2010 Census data for school locations

**MEPS (Monitoring Educational Progress) - Years: 2013-2020**

- `/schools/meps/{year}` - School environment data

### School districts endpoints (K-12 district level)

**Common Core of Data (CCD) - Years: 1986-2023**

- `/school-districts/ccd/directory/{year}` - District identifiers, names, addresses, district type, number of schools, grade span, operational status
- `/school-districts/ccd/enrollment/{year}/{grade}` - Total district enrollment by grade
- `/school-districts/ccd/enrollment/race/{year}/{grade}` - District enrollment by race and grade
- `/school-districts/ccd/enrollment/race-sex/{year}/{grade}` - District enrollment by race, sex, and grade
- `/school-districts/ccd/enrollment/sex/{year}/{grade}` - District enrollment by sex and grade
- `/school-districts/ccd/finance/{year}` - District revenues and expenditures (1991, 1994-2020)

**EdFacts - Years: 2009-2020**

- `/school-districts/edfacts/assessments/{year}/{grade_edfacts}` - District assessment results
- `/school-districts/edfacts/assessments/race/{year}/{grade_edfacts}` - District assessments by race
- `/school-districts/edfacts/assessments/sex/{year}/{grade_edfacts}` - District assessments by sex
- `/school-districts/edfacts/assessments/special-populations/{year}/{grade_edfacts}` - District assessments by special populations
- `/school-districts/edfacts/grad-rates/{year}` - District graduation rates (2010-2019)

**Small Area Income and Poverty Estimates (SAIPE) - Years: 1995-2023**

- `/school-districts/saipe/{year}` - Poverty estimates for school-age children, median household income

### College and university endpoints (higher education)

**Integrated Postsecondary Education Data System (IPEDS) - Years: 1980-2023**

*Institutional characteristics:*
- `/college-university/ipeds/directory/{year}` - Institution identifiers, names, locations, control (public/private), level (2-year/4-year), Carnegie classification, HBCU/HSI/Tribal College indicators, religious affiliation, land grant status
- `/college-university/ipeds/institutional-characteristics/{year}` - Calendar system, academic offerings, characteristics

*Admissions and enrollment:*
- `/college-university/ipeds/admissions-enrollment/{year}` - Applications, acceptances, enrollments, SAT/ACT scores, yield rates
- `/college-university/ipeds/admissions-requirements/{year}` - Admission test requirements and policies
- `/college-university/ipeds/fall-enrollment/age/{year}/{level_of_study}` - Fall enrollment by age and sex (1991-2020)
- `/college-university/ipeds/fall-enrollment/race/{year}/{level_of_study}` - Fall enrollment by race and sex (1986-2020)
- `/college-university/ipeds/fall-enrollment/residence/{year}` - Fall enrollment by state of residence (in-state vs. out-of-state)
- `/college-university/ipeds/enrollment-headcount/{year}/{level_of_study}` - Headcount enrollment (1996-2021)
- `/college-university/ipeds/enrollment-full-time-equivalent/{year}/{level_of_study}` - FTE enrollment (1997-2021)
- `/college-university/ipeds/fall-retention/{year}` - First-year retention rates (2003-2020)

*Completions and outcomes:*
- `/college-university/ipeds/completers/{year}` - Number of students who completed programs (2011-2022)
- `/college-university/ipeds/completions-cip-2/{year}` - Degrees/certificates by 2-digit CIP code (1991-2022)
- `/college-university/ipeds/completions-cip-6/{year}` - Degrees/certificates by 6-digit CIP code (1983-2022)
- `/college-university/ipeds/grad-rates/{year}` - 150% graduation rates (6-year for bachelors) (1996-2017)
- `/college-university/ipeds/grad-rates-200pct/{year}` - 200% graduation rates (8-year) (2007-2017)
- `/college-university/ipeds/grad-rates-pell/{year}` - Graduation rates for Pell Grant recipients (2015-2017)
- `/college-university/ipeds/outcome-measures/{year}` - 8-year outcome measures for various cohorts (2015-2021)

*Finance and costs:*
- `/college-university/ipeds/finance/{year}` - Revenues, expenditures, assets, endowments (1979, 1983-2017)
- `/college-university/ipeds/academic-year-tuition/{year}` - Standard tuition and fees (1986-2021)
- `/college-university/ipeds/academic-year-tuition-prof-program/{year}` - Professional program tuition (1986-2021)
- `/college-university/ipeds/academic-year-room-board-other/{year}` - Room, board, and other expenses (1999-2021)
- `/college-university/ipeds/program-year-room-board-other/{year}` - Room and board for program-length years (1999-2021)
- `/college-university/ipeds/program-year-tuition-cip/{year}` - Tuition by CIP code program (1987-2021)

*Financial aid:*
- `/college-university/ipeds/sfa-all-undergraduates/{year}` - Financial aid for all undergraduates (2007-2021)
- `/college-university/ipeds/sfa-by-living-arrangement/{year}` - Financial aid by living arrangement (2008-2021)
- `/college-university/ipeds/sfa-by-tuition-type/{year}` - Financial aid by in-state/out-of-state status (1999-2021)
- `/college-university/ipeds/sfa-ftft/{year}` - Aid for first-time, full-time students (1999-2021)
- `/college-university/ipeds/sfa-grants-and-net-price/{year}` - Grant aid and net price (2008-2021)

*Faculty and staff:*
- `/college-university/ipeds/salaries-instructional-staff/{year}` - Instructional staff salaries (1980-2022)
- `/college-university/ipeds/salaries-noninstructional-staff/{year}` - Noninstructional staff salaries (2012-2022)
- `/college-university/ipeds/student-faculty-ratio/{year}` - Student-to-faculty ratios (2009-2020)

*Other:*
- `/college-university/ipeds/academic-libraries/{year}` - Library collections, services, expenses (2013-2020)

**College Scorecard - Years: 1996-2020**

- `/college-university/scorecard/institutional-characteristics/{year}` - Scorecard institutional characteristics
- `/college-university/scorecard/student-characteristics/aid-applicants/{year}` - Characteristics of aid applicants (1997-2016)
- `/college-university/scorecard/student-characteristics/home-neighborhood/{year}` - Home neighborhood characteristics (1997-2016)
- `/college-university/scorecard/earnings/{year}` - Post-graduation earnings (1, 2, 3, 4, 6, 8, 10 years after completion) (2003-2014, 2018)
- `/college-university/scorecard/repayment/{year}` - Loan repayment rates (2007-2016)
- `/college-university/scorecard/default/{year}` - Student loan default rates (1996-2020)

**Federal Student Aid (FSA)**

- `/college-university/fsa/90-10-revenue-percentages/{year}` - 90/10 revenue rule for proprietary institutions (2014-2021)
- `/college-university/fsa/campus-based-volume/{year}` - Campus-based federal aid programs (2001-2021)
- `/college-university/fsa/financial-responsibility/{year}` - Financial responsibility composite scores (2006-2016)
- `/college-university/fsa/grants/{year}` - Federal grant awards (1999-2021)
- `/college-university/fsa/loans/{year}` - Federal student loan volume (1999-2021)

**Other college sources:**

- `/college-university/campus-crime/hate-crimes/{year}` - Hate crimes on campuses (2005-2021)
- `/college-university/eada/institutional-characteristics/{year}` - Athletic department data (2002-2021)
- `/college-university/nacubo/endowments/{year}` - Endowment values and returns (2012-2022)
- `/college-university/nccs/990-forms/{year}` - IRS Form 990 for nonprofit institutions (1993-2016)
- `/college-university/nhgis/census-1990/{year}` - 1990 Census data for college locations
- `/college-university/nhgis/census-2000/{year}` - 2000 Census data for college locations
- `/college-university/nhgis/census-2010/{year}` - 2010 Census data for college locations

### Metadata endpoints

These special endpoints provide information about the API itself:

- `/api/v1/api-endpoints/` - Lists all available endpoints with IDs, URLs, years available
- `/api/v1/api-downloads/` - Lists downloadable CSV files and codebooks
- `/api/v1/api-variables/` - Lists all variables with data types, formats, labels
- `/api/v1/api-endpoint-varlist/` - Lists variables by endpoint
- `/api/v1/api-changes/` - Information about API updates and changes

### Summary endpoints

For all regular data endpoints, summary endpoints provide rapid aggregated statistics:

```
/api/v1/{level}/{source}/{topic}/summaries?var={variable}&stat={statistic}&by={grouping}
```

**Available statistics:** sum, count, avg, min, max, variance, stddev, median

**Example:** 
```
https://educationdata.urban.org/api/v1/schools/ccd/enrollment/summaries?var=enrollment&stat=sum&by=fips
```

## Data availability by category

### School-level data (K-12)

**Directory information:**
- School identifiers (NCESSCH, state/district codes)
- Geographic data (address, latitude/longitude, county, metro/rural classification)
- School characteristics (charter, magnet, Title I status)
- Grade offerings and school level (elementary, middle, secondary)
- Operational status (open, closed, new, reopened)
- School type (regular, special education, vocational, alternative)
- Virtual school indicators

**Enrollment data:**
- Total enrollment by grade (Pre-K through 12, ungraded)
- Disaggregated by race/ethnicity (White, Black, Hispanic, Asian, American Indian/Alaska Native, Native Hawaiian/Pacific Islander, two or more races)
- Disaggregated by sex (male, female)
- Limited English Proficient (LEP) students
- Students with disabilities (IDEA categories)
- Gifted and talented enrollment

**Performance metrics:**
- State assessment proficiency rates (math, reading/ELA, science)
- Performance level distributions (below basic, basic, proficient, advanced)
- Assessment participation rates
- 4-year adjusted cohort graduation rates
- Extended graduation rates (5-year, 6-year)
- All metrics disaggregated by race, sex, disability, LEP, economic disadvantage

**Advanced coursework:**
- AP and IB course enrollment and exam participation
- Algebra I, Algebra II, Geometry, Calculus enrollment
- Advanced math and science courses
- Computer science course access
- SAT/ACT participation rates

**Discipline and safety:**
- In-school suspensions
- Out-of-school suspensions
- Expulsions
- Corporal punishment instances
- Law enforcement referrals
- School-related arrests
- Restraint and seclusion (mechanical, physical, instances)
- Harassment and bullying (by type: race, sex, disability, religion)
- School offenses and incidents

**Attendance and retention:**
- Chronic absenteeism (missing 15+ days)
- Grade retention by grade level
- All disaggregated by race, sex, disability, LEP status

**School environment:**
- Teacher and staff characteristics
- Course and program offerings
- Credit recovery programs
- Dual enrollment opportunities
- Internet access indicators
- COVID-19 indicators (2020)

**Census data at school locations:**
- 1990, 2000, 2010 Census demographic and economic data
- Neighborhood characteristics surrounding schools

### District-level data (K-12)

**Directory information:**
- District identifiers (LEAID, NCES ID, state codes)
- Geographic information
- District type (regular, charter agency, state-operated)
- Number of schools operated
- Grade span offered
- Operational status

**Enrollment data:**
- Total district enrollment by year
- Enrollment by grade
- Enrollment disaggregated by race/ethnicity and sex
- Full demographic breakdowns

**Financial data - Revenue sources:**
- Total revenue by source (federal, state, local)
- Federal revenue breakdown:
  - Title I revenue
  - IDEA (special education) revenue
  - Child Nutrition revenue
  - Other federal programs
- State revenue breakdown:
  - General formula assistance
  - Special education funding
  - Transportation funding
  - Other state sources
- Local revenue breakdown:
  - Property taxes
  - Other local taxes
  - Parent government contributions
  - Other local sources
- Revenue from intermediate sources

**Financial data - Expenditures:**
- Current expenditures total
- Instruction expenditures (salaries, benefits, purchased services, supplies)
- Support services:
  - Student support
  - Instructional staff support
  - General administration
  - School administration
  - Operations and maintenance
  - Student transportation
  - Other support services
- Capital outlay
- Interest on debt
- Other expenditures
- Per-pupil expenditure calculations

**Performance metrics:**
- State assessment proficiency rates (math, reading/ELA)
- Participation rates
- 4-year adjusted cohort graduation rates
- All disaggregated by race, sex, disability, LEP, economic status

**Poverty estimates:**
- Total population in district
- Number of children ages 5-17
- Number of children ages 5-17 in poverty
- Poverty rate for school-age children
- Median household income

### College and university data

**Institutional characteristics:**
- Institution identifiers (UNITID, OPEID)
- Institution name, location, geographic classification
- Control (public, private nonprofit, private for-profit)
- Level (4-year, 2-year, less than 2-year)
- Carnegie classification
- Special designations (HBCU, Hispanic-serving, Tribal College)
- Religious affiliation
- Land grant status
- Calendar system

**Admissions and enrollment:**
- Applications, acceptances, enrolled students
- SAT/ACT scores (25th and 75th percentile)
- Admissions yield rates
- Admissions selectivity and requirements
- Total enrollment (undergraduate, graduate, first-professional)
- Full-time vs. part-time enrollment
- First-time, first-year students
- Enrollment by race/ethnicity and sex
- Enrollment by age bands
- Enrollment by state of residence (in-state vs. out-of-state)
- Full-time equivalent (FTE) enrollment

**Degrees and completions:**
- Degrees and certificates awarded by level (certificate, associate, bachelor's, master's, doctorate, first-professional)
- Completions by field of study (2-digit and 6-digit CIP codes)
- Completions by race/ethnicity and sex
- Distance education completions

**Graduation and retention:**
- First-year retention rates (full-time and part-time)
- 150% graduation rates (6-year for bachelors, 3-year for associates)
- 200% graduation rates (8-year for bachelors)
- Graduation rates by race/ethnicity, sex, Pell recipient status
- Transfer-out rates
- 8-year outcome measures for various cohorts
- Cohort sizes

**Financial data - Revenues:**
- Tuition and fees revenue (gross and net)
- Federal, state, and local appropriations
- Federal, state, and private grants and contracts
- Private gifts
- Investment income and returns
- Sales and services (educational activities, auxiliary enterprises, hospitals)
- Other revenues

**Financial data - Expenses:**
- Instruction expenses
- Research expenses
- Public service expenses
- Academic support
- Student services
- Institutional support
- Operations and maintenance of plant
- Scholarships and fellowships
- Auxiliary enterprises
- Hospital services
- Depreciation

**Financial data - Assets:**
- Total assets and liabilities
- Endowment assets (beginning and ending values)
- Endowment returns

**Costs and tuition:**
- Published tuition and fees (in-state, out-of-state, district)
- Professional program tuition
- Room and board charges
- Books and supplies costs
- Other expenses
- Total cost of attendance

**Student financial aid:**
- Number of students receiving aid
- Average aid amounts
- Federal grants (Pell Grant)
- State and local grants
- Institutional grants
- Federal loans
- Average net price overall
- Net price by family income level (quintiles)
- Typical debt at graduation
- Typical monthly loan payment

**Student outcomes (College Scorecard):**
- Median earnings at 1, 2, 3, 4, 6, 8, 10 years after completion
- Earnings by field of study
- Earnings by credential level
- Loan repayment rates (1, 3, 5, 7 years)
- Cohort default rates (2-year and 3-year)
- Median student debt
- Debt-to-earnings ratios
- Share of borrowers in income-driven repayment
- Share with declining loan balances
- Employment rates

**Student demographics:**
- Dependency status (dependent vs. independent)
- First-generation college students
- Age distribution
- Family income levels
- Pell Grant recipients
- Federal loan recipients
- Home neighborhood characteristics (for aid applicants)

**Faculty and staff:**
- Full-time and part-time staff counts
- Faculty counts by rank
- Instructional staff
- Noninstructional staff
- Salaries by position and rank
- Student-to-faculty ratios

**Other data:**
- Academic library collections, services, and expenses
- Athletic department participation and characteristics
- Campus crime statistics (hate crimes)
- 90/10 revenue percentages (proprietary institutions)
- Campus-based federal aid volume
- Financial responsibility composite scores
- IRS Form 990 data (nonprofit institutions)
- Census data at institution locations

### Student demographic variables

**Race/ethnicity categories (standardized across datasets):**
- White
- Black or African American
- Hispanic or Latino
- Asian
- American Indian or Alaska Native
- Native Hawaiian or Other Pacific Islander
- Two or more races
- Non-resident alien (higher education)
- Race/ethnicity unknown

**Sex/gender:**
- Male
- Female
- Non-binary/other (in newer datasets)

**Other demographic characteristics:**
- Grade level (Pre-K through 12, ungraded, totals)
- Age bands (varies by dataset)
- Limited English Proficiency (LEP) status
- Disability status (IDEA disability categories)
- Economic disadvantage (Free/Reduced-Price Lunch eligibility)
- Gifted and talented status
- Migrant status
- Homeless status
- Foster care status
- Military-connected status
- First-generation college student (higher education)
- Pell Grant recipient (higher education)
- Dependency status (higher education)

### Geographic coverage

**States and territories:**
- All 50 US states plus District of Columbia
- Puerto Rico and other territories (varies by dataset)

**Geographic identifiers:**
- State FIPS codes
- County FIPS codes
- Congressional districts
- Metropolitan/micropolitan statistical areas
- Urbanicity codes (12-category NCES locale classification):
  - City: large, midsize, small
  - Suburb: large, midsize, small
  - Town: fringe, distant, remote
  - Rural: fringe, distant, remote
- Census regions and divisions
- School attendance boundaries (via supplemental data)

### Temporal coverage

**By data source:**
- **Common Core of Data (CCD):** 1986-2023 (38 years of continuous data)
- **Civil Rights Data Collection (CRDC):** 2011, 2013, 2015, 2017, 2020 (biennial collection)
- **IPEDS:** 1980-2023 (45+ years, varies by component)
- **EdFacts:** 2009-2020 (assessment data)
- **SAIPE:** 1995-2023 (annual estimates)
- **College Scorecard:** 1996-2020 (varies by metric)

## Constructing API queries

### Basic query structure

Construct API queries by building URLs with the appropriate path components and query parameters.

**Standard format:**
```
https://educationdata.urban.org/api/v1/{level}/{source}/{topic}/{year}/[specifiers]/?[filters]
```

**Example queries:**

Simple directory request:
```
https://educationdata.urban.org/api/v1/schools/ccd/directory/2020/
```

Enrollment with grade specifier:
```
https://educationdata.urban.org/api/v1/schools/ccd/enrollment/2013/grade-3/
```

With disaggregation specifier:
```
https://educationdata.urban.org/api/v1/schools/ccd/enrollment/race/2020/grade-9/
```

College directory:
```
https://educationdata.urban.org/api/v1/college-university/ipeds/directory/2023/
```

### Grade values for K-12 endpoints

When endpoints require grade specifiers, use these values:

- `grade-pk` - Pre-kindergarten
- `grade-1` through `grade-12` - Individual grades
- `grade-13` - Grade 13 (rare)
- `grade-14` - Adult education
- `grade-15` - Ungraded students
- `grade-16` - K-12 total
- `grade-20` - Grades 7-8 combined
- `grade-21` - Grades 9-10 combined
- `grade-22` - Grades 11-12 combined
- `grade-99` - Total all grades

### Level of study values for college endpoints

For IPEDS endpoints requiring level of study:
- `undergraduate` - Undergraduate students
- `graduate` - Graduate students
- `first-professional` - First-professional (law, medicine, etc.)
- Specific values vary by endpoint; check documentation

## Filtering data

### Filter syntax

Add filters as query string parameters at the end of URLs:

```
?filter_variable=value
```

**Single filter example:**
```
https://educationdata.urban.org/api/v1/schools/ccd/directory/2020?fips=17
```

### Common filter variables

**Geographic filters:**
- `fips` - State FIPS code (e.g., `17` for Illinois, `11` for DC, `6` for California)
- `leaid` - District ID
- `ncessch` - School ID
- `unitid` - College/university IPEDS ID

**Institutional filters:**
- `school_level` - School level code (e.g., `1` for primary, `2` for middle, `3` for high school)
- `charter` - Charter school indicator (`1` for charter, `0` for non-charter)
- `grade` - Grade level
- `race` - Race/ethnicity code
- `sex` - Sex/gender code

**Important:** Available filters vary by endpoint. Check the documentation for each endpoint to see which filters are supported.

### Multiple filter values

Use comma-separated values to match any of the specified values (OR logic):

```
?fips=17,55
?year=2018,2019,2020
?grade=9,10,11,12
```

**Example:**
```
https://educationdata.urban.org/api/v1/schools/ccd/directory/2020?fips=17,55
```
Returns schools in Illinois (17) OR Wisconsin (55).

### Combining multiple filters

Use ampersand (`&`) to combine multiple filters (AND logic):

```
?filter1=value1&filter2=value2
```

**Examples:**

Charter schools in DC:
```
https://educationdata.urban.org/api/v1/schools/ccd/enrollment/2013/grade-3/?charter=1&fips=11
```

High schools in Illinois:
```
https://educationdata.urban.org/api/v1/schools/ccd/directory/2020?school_level=3&fips=17
```

Multiple states and years:
```
?fips=17,55&year=2018,2019,2020
```

**Filter combination logic:**
- Multiple filters with `&` use AND logic (all conditions must be met)
- Multiple values within a filter (comma-separated) use OR logic (any value matches)
- Example: `?fips=17,55&charter=1` means (Illinois OR Wisconsin) AND (charter schools)

### Filtering limitations

**Important filtering constraints:**

1. **Equality-based filtering only** - The API supports only exact matches. There are NO comparison operators like greater than (>), less than (<), not equals (!=), etc.

2. **Endpoint-specific filters** - Only variables listed as filters in the documentation for each endpoint can be used for filtering. Not all variables are filterable.

3. **No custom sorting** - The API does not support sort or order_by parameters. Results are returned in the database's natural order.

4. **Range queries** - For ranges (like multiple years), you must specify all values explicitly using comma-separated format:
   ```
   ?year=2018,2019,2020
   ```
   You cannot use expressions like `year>=2018`.

### Summary endpoint queries

Summary endpoints provide aggregated statistics without downloading raw data:

**Format:**
```
/api/v1/{level}/{source}/{topic}/summaries?var={variable}&stat={statistic}&by={grouping}
```

**Parameters:**
- `var` - Variable to summarize (must be numeric, non-filter variable)
- `stat` - Statistic to calculate (sum, count, avg, min, max, variance, stddev, median)
- `by` - Grouping variable(s), comma-separated for multiple dimensions

**Additional filters can be added using standard filter syntax.**

**Examples:**

Sum of enrollment by state:
```
https://educationdata.urban.org/api/v1/schools/ccd/enrollment/summaries?var=enrollment&stat=sum&by=fips
```

Average enrollment by school level:
```
https://educationdata.urban.org/api/v1/schools/ccd/enrollment/summaries?var=enrollment&stat=avg&by=school_level
```

With filters - sum of enrollment by sex for California, limited to specific races:
```
https://educationdata.urban.org/api/v1/schools/ccd/enrollment/summaries?var=enrollment&stat=sum&by=sex&fips=6&race=1,2
```

Multiple grouping dimensions:
```
https://educationdata.urban.org/api/v1/schools/ccd/enrollment/summaries?var=enrollment&stat=sum&by=fips,race&fips=17,55&year=2018,2019,2020
```

**Benefits of summary endpoints:**
- Orders of magnitude faster than downloading and aggregating raw data
- Pre-joined with directory data, allowing grouping by variables not in the original endpoint
- Reduces data transfer and processing time
- Ideal for dashboards, visualizations, and quick analyses

## Authentication and rate limits

### Authentication requirements

**No authentication required.** The Education Data Portal API is completely open and public:

- No API keys needed
- No registration required
- No authentication tokens
- No login credentials
- Direct access to all endpoints via URL

You can access all data directly in a web browser or through programmatic requests without any authentication mechanism.

### Rate limits and throttling

**Primary rate limit:** 10,000 records per page maximum

**Details:**
- The API limits responses to 10,000 records per page to prevent large requests from degrading performance for other users
- When results exceed 10,000 records, pagination is required (see Pagination section)
- No explicit request-rate limits (requests per minute/hour) are documented
- The primary constraint is the per-page record limit rather than request frequency

**Performance characteristics:**
- 95% of data requests returned within 30 seconds
- 90% of data requests returned within 10 seconds
- 75% of data requests returned within 2 seconds
- 90%+ of requests served from cache

### Usage guidelines and terms of service

**License:** Open Data Commons Attribution License (ODC-By) v1.0
- Data provided "as is" without warranty
- Free to use for commercial and non-commercial purposes
- Requires proper attribution when citing data
- No restrictions with proper attribution

**License URL:** https://opendatacommons.org/licenses/by/1-0/

**Terms of Service:** https://www.urban.org/terms-service

**Liability disclaimer:** The Urban Institute shall not be liable for any claims or damages with respect to any loss arising from use of the datasets.

### Citation requirements

**For research reports, briefs, or academic work:**
```
[dataset names], Education Data Portal (Version 0.23.0), Urban Institute, 
accessed [Month DD, YYYY], https://educationdata.urban.org/documentation/, 
made available under the ODC Attribution License.
```

**For blog posts, data visualizations, or space-constrained work:**
```
[dataset names], via Education Data Portal v. 0.23.0, Urban Institute, 
under ODC Attribution License.
```

### User engagement

The Urban Institute encourages users to:
- Email educationdata@urban.org to notify them of public projects or research using the data
- Provide information on titles and links to published work
- This helps elevate work visibility and support continued funding

## API response structure

### Standard response format

All API endpoints return JSON-formatted responses with a consistent structure:

```json
{
  "results": [ /* array of data records */ ],
  "next": "URL to next page or null"
}
```

**Response components:**

**`results`** - Array containing the actual data records:
- Up to 10,000 records per page
- Each record is a JSON object with field-value pairs
- Fields vary by endpoint

**`next`** - URL to retrieve the next page:
- String containing full URL to next page if more results exist
- `null` if on the last page of results

### Example responses

**School directory request:**
```
URL: https://educationdata.urban.org/api/v1/schools/ccd/directory/2020/
```

Response structure:
```json
{
  "results": [
    {
      "year": 2020,
      "ncessch": "010000100277",
      "school_name": "Example Elementary School",
      "fips": 1,
      "school_level": 1,
      "charter": 0,
      "latitude": 32.3456,
      "longitude": -86.2345
      // ... additional fields
    }
    // ... up to 10,000 records
  ],
  "next": "https://educationdata.urban.org/api/v1/schools/ccd/directory/2020/?page=2"
}
```

**Summary endpoint response:**
```
URL: https://educationdata.urban.org/api/v1/schools/ccd/enrollment/summaries?var=enrollment&stat=sum&by=fips&year=2020
```

Response structure:
```json
{
  "results": [
    {
      "fips": 1,
      "year": 2020,
      "enrollment": 754123
    },
    {
      "fips": 2,
      "year": 2020,
      "enrollment": 132104
    }
    // ... one record per state
  ]
}
```

### Data record structure

Each record in the `results` array contains:

**Identifier fields:**
- `year` - Academic year
- `ncessch` - School ID (12-digit)
- `leaid` - District ID (7-digit)
- `unitid` - College/university ID
- `fips` - State FIPS code

**Data fields specific to the endpoint:**
- Numeric values (enrollment counts, revenue amounts, test scores, etc.)
- Categorical values (school types, grade levels, race codes, etc.)
- Text fields (names, addresses)
- Geographic coordinates (latitude, longitude)

**Special values:**
- `-1` typically indicates missing data
- `-2` typically indicates not applicable
- `-3` may indicate suppressed for privacy
- Check endpoint-specific documentation for special value meanings

### Metadata endpoint responses

Metadata endpoints return information about the API structure:

**`/api/v1/api-endpoints/`** - Lists all available endpoints:
- Endpoint IDs
- Endpoint URLs
- Years available
- Descriptions

**`/api/v1/api-variables/`** - Lists all variables:
- Variable names
- Data types
- Formats
- Labels and descriptions
- Special value codes

**`/api/v1/api-endpoint-varlist/`** - Variables by endpoint:
- Which variables are available for each endpoint
- Required vs. optional variables

**`/api/v1/api-downloads/`** - CSV downloads and codebooks:
- Direct download URLs
- Codebook links (Excel format)
- File sizes and descriptions

### Pagination

**Pagination is automatic and transparent:**

When results exceed 10,000 records:
1. First request returns up to 10,000 records plus a `next` URL
2. Continue requesting the `next` URL to retrieve subsequent pages
3. `next` becomes `null` when no more pages remain

**Implementing pagination:**

Python example:
```python
import requests
import pandas as pd

url = "https://educationdata.urban.org/api/v1/schools/ccd/directory/2020/"
response = requests.get(url).json()
data = response["results"]

# Loop through remaining pages
while response["next"]:
    response = requests.get(response["next"]).json()
    data.extend(response["results"])

df = pd.DataFrame(data)
```

JavaScript example:
```javascript
let url = "https://educationdata.urban.org/api/v1/schools/ccd/directory/2020/"
let data = []

const getData = async (url) => {
  const response = await fetch(url);
  const json = await response.json();
  data = data.concat(json.results);
  
  if (json.next) {
    await getData(json.next);
  }
}

getData(url)
```

**Note:** The official R and Stata packages automatically handle pagination, so users of those tools don't need to implement manual pagination logic.

### Error handling

While specific error response formats aren't fully documented, follow these best practices:

**Check for expected response structure:**
```python
response = requests.get(url)
if response.status_code == 200:
    data = response.json()
    if "results" in data:
        # Process results
    else:
        # Handle unexpected response structure
else:
    # Handle HTTP error
```

**Handle missing data:**
- Empty `results` arrays indicate no matching records
- Check for special values (-1, -2, -3) in numeric fields
- Validate that required fields are present

**Common issues:**
- Invalid endpoint URLs (incorrect path components)
- Missing required specifiers (e.g., grade for enrollment endpoints)
- Invalid filter values
- Database query timeouts for very large, unoptimized requests

## Best practices for using the API

### Performance optimization strategies

**1. Use main filters effectively**

Apply filters at the API level rather than downloading all data and filtering locally:

Efficient:
```
/api/v1/schools/ccd/directory/2020?fips=17&school_level=3
```

Inefficient:
```
/api/v1/schools/ccd/directory/2020/
(then filtering locally for Illinois high schools)
```

**Main filters** (year, fips, ncessch, leaid, unitid, grade) are indexed and provide the fastest queries.

**2. Leverage summary endpoints**

For aggregated statistics, summary endpoints are orders of magnitude faster than pulling raw records:

Fast summary query:
```
/api/v1/schools/ccd/enrollment/summaries?var=enrollment&stat=sum&by=fips,race
```

Versus downloading millions of school-level records and aggregating locally.

**3. Use CSV downloads for large datasets**

For complete datasets spanning multiple years:
- CSV downloads are significantly faster than paginating through API results
- Access via: `https://educationdata.urban.org/csv/{file_dir}/{file_name}`
- Available in documentation under "Downloads" tab
- Single CSV may cover multiple years
- May require post-download filtering

**Trade-off:** CSV is faster for full datasets but slower for small, filtered subsets. Use the API for targeted queries, CSV for comprehensive downloads.

**4. Specify multiple values efficiently**

Use comma-separated values in a single filter:
```
?fips=17,55&year=2018,2019,2020
```

Rather than making separate requests for each value.

**5. Take advantage of caching**

The API implements aggressive caching:
- Identical requests return much faster (served from cache)
- 90%+ of requests served from cache
- Query parameter order doesn't affect caching (URLs are normalized)

**6. Request only necessary data**

- Use appropriate endpoint granularity (don't request school-level data if district-level suffices)
- Apply filters to reduce result size
- Use summary endpoints when aggregated statistics meet your needs

### Data retrieval guidelines

**1. Check data availability first**

Use metadata endpoints to verify data availability:
```python
metadata_url = "https://educationdata.urban.org/api/v1/api-endpoints/"
payload = {"endpoint_id": 24}
response = requests.get(metadata_url, params=payload).json()
latest_year = response["results"][0]["years_available"][-4:]
```

**2. Implement proper pagination**

Always handle pagination for large result sets:
- Check for `next` field in responses
- Continue requesting until `next` is `null`
- Or use R/Stata packages that handle pagination automatically

**3. Validate data quality**

- Check for special values indicating missing data (-1, -2, -3)
- Validate that required fields are present
- Be aware of privacy suppressions in CRDC and EdFacts data
- Consider COVID-19 data quality issues for 2019-20 and 2020-21

**4. Handle temporal changes**

- School and district boundaries change over time; IDs may not be stable across all years
- CRDC is biennial (collected every other year)
- Check years available for each endpoint
- Be aware of gaps in data collection

### Programming language implementations

**R Package (recommended for R users):**
```r
install.packages("educationdata")
library(educationdata)

# Get data with automatic pagination
df <- get_education_data(
  level = "schools",
  source = "ccd",
  topic = "directory",
  filters = list(year = 2020, fips = 17),
  add_labels = TRUE
)
```

**Stata Package (recommended for Stata users):**
```stata
ssc install educationdata
ssc install libjson

educationdata using "schools ccd directory", ///
  sub(year=2020 fips=17) clear
```

**Python (using requests library):**
```python
import requests
import pandas as pd

url = "https://educationdata.urban.org/api/v1/schools/ccd/directory/2020/"
params = {"fips": 17, "school_level": 3}
response = requests.get(url, params=params).json()

data = response["results"]
while response["next"]:
    response = requests.get(response["next"]).json()
    data.extend(response["results"])

df = pd.DataFrame(data)
```

**JavaScript (using fetch):**
```javascript
const url = "https://educationdata.urban.org/api/v1/schools/ccd/directory/2020/?fips=17";

fetch(url)
  .then(response => response.json())
  .then(data => {
    console.log(data.results);
    // Handle pagination if needed
    if (data.next) {
      // fetch data.next
    }
  });
```

### Common pitfalls to avoid

**1. Not handling pagination**
- Assuming all data arrives in the first response
- Solution: Always check for and follow `next` URLs

**2. Ignoring the 10,000 record limit**
- Expecting unlimited results per page
- Solution: Implement proper pagination loops

**3. Using API for massive bulk downloads**
- Pulling gigabytes of data via paginated API calls
- Solution: Use CSV downloads for large comprehensive datasets (8+ GB)

**4. Inefficient filtering**
- Downloading all data and filtering locally
- Solution: Use API query parameters to filter at source

**5. Missing required specifiers**
- Some endpoints require grade, level of study, or other path parameters
- Solution: Check documentation "Example Request" tab for required components

**6. Not utilizing summary endpoints**
- Computing aggregations on millions of raw records locally
- Solution: Use `/summaries` endpoints with appropriate statistics

**7. Assuming stable identifiers across time**
- School and district IDs can change as boundaries shift
- Solution: Use multiple identifiers (name, location) to track entities over time

**8. Ignoring data quality caveats**
- EdFacts data uses "fuzzing" for privacy, introducing measurement error
- CRDC small cell sizes may be suppressed
- COVID-19 impacts on 2019-20 and 2020-21 data
- Solution: Read data quality notes in source documentation

**9. Not checking endpoint-specific filters**
- Assuming all variables can be filtered
- Solution: Check documentation for each endpoint's available filters

**10. Bypassing cache unnecessarily**
- Making identical requests with different parameter orders
- Note: API now normalizes URLs, but use consistent formatting

### Tips for specific use cases

**Building dashboards and visualizations:**
- Use summary endpoints for real-time aggregations
- Cache results on your end to reduce API calls
- Monitor response times and optimize queries
- Consider pre-loading data via CSV for static visualizations

**Research and analysis:**
- Download complete datasets via CSV for comprehensive analysis
- Use API for exploratory queries and data validation
- Leverage R or Stata packages for simplified workflows
- Document exact API queries/versions for reproducibility

**Data pipelines and automation:**
- Use metadata endpoints to programmatically discover available years
- Implement error handling and retry logic
- Schedule large downloads during off-peak hours
- Store downloaded data locally to minimize repeated API calls

**Quick lookups and exploration:**
- Use API directly in web browser for small queries
- Test query syntax in browser before implementing in code
- Use summary endpoints for quick statistics
- Leverage filters to narrow results efficiently

### Working with variable documentation

**Access codebooks and data dictionaries:**

1. **API Variables endpoint:**
```
https://educationdata.urban.org/api/v1/api-variables/
```
Returns all variables with data types, formats, labels, special values

2. **API Endpoint Variables endpoint:**
```
https://educationdata.urban.org/api/v1/api-endpoint-varlist/
```
Returns variables organized by endpoint

3. **Downloadable codebooks:**
- Excel format (XLS) codebooks available for major endpoints
- Access via "Downloads" tab in documentation
- Include variable names, types, labels, value codes

**Understanding special values:**
- `-1` typically indicates missing data
- `-2` typically indicates not applicable
- `-3` may indicate suppressed for privacy
- `-9` sometimes used for "not reported"
- Check endpoint-specific codebooks for exact meanings

**Using labels in R package:**
```r
df <- get_education_data(
  level = "schools",
  source = "ccd",
  topic = "directory",
  add_labels = TRUE  # Adds human-readable labels
)
```

## Data sources and updates

### Federal data sources integrated

The Education Data Portal aggregates and harmonizes data from:

**US Department of Education:**
- Common Core of Data (CCD) - Public K-12 schools and districts
- Civil Rights Data Collection (CRDC) - Equity and civil rights data
- EdFacts - State assessment and performance data
- Integrated Postsecondary Education Data System (IPEDS) - College data
- College Scorecard - Student outcomes and loan repayment

**US Census Bureau:**
- Small Area Income and Poverty Estimates (SAIPE) - District poverty data
- National Historical Geographic Information System (NHGIS) - Census data at education institution locations

**Other sources:**
- Federal Student Aid (FSA) - Student loan and grant data
- National Association of College and University Business Officers (NACUBO) - Endowment data
- National Center for Charitable Statistics (NCCS) - IRS Form 990 data
- Campus Crime (Clery Act) - Campus crime statistics
- Equity in Athletics Data (EADA) - Athletic participation

### Data quality considerations

**Known limitations:**

1. **Privacy protections:** Small cell sizes may be suppressed in CRDC and EdFacts data

2. **EdFacts fuzzing:** EdFacts data uses statistical "fuzzing" to protect student privacy, which introduces measurement error in reported values

3. **COVID-19 impacts:**
   - 2019-20 assessment data largely not collected
   - 2020-21 data has participation and quality issues
   - 2020 CRDC data may have collection anomalies

4. **CRDC collection gaps:** Biennial collection means data not available for all years (collected only in odd years: 2011, 2013, 2015, 2017, 2020)

5. **College Scorecard limitations:** Only includes students who received federal financial aid (Title IV); not all students

6. **Identifier stability:** School district boundaries change over time; district IDs may not be perfectly stable across all years

7. **IPEDS branch campuses:** Sometimes aggregated to main campus at OPEID level rather than individual campus (UNITID)

8. **Finance fiscal years:** Finance data uses fiscal year which may differ from academic year

### Data update frequency

The portal is updated as source agencies release new data:
- CCD: Annual updates (typically released in spring for prior year)
- CRDC: Biennial updates (typically 12-18 months after collection year)
- IPEDS: Annual updates by component (fall, spring, winter collections)
- EdFacts: Annual updates (typically fall release for prior year)
- SAIPE: Annual updates (typically released in fall)
- College Scorecard: Annual updates (typically fall release)

Check the metadata endpoints or documentation for current data availability.

## Support and resources

**General questions and support:**
- Email: educationdata@urban.org

**Official documentation:**
- Main documentation: https://educationdata.urban.org/documentation/
- FAQ guide: https://urbaninstitute.github.io/education-data-faqs/

**GitHub repositories:**
- R package: https://github.com/UrbanInstitute/education-data-package-r
- Stata package: https://github.com/UrbanInstitute/education-data-package-stata
- Summary endpoints: https://github.com/UrbanInstitute/education-data-summary-endpoints
- FAQ guide: https://github.com/UrbanInstitute/education-data-faqs

**Issue reporting:**
- R package issues: https://github.com/UrbanInstitute/education-data-package-r/issues
- Stata package issues: https://github.com/UrbanInstitute/education-data-package-stata/issues
- Summary endpoints issues: https://github.com/UrbanInstitute/education-data-summary-endpoints/issues
- FAQ issues: https://github.com/UrbanInstitute/education-data-faqs/issues

## Summary

The Urban Institute Education Data Portal API provides comprehensive, harmonized access to decades of US education data spanning kindergarten through postsecondary education. With **no authentication required**, **consistent REST architecture**, and **160+ endpoints** covering enrollment, demographics, finance, and performance metrics, the API democratizes access to federal education data. Key features include **10,000 records per page** with automatic pagination, **summary endpoints** for rapid aggregations, and official **R and Stata packages** that simplify usage. The API serves data from all 50 states and DC across 38+ years of K-12 data and 45+ years of college data, making it an invaluable resource for researchers, policymakers, journalists, and developers working with education data.