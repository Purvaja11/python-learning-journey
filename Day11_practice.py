"""
DAY 11 - DAILY PRACTICE & SELF-ASSESSMENT
Data Cleaning Mastery - Complete all exercises!
"""

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

print("="*80)
print("DAY 11 - DATA CLEANING DAILY PRACTICE")
print("="*80)
print("\n")

# ============================================================================
# EXERCISE 1: MISSING VALUES MASTERY 
# ============================================================================

print("="*80)
print("EXERCISE 1: MISSING VALUES MASTERY ")
print("="*80)

# Dataset with various missing value scenarios
exercise1_data = pd.DataFrame({
    'Employee_ID': ['E001', 'E002', 'E003', 'E004', 'E005', 'E006', 'E007', 'E008'],
    'Name': ['Alice', 'Bob', None, 'Diana', 'Eve', 'Frank', 'Grace', 'Henry'],
    'Age': [28, 35, 42, np.nan, 31, 29, np.nan, 38],
    'Salary': [55000, 62000, 58000, 64000, np.nan, 59000, 61000, np.nan],
    'Department': ['Sales', 'IT', 'Marketing', 'Sales', None, 'IT', 'HR', 'Marketing'],
    'Years_Experience': [3, 8, 12, 7, 5, np.nan, 4, 10]
})

print("\n📊 Original Data:")
print(exercise1_data)
print(f"\n📈 Missing Values Count:")
print(exercise1_data.isnull().sum())

print("\n✏️ YOUR TASKS:")
print("1. Fill missing 'Name' with 'Unknown'")
print("2. Fill missing 'Age' with median age")
print("3. Fill missing 'Salary' with median salary")
print("4. Fill missing 'Department' with mode (most common)")
print("5. Fill missing 'Years_Experience' with mean (rounded to 1 decimal)")

print("\n" + "-"*80)
print("SOLUTION TEMPLATE:")
print("-"*80)

# YOUR CODE HERE - START
df_ex1 = exercise1_data.copy()

# Task 1: Fill missing Name
df_ex1['Name'] = df_ex1['Name'].fillna('Unknown')

# Task 2: Fill missing Age with median
df_ex1['Age'] = df_ex1['Age'].fillna(df_ex1['Age'].median())

# Task 3: Fill missing Salary with median
df_ex1['Salary'] = df_ex1['Salary'].fillna(df_ex1['Salary'].median())

# Task 4: Fill missing Department with mode
df_ex1['Department'] = df_ex1['Department'].fillna(df_ex1['Department'].mode()[0])

# Task 5: Fill missing Years_Experience with mean
df_ex1['Years_Experience'] = df_ex1['Years_Experience'].fillna(df_ex1['Years_Experience'].mean())

# YOUR CODE HERE - END

print("\n✅ Your Result:")
print(df_ex1)
print(f"\n✅ Missing Values After Cleaning:")
print(df_ex1.isnull().sum())

# Verification
expected_missing = df_ex1.isnull().sum().sum()
if expected_missing == 0:
    print("\n🎉 PERFECT! All missing values handled!")
else:
    print(f"\n⚠️ Still have {expected_missing} missing values. Review your code!")

# ============================================================================
# EXERCISE 2: DUPLICATES & OUTLIERS 
# ============================================================================

print("\n" + "="*80)
print("EXERCISE 2: DUPLICATES & OUTLIERS ")
print("="*80)

exercise2_data = pd.DataFrame({
    'Order_ID': ['O001', 'O002', 'O003', 'O002', 'O004', 'O005', 'O006', 'O007', 'O008'],
    'Product': ['Laptop', 'Phone', 'Tablet', 'Phone', 'Mouse', 'Keyboard', 'Monitor', 'Laptop', 'Headphones'],
    'Quantity': [2, 1, 3, 1, 15, 2, 1, 999, 4],  # 999 is outlier
    'Price': [50000, 25000, 15000, 25000, 500, 1200, 12000, 50000, 2000],
    'Customer_Age': [28, 35, 42, 35, -5, 29, 150, 32, 45]  # -5 and 150 are invalid
})

print("\n📊 Original Data:")
print(exercise2_data)
print(f"\nDuplicates: {exercise2_data.duplicated().sum()}")

