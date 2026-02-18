"""
DAY 18 PRACTICE: Data Cleaning
Real-world messy data challenges!

Complete these BEFORE checking solutions.
"""

import pandas as pd
import numpy as np
import re

print("="*80)
print("🎯 DAY 18: DATA CLEANING PRACTICE")
print("="*80)

# Shared messy dataset for all exercises
data = {
    'name': ['Alice Johnson', 'bob smith', '  CHARLIE  ', None, 'Eve Wilson',
             'frank castle', 'Grace Hopper', 'henry ford', 'Isabella M', 'Jack'],
    'email': ['alice@email.com', 'bob@email', 'charlie@email.com', None,
              'eve@email.com', 'not_an_email', 'grace@email.com', 'henry@email.com',
              'isabella@email.com', 'jack@email.com'],
    'age': [28, 35, -5, 29, 150, 45, 38, 27, None, 29],
    'salary': [50000, 75000, 120000, 65000, 45000, 9999999, 85000, 55000, None, 60000],
    'city': ['Mumbai', 'mumbai', 'DELHI', 'Delhi', 'pune', 'Pune',
             'bangalore', 'BANGALORE', 'Chennai', 'chennai'],
    'join_date': ['2022-01-15', '2021/06/20', '20-03-2022', '2023-08-10',
                  '2022-11-05', '2021-03-22', '15/07/2022', '2023-02-28',
                  '2022-09-14', None],
    'score': [85, 92, 78, None, 88, 95, 72, 68, 91, 84]
}

df = pd.DataFrame(data)

# =============================================================================
# EXERCISE 1: Data Quality Report
# =============================================================================
print("\n" + "="*80)
print("EXERCISE 1: Write a Data Quality Function")
print("="*80)
print("""TASK: Write a function that returns a quality report showing

- Total rows and columns
- Missing value count and % for each column
- Number of duplicate rows
- Data types of each column

Expected output format:
   column_name: X missing (Y%)

Hint: Use df.isnull().sum(), df.duplicated().sum(), df.dtypes""")


# TODO: Write your function
def data_quality_report(df):
    print(f"\n📐 Shape: {df.shape[0]} rows x {df.shape[1]} columns")
    print("\n🔴 MISSING VALUES:")
    missing = df.isnull().sum()
    missing_pct = (missing / len(df) * 100).round(2)
    for col in df.columns:
        if missing[col] > 0:
            print(f"	{col:15s}: {missing[col]} missing ({missing_pct[col]}%)")
            
    print(f"\n🔴 DUPLICATES: {df.duplicated().sum()} duplicate rows")

    print(f"\n🔵 DATA TYPES:")
    for col, dtype in df.dtypes.items():
        print(f"	{col:15s}: {dtype}")



# Uncomment to test:
data_quality_report(df)


# =============================================================================
# EXERCISE 2: Handle Missing Values (Smart Strategy)
# =============================================================================
print("\n" + "="*80)
print("EXERCISE 2: Smart Missing Value Handling")
print("="*80)
print("""TASK: Fill missing values using the RIGHT strategy for each column

- 'name': fill with 'Unknown'
- 'age': fill with MEDIAN (not mean - why?)
- 'salary': fill with MEDIAN grouped by city
- 'score': fill with MEAN
- 'email': keep as NaN (we'll handle separately)

After filling, print: "Missing values remaining: X"

Hint: Use .fillna(), .groupby().transform()
""")

df_ex2 = df.copy()

# TODO: Fill missing values

# Name: fill with 'Unknown'
df_ex2['name'] = df_ex2['name'].fillna('Unknown')

# Age: fill with MEDIAN (not mean - median is robust to outliers like 150 and -5)
df_ex2['age'] = df_ex2['age'].fillna(df_ex2['age'].median())

# Salary: fill with MEDIAN grouped by city (smarter than global median)
df_ex2['salary'] = df_ex2.groupby('city')['salary'].transform(
    lambda x: x.fillna(x.median()))

# Fallback to global median if city group has no other values
df_ex2['salary'] = df_ex2['salary'].fillna(df_ex2['salary'].median())

# Score: fill with MEAN (score is normaaly distributed, mean works fine)
df_ex2['score'] = df_ex2['score'].fillna(df_ex2['score'].mean())

# Email: keep as NaN - handle separately with validation
print(df_ex2[['name', 'age', 'salary', 'score']].to_string())
print(f"\n Missing values remaining: {df_ex2[['name', 'age', 'salary', 'score']].isnull().sum().sum()}")

# Uncomment to test:
print(f"Missing values remaining: {df_ex2.isnull().sum().sum()}")
print(df_ex2[['name', 'age', 'salary', 'score']].to_string())


# =============================================================================
# EXERCISE 3: Standardize Text Data
# =============================================================================
print("\n" + "="*80)
print("EXERCISE 3: String Standardization")
print("="*80)
print("""TASK: Clean the text columns:
1. 'name': strip whitespace + Title Case
2. 'city': strip whitespace + Title Case
3. After cleaning, show unique cities (should be 5 cities, not 10!)

Before: ['Mumbai', 'mumbai', 'DELHI', 'Delhi', 'pune', ...]
After:  ['Mumbai', 'Delhi', 'Pune', 'Bangalore', 'Chennai']

Hint: .str.strip(), .str.title()
""")

df_ex3 = df.copy()

# TODO: Standardize text
df_ex3['name'] = df_ex3['name'].str.strip().str.title()
df_ex3['city'] = df_ex3['city'].str.strip().str.title()

# Uncomment to test:
print(f"Unique cities before: {sorted(df['city'].unique())}")
print(f"Unique cities After: {sorted(df_ex3['city'].unique())}")
print(f"\nReduced from {df['city'].nunique()} to {df_ex3['city'].nunique()} unique cities ✅")



# =============================================================================
# EXERCISE 4: Regex Email Validation
# =============================================================================
print("\n" + "="*80)
print("EXERCISE 4: Email Validation with Regex")
print("="*80)
print("""
TASK: 
1. Write a regex pattern to validate emails
2. Mark invalid emails as 'Invalid'
3. Print how many emails are invalid

Valid email: must have @ and a domain with . 
Examples:
  'alice@email.com'  → VALID
  'bob@email'        → INVALID (no .com)
  'not_an_email'     → INVALID (no @)
  None               → INVALID

Hint: pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
      Use re.match() or str.contains()
""")

df_ex4 = df.copy()

# TODO: Validate emails
email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

def validate_email(email):
    if pd.isnull(email):
        return 'Invalid'
    elif re.match(email_pattern, str(email)):
        return email.lower()  # Optional: standardize to lowercase
    return 'Invalid'



df_ex4['email'] = df_ex4['email'].apply(validate_email)

# Uncomment to test:
invalid_count = (df_ex4['email'] == 'Invalid').sum()
print(f"Invalid emails found: {invalid_count}")
print(df_ex4[['name', 'email']].to_string())



# =============================================================================
# EXERCISE 5: Fix Invalid Values
# =============================================================================
print("\n" + "="*80)
print("EXERCISE 5: Fix Invalid Values")
print("="*80)
print("""
TASK: Fix logically invalid values:
1. 'age': 
   - Negative age → replace with median
   - Age > 100 → replace with median
2. 'salary': 
   - Values > 500000 → replace with median (outlier!)
3. Print count of fixes made for each column

Before: age has -5 and 150 (invalid!)
Before: salary has 9999999 (outlier!)

Hint: Use boolean masking: df[df['age'] < 0] = median
""")

df_ex5 = df.copy()

# TODO: Fix invalid values

#Age fixing
age_median = df_ex5['age'].median()
negative_ages = (df_ex5['age'] < 0).sum()
impossible_ages = (df_ex5['age'] > 100).sum()
df_ex5.loc[df_ex5['age'] < 0, 'age'] = age_median
df_ex5.loc[df_ex5['age'] > 100, 'age'] = age_median
print(f"Fixed {negative_ages} negative ages")
print(f"Fixed {impossible_ages} ages (> 100)")
print(f"Age range after: {df_ex5['age'].min()} - {df_ex5['age'].max()}")


# Salary fixing
salary_median = df_ex5['salary'].median()
salary_outliers = (df_ex5['salary'] > 500000).sum()
df_ex5.loc[df_ex5['salary'] > 500000, 'salary'] = salary_median
print(f"\nFixed {salary_outliers} salary outliers (> 500,000)")
print(f"Salary max after: {df_ex5['salary'].max():,.0f}")