print("\n✏️ YOUR TASKS:")
print("1. Remove duplicate rows (keep first occurrence) ")
print("2. Remove rows where Customer_Age < 0 or > 120 ")
print("3. Cap Quantity outliers at 50 (use clip method) ")
print("4. Calculate IQR bounds for Price and flag outliers ")

print("\n" + "-"*80)
print("SOLUTION TEMPLATE:")
print("-"*80)

# YOUR CODE HERE - START
df_ex2 = exercise2_data.copy()

# Task 1: Remove duplicates
df_ex2 = df_ex2.drop_duplicates()

# Task 2: Remove invalid ages
df_ex2 = df_ex2[df_ex2['Customer_Age'] > 0]
df_ex2 = df_ex2[df_ex2['Customer_Age'] < 120]

# Task 3: Cap Quantity at 50
df_ex2['Quantity'] = df_ex2['Quantity'].clip(upper=50)

# Task 4: Calculate IQR for Price and add 'Price_Outlier' column (True/False)
Q1 = df_ex2['Price'].quantile(0.25)
Q3 = df_ex2['Price'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
df_ex2['Price_Outlier'] = ((df_ex2['Price'] < lower_bound) | (df_ex2['Price'] > upper_bound))
df_ex2['Price_Outlier'] = ((df_ex2['Price'] >= lower_bound) & (df_ex2['Price'] <= upper_bound))

# YOUR CODE HERE - END

print("\n✅ Your Result:")
print(df_ex2)

# Verification
if df_ex2.duplicated().sum() == 0:
    print("\n✅ No duplicates!")
else:
    print("\n⚠️ Still have duplicates!")

if ((df_ex2['Customer_Age'] >= 0) & (df_ex2['Customer_Age'] <= 120)).all():
    print("✅ All ages valid!")
else:
    print("⚠️ Invalid ages still present!")

if (df_ex2['Quantity'] <= 50).all():
    print("✅ Quantities capped!")
else:
    print("⚠️ Quantities not properly capped!")

# ============================================================================
# EXERCISE 3: TEXT CLEANING & STANDARDIZATION (20 points)
# ============================================================================

print("\n" + "="*80)
print("EXERCISE 3: TEXT CLEANING & STANDARDIZATION")
print("="*80)

exercise3_data = pd.DataFrame({
    'Customer_ID': ['C001', 'C002', 'C003', 'C004', 'C005', 'C006'],
    'Name': ['  john DOE  ', 'jane@smith', 'Bob#Johnson', '  ALICE brown', 'charlie$davis', 'EVE white  '],
    'Email': ['JOHN@GMAIL.COM', 'jane@GMAIL.com', 'bob@Yahoo.COM', 'alice@gmail.COM', 'charlie@YAHOO.com', 'eve@gmail.COM'],
    'City': ['  mumbai  ', 'DELHI', 'bangalore', 'Mumbai', 'delhi', '  Bangalore  '],
    'Phone': ['9876543210', '98765-43210', '(987) 654-3210', '987 654 3210', '9876543210', '98-765-43210']
})

print("\n📊 Original Data:")
print(exercise3_data)

print("\n✏️ YOUR TASKS:")
print("1. Clean 'Name': strip whitespace, remove special chars, title case ")
print("2. Standardize 'Email': all lowercase ")
print("3. Standardize 'City': strip whitespace, title case ")
print("4. Clean 'Phone': remove all non-digits ")
print("5. Verify all phone numbers are exactly 10 digits ")

print("\n" + "-"*80)
print("SOLUTION TEMPLATE:")
print("-"*80)

# YOUR CODE HERE - START
df_ex3 = exercise3_data.copy()

# Task 1: Clean Name
df_ex3['Name'] = df_ex3['Name'].str.strip()
df_ex3['Name'] = df_ex3['Name'].str.replace(r'[^a-zA-Z\s]', '', regex=True)
df_ex3['Name'] = df_ex3['Name'].str.title()

# Task 2: Lowercase Email
df_ex3['Email'] = df_ex3['Email'].str.lower()

# Task 3: Standardize City
df_ex3['City'] = df_ex3['City'].str.strip()
df_ex3['City'] = df_ex3['City'].str.title()

# Task 4: Clean Phone (remove non-digits)
df_ex3['Phone'] = df_ex3['Phone'].str.strip()
df_ex3['Phone'] = df_ex3['Phone'].str.replace(r'[^0-9]', '', regex=True)

# Task 5: Add 'Valid_Phone' column (True if 10 digits)
df_ex3['Valid_Phone'] = (df_ex3['Phone'].astype(str).str.len() == 10)

# YOUR CODE HERE - END

print("\n✅ Your Result:")
print(df_ex3)

# Verification
has_special = df_ex3['Name'].str.contains(r'[^a-zA-Z\s]').any()
if not has_special:
    print("\n✅ Names cleaned! ")
else:
    print("\n⚠️ Names still have special characters!")

if df_ex3['Email'].str.islower().all():
    print("✅ Emails standardized! ")
else:
    print("⚠️ Emails not all lowercase!")

# ============================================================================
# EXERCISE 4: DATA TYPES & VALIDATION 
# ============================================================================

print("\n" + "="*80)
print("EXERCISE 4: DATA TYPES & VALIDATION ")
print("="*80)

exercise4_data = pd.DataFrame({
    'Transaction_ID': ['T001', 'T002', 'T003', 'T004', 'T005'],
    'Date': ['2024-01-15', '2024-02-20', 'invalid_date', '2024-03-10', '2025-12-31'],
    'Amount': ['1000', '1500.50', '2000', 'invalid', '3000'],
    'Quantity': ['5', '10', '15', '20', '25'],
    'Is_Delivered': ['Yes', 'No', 'Yes', '1', '0']
})

print("\n📊 Original Data:")
print(exercise4_data)
print(f"\n📈 Data Types:")
print(exercise4_data.dtypes)

print("\n✏️ YOUR TASKS:")
print("1. Convert 'Date' to datetime (coerce errors to NaT)")
print("2. Convert 'Amount' to float (coerce errors to NaN) ")
print("3. Convert 'Quantity' to int ")
print("4. Create validation report function ")

print("\n" + "-"*80)
print("SOLUTION TEMPLATE:")
print("-"*80)

# YOUR CODE HERE - START
df_ex4 = exercise4_data.copy()

# Task 1: Convert Date to datetime
df_ex4['Date'] = pd.to_datetime(df_ex4['Date'], errors='coerce')

# Task 2: Convert Amount to float
df_ex4['Amount'] = pd.to_numeric(df_ex4['Amount'], errors='coerce')

# Task 3: Convert Quantity to int
df_ex4['Quantity'] = df_ex4['Quantity'].astype(int)

# Task 4: Create validation function
def validate_dataframe(df):
    """
    Validation function that checks:
    - Missing values count
    - Invalid dates (NaT)
    - Invalid amounts (NaN)
    - Returns True if data is valid, False otherwise
    """
    # YOUR CODE HERE
    issues = []

    # Check missing values 
    missing = df.isnull().sum()
    if missing.sum() > 0:
        issues.append(f"Missing values: {missing[missing > 0].to_dict()}")
    
    # Check invalid dates
    invalid_dates = df['Date'].isna().sum()
    if invalid_dates > 0:
        issues.append(f"Invalid Dates: {invalid_dates}")

    # Check invalid amounts
    invalid_amounts = df['Amount'].isnull().sum()
    if invalid_amounts > 0:
        issues.append(f"Invalid Amounts: {invalid_amounts}")

    if issues:
        print(" DATA QUALITY ISSUES FOUND:")
        for issue in issues:
            print(f"  -{issue}")
    else:
        print(" Data validation passed!")
    return len(issues) == 0

# YOUR CODE HERE - END

print("\n✅ Your Result:")
print(df_ex4)
print(f"\n✅ Data Types After Conversion:")
print(df_ex4.dtypes)

# Verification
if df_ex4['Date'].dtype == 'datetime64[ns]':
    print("\n✅ Date converted! ")
else:
    print("\n⚠️ Date not converted to datetime!")

if df_ex4['Amount'].dtype == 'float64':
    print("✅ Amount converted! ")
else:
    print("⚠️ Amount not converted to float!")

if df_ex4['Quantity'].dtype in ['int64', 'int32']:
    print("✅ Quantity converted! ")
else:
    print("⚠️ Quantity not converted to int!")

# ============================================================================
# EXERCISE 5: REAL-WORLD CHALLENGE - COMPLETE PIPELINE 
# ============================================================================

print("\n" + "="*80)
print("EXERCISE 5: REAL-WORLD CHALLENGE - COMPLETE PIPELINE ")
print("="*80)

# Realistic messy dataset combining ALL issues
challenge_data = pd.DataFrame({
    'ID': ['P001', 'P002', 'P003', 'P001', 'P004', None, 'P005', 'P006'],
    'Name': ['  ALICE  ', 'bob@smith', 'Charlie', 'Alice', 'diana#', 'Eve', 'frank', '  Grace'],
    'Age': [25, 999, 30, 25, -5, 28, np.nan, 35],
    'Salary': ['50000', '60000', 'invalid', '50000', '55000', np.nan, '62000', '58000'],
    'City': ['mumbai', 'DELHI', 'bangalore', 'Mumbai', 'delhi', 'Bangalore', 'chennai', 'Mumbai'],
    'Join_Date': ['2021-01-15', '2020-03-20', 'invalid', '2021-01-15', '2022-06-10', '2019-08-05', '2023-02-01', '2050-12-31'],
    'Department': ['Sales', 'sales', 'MARKETING', 'Sales', None, 'IT', 'Marketing', 'HR']
})

print("\n📊 MESSY DATA - Fix EVERYTHING:")
print(challenge_data)

print("\n✏️ YOUR CHALLENGE:")
print("Apply ALL cleaning techniques you've learned!")
print("1. Remove duplicates ")
print("2. Handle missing ID (drop rows) ")
print("3. Clean Name (strip, remove special chars, title case) ")
print("4. Fix Age (remove invalid, fill missing with median)")
print("5. Convert Salary to numeric ")
print("6. Standardize City ")
print("7. Fix Join_Date (datetime, remove future dates) ")
print("8. Standardize Department ")

print("\n" + "-"*80)
print("YOUR COMPLETE SOLUTION:")
print("-"*80)

# YOUR CODE HERE - START
df_challenge = challenge_data.copy()

# Step 1: Remove duplicates
df_challenge = df_challenge.drop_duplicates()

# Step 2: Handle missing ID
df_challenge['ID'] = df_challenge.dropna(subset=['ID'])

# Step 3: Clean Name
df_challenge['Name'] = df_challenge['Name'].str.strip()
df_challenge['Name'] = df_challenge['Name'].str.replace(r'[^a-zA-Z\s]', '', regex=True)
df_challenge['Name'] = df_challenge['Name'].str.title()

# Step 4: Fix Age
df_challenge = df_challenge[(df_challenge['Age'] > 0) & (df_challenge['Age'] < 120)]
df_challenge['Age'] = df_challenge['Age'].fillna(df_challenge['Age'].median())

# Step 5: Convert Salary
df_challenge['Salary'] = pd.to_numeric(df_challenge['Salary'], errors='coerce')

# Step 6: Standardize City
df_challenge['City'] = df_challenge['City'].str.strip()
df_challenge['City'] = df_challenge['City'].str.title()

# Step 7: Fix Join_Date
df_challenge['Join_Date'] = pd.to_datetime(df_challenge['Join_Date'], errors='coerce')

# Remove Future dates
today = pd.Timestamp.now()
future_dates = (df_challenge['Join_Date'] > today).sum()
if future_dates > 0:
    df_challenge = df_challenge[df_challenge['Join_Date'] <= today]

# Step 8: Standardize Department
df_challenge['Department'] = df_challenge['Department'].str.strip()
df_challenge['Department'] = df_challenge['Department'].str.title()
df_challenge['Department'] = df_challenge['Department'].fillna(df_challenge['Department'].mode()[0])

# YOUR CODE HERE - END

print("\n✅ YOUR FINAL CLEANED DATA:")
print(df_challenge)

# Final Validation
print("\n" + "="*80)
print("FINAL VALIDATION")
print("="*80)



if df_challenge.duplicated().sum() == 0:
    print("✅ No duplicates!")

if df_challenge['ID'].isnull().sum() == 0:
    print("✅ No missing IDs!")

if not df_challenge['Name'].str.contains(r'[^a-zA-Z\s]').any():
    print("✅ Names cleaned!")

if ((df_challenge['Age'] > 0) & (df_challenge['Age'] < 120)).all():
    print("✅ Valid ages!")

if df_challenge['Salary'].dtype in ['float64', 'int64']:
    print("✅ Salary numeric!")

print(f"\n All Validation Complete!")