# =============================================================================
# EXERCISE 6: Multi-Format Date Parsing
# =============================================================================
print("\n" + "="*80)
print("EXERCISE 6: Parse Multiple Date Formats")
print("="*80)
print("""
TASK: The join_date column has 3 different formats:
  '2022-01-15'  → YYYY-MM-DD
  '2021/06/20'  → YYYY/MM/DD  
  '20-03-2022'  → DD-MM-YYYY
  '15/07/2022'  → DD/MM/YYYY

Write a function that detects the format and parses correctly.
Convert all to standard datetime format.

After parsing:
- Print min and max join dates
- Print how many dates failed to parse

Hint: Try multiple formats with strptime, use try/except
""")

df_ex6 = df.copy()

# TODO: Parse dates
from datetime import datetime
def parse_date(date_str):
     if pd.isnull(date_str):
         return None
     
     formats = ['%Y-%m-%d', 
                '%Y/%m/%d',
                '%d-%m-%Y', 
                '%d/%m/%Y']

     for fmt in formats:
         try:
             return datetime.strptime(str(date_str), fmt).date()
         except ValueError:
             continue
         
     return None  # Failed to parse


df_ex6['join_date'] = pd.to_datetime(df_ex6['join_date'].apply(parse_date))

# Uncomment to test:
print(df_ex6[['name', 'join_date']].to_string())
print(f"\nDate range: {df_ex6['join_date'].min()} to {df_ex6['join_date'].max()}")
print(f"Failed to parse: {df_ex6['join_date'].isna().sum()}")



# =============================================================================
# EXERCISE 7: Outlier Detection with IQR
# =============================================================================
print("\n" + "="*80)
print("EXERCISE 7: Outlier Detection with IQR Method")
print("="*80)
print("""
TASK: Write a function that:
1. Calculates Q1, Q3, IQR for a column
2. Identifies outliers (below Q1-1.5*IQR or above Q3+1.5*IQR)
3. Reports which values are outliers
4. Replaces outliers with median

Apply this to the 'salary' and 'score' columns.

IQR Formula:
  Q1 = 25th percentile
  Q3 = 75th percentile
  IQR = Q3 - Q1
  Lower bound = Q1 - 1.5 * IQR
  Upper bound = Q3 + 1.5 * IQR

Hint: Use .quantile(0.25), .quantile(0.75), .clip()
""")

df_ex7 = df.copy()

# TODO: Implement IQR outlier detection
def detect_and_fix_outliers(series):
    """Detect outliers using IQR and clip them"""
    clean = series.dropna()  # Exclude NaN for quantile calculation

    Q1 = clean.quantile(0.25)
    Q3 = clean.quantile(0.75)
    IQR = Q3 - Q1

    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR

    outliers = clean[(clean < lower) | (clean > upper)]
    n_outliers = len(outliers)


    # Clip the original series
    fixed = series.clip(lower=lower, upper=upper)

    return fixed, n_outliers, lower, upper


# Apply to salary
df_ex7['salary'], n, lower, upper = detect_and_fix_outliers(df_ex7['salary'])
print(f"Salary outliers found: {n}")
print(f"Valid Salary range (IQR): {lower:,.0f} - {upper:,.0f}")
print(f"Salary range after fixing: {df_ex7['salary'].min():,.0f} - {df_ex7['salary'].max():,.0f}")

# Apply to score
df_ex7['score'], n, lower, upper = detect_and_fix_outliers(df_ex7['score'])
print(f"\nScore outliers found: {n}")
print(f"Score range after fixing: {df_ex7['score'].min():.1f} - {df_ex7['score'].max():.1f}")



# =============================================================================
# EXERCISE 8: Complete Pipeline (HARD!)
# =============================================================================
print("\n" + "="*80)
print("EXERCISE 8: Build Complete Cleaning Pipeline")
print("="*80)
print("""
TASK: Combine ALL previous exercises into one clean pipeline function

def clean_dataset(df):
    # Step 1: Remove duplicates
    # Step 2: Handle missing values
    # Step 3: Standardize strings
    # Step 4: Validate emails
    # Step 5: Fix invalid values
    # Step 6: Parse dates
    # Step 7: Fix outliers
    # Step 8: Add derived columns:
    #   - 'name_length': number of words in name
    #   - 'is_valid_email': True/False
    #   - 'age_group': 'Young' (<30), 'Middle' (30-45), 'Senior' (>45)
    
    return cleaned_df

# Test by running:
# clean_df = clean_dataset(df.copy())
# print(f"Shape: {df.shape} → {clean_df.shape}")
# print(clean_df.dtypes)
""")

# TODO: Build complete pipeline
def clean_dataset(df):
    """Complete cleaning pipeline combining all steps"""
    df = df.copy()

    # Step 1: Remove duplicates
    before = len(df)
    df = df.drop_duplicates()
    print(f"    Step 1 - Removed {before - len(df)} duplicate rows")

    # Step 2: Handle missing values 
    df['name'] = df['name'].fillna('Unknown')
    df['age'] = df['age'].fillna(df['age'].median())
    df['salary'] = df.groupby('city')['salary'].transform(
        lambda x: x.fillna(x.median()))
    df['salary'] = df['salary'].fillna(df['salary'].median())
    df['score'] = df['score'].fillna(df['score'].mean())

    print(f"    Step 2 - filled missing values")

    # Step 3: Standardize strings
    df['name'] = df['name'].str.strip().str.title()
    df['city'] = df['city'].str.strip().str.title()
    print(f"    Step 3 - standardized text ({df['city'].nunique()} unique cities)")

    # Step 4: Validate emails
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    def validate_email(email):
      if pd.isnull(email): return 'Invalid'
      return email.lower() if re.match(email_pattern, str(email)) else 'Invalid'
    df['email'] = df['email'].apply(validate_email)
    invalid = (df['email'] == 'Invalid').sum()
    print(f"    Step 4 - validated emails {invalid} invalid emails") 

    # Step 5: Fix invalid values
    age_median = df['age'].median()
    df.loc[df['age'] < 0, 'age'] = age_median
    df.loc[df['age'] > 100, 'age'] = age_median
    df['salary'] = df['salary'].clip(upper=500000)
    print(f"    Step 5 - fixed invalid ages and salary outliers")

    # Step 6: Parse dates
    def parse_date(d):
        if pd.isnull(d): return None
        for fmt in ['%Y-%m-%d', '%Y/%m/%d', '%d-%m-%Y', '%d/%m/%Y']:
            try: return datetime.strptime(str(d), fmt).date()
            except: continue
        return None
    df['join_date'] = pd.to_datetime(df['join_date'].apply(parse_date))
    print(f"    Step 6 - parsed all dates")

    # Step 7: Add derived columns
    df['name_length'] = df['name'].str.split().str.len()
    df['is_valid_email'] = df['email'] != 'Invalid'
    df['age_group'] = pd.cut(
        df['age'], 
        bins=[0, 30, 45, np.inf], 
        labels=['Young', 'Middle', 'Senior']
    )
    print(f"    Step 7 - added 3 derived columns")

    return df

# Uncomment to test:
print("\nRunning complete pipeline...")
clean_df = clean_dataset(df.copy())

print(f"\n📊 Shape: {df.shape} → {clean_df.shape}")
print(f"✅ Missing values remaining: {clean_df.isnull().sum().sum()}")
print(f"✅ Duplicates remaining: {clean_df.duplicated().sum()}")

print("\nFirst 5 rows of clean data:")
print(clean_df[['name', 'city', 'age', 'age_group', 'is_valid_email', 'score']].to_string())


# =============================================================================
# Completion
# =============================================================================

print("\n" + "="*80)
print("✅ COMPLETION CHECKLIST")
print("="*80)
print("""
□ Exercise 1: Data quality report function
□ Exercise 2: Smart missing value strategies
□ Exercise 3: String standardization
□ Exercise 4: Email validation with regex
□ Exercise 5: Fix invalid values
□ Exercise 6: Multi-format date parsing
□ Exercise 7: IQR outlier detection
□ Exercise 8: Complete cleaning pipeline (HARD!)


💡 KEY LESSONS:
- fillna(mean) vs fillna(median) → USE MEDIAN for skewed data!
- Group-based imputation is smarter than global imputation
- Always validate with regex, not just check for None
- IQR is robust, Z-score is not (affected by outliers)
- Build reusable pipelines, not one-off scripts
""")
print("\n" + "="*80)
print("Good luck! 💪 Real data is always messy!")
print("="*80)