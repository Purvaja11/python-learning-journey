"""
DAY 18: DATA CLEANING MASTERCLASS
Advanced techniques for handling real-world messy data

Topics:
- Missing value strategies (beyond just dropna/fillna)
- Duplicate detection and removal
- Data type fixing and standardization
- String cleaning with regex
- Outlier detection and treatment
- Automated cleaning pipeline
"""

import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

print("="*80)
print("🧹 DAY 18: DATA CLEANING MASTERCLASS")
print("="*80)


# =============================================================================
# STEP 1: CREATE REALISTIC MESSY DATASET
# =============================================================================

def create_messy_dataset():
    """Create a realistic messy dataset like you'd find in real work"""

    np.random.seed(42)

    data = {
        'customer_id': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                        11, 12, 13, 14, 15, 2, 5, 16, 17, 18],  # 2, 5 are duplicates

        'name': ['Alice Johnson', 'bob smith', 'CHARLIE BROWN', 'Diana Prince',
                 'Eve wilson', '  Frank Castle  ', 'Grace Hopper', 'henry ford',
                 'Isabella M.', 'Jack O\'Brien', 'Kate Bush', 'liam NEESON',
                 None, 'Nina Simone', 'Oscar Wilde', 'bob smith',  # None = missing
                 'Eve wilson', 'Paul McCartney', 'Quinn Hughes', 'Rachel Green'],

        'email': ['alice@email.com', 'bobsmith@email.com', 'charlie@email.com',
                  'diana@email.com', 'eve@email.com', 'frank@email.com',
                  'gracehopper@email.com', 'henry@email',  # invalid - no .com
                  'isabella@email.com', 'jack@email.com', 'kate@email.com',
                  'liam@email.com', 'missing_email',  # invalid
                  'nina@email.com', 'oscar@email.com', 'bobsmith@email.com',  # duplicate
                  'eve@email.com', 'paul@email.com', 'quinn@email.com', 'rachel@email.com'],

        'age': [28, 35, 42, 29, 31, 45, 38, 27, 33, 29,
                41, 36, None, 44, 52, 35, 31, 28,
                -5,   # invalid - negative age
                150], # invalid - impossible age

        'city': ['Mumbai', 'mumbai', 'DELHI', 'Delhi', 'Pune',
                 'pune', 'Bangalore', 'BANGALORE', 'Chennai', 'chennai',
                 'Hyderabad', 'hyderabad', 'Mumbai', 'Delhi', 'Pune',
                 'mumbai', 'Pune', 'Bangalore', 'Chennai', 'Hyderabad'],

        'salary': [50000, 75000, 120000, 65000, 45000,
                   90000, 85000, 55000, 70000, 60000,
                   95000, 80000, None,  # missing
                   72000, 110000, 75000, 45000,
                   9999999,  # outlier - way too high
                   58000, 63000],

        'join_date': ['2022-01-15', '2021/06/20', '20-03-2022',  # mixed formats!
                      '2023-08-10', '2022-11-05', '2021-03-22',
                      '15/07/2022', '2023-02-28', '2022-09-14', '2021-12-01',
                      '2023-05-17', '2022-07-30', '2021-08-15',
                      '2023-01-22', '2022-04-18', '2021/06/20',
                      '2022-11-05', '2023-03-12', '2022-06-25', '2021-10-08'],

        'phone': ['9876543210', '987-654-3211', '+91 9876543212',
                  '(98) 7654-3213', '9876543214', '98765 43215',
                  '9876543216', 'N/A', '9876543218', '9876543219',
                  '9876543220', '9876543221', None,
                  '9876543223', '9876543224', '987-654-3211',
                  '9876543214', '9876543227', '9876543228', '9876543229'],

        'purchase_amount': [1500.50, 2300.00, 15000.75, 800.25, 4500.00,
                            6700.50, 3200.00, 950.75, 2100.50, 1800.00,
                            7800.25, 4300.50, None,  # missing
                            3600.75, 9200.00, 2300.00, 4500.00,
                            -500.00,  # invalid - negative purchase
                            2800.50, 3100.25]
    }

    return pd.DataFrame(data)


# =============================================================================
# STEP 2: ASSESS DATA QUALITY
# =============================================================================

class DataQualityReport:
    """Generate comprehensive data quality report"""

    def __init__(self, df):
        self.df = df

    def full_report(self):
        """Print complete data quality assessment"""
        print("\n" + "="*80)
        print("📊 DATA QUALITY ASSESSMENT REPORT")
        print("="*80)

        print(f"\n📐 Dataset Shape: {self.df.shape[0]} rows × {self.df.shape[1]} columns")

        # Missing values
        print("\n🔴 MISSING VALUES:")
        missing = self.df.isnull().sum()
        missing_pct = (missing / len(self.df) * 100).round(2)
        missing_df = pd.DataFrame({
            'Missing Count': missing,
            'Missing %': missing_pct
        })
        print(missing_df[missing_df['Missing Count'] > 0].to_string())

        # Duplicates
        print(f"\n🔴 DUPLICATES:")
        exact_dupes = self.df.duplicated().sum()
        print(f"   Exact duplicate rows: {exact_dupes}")

        # Data types
        print(f"\n🔵 DATA TYPES:")
        print(self.df.dtypes.to_string())

        # Numeric summaries
        print(f"\n🔵 NUMERIC COLUMN RANGES:")
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            col_data = self.df[col].dropna()
            print(f"   {col:20s}: min={col_data.min():>12.2f}  max={col_data.max():>12.2f}  mean={col_data.mean():>12.2f}")

        # Value counts for categorical
        print(f"\n🔵 UNIQUE VALUES (categorical):")
        cat_cols = self.df.select_dtypes(include=['object']).columns
        for col in cat_cols:
            unique_count = self.df[col].nunique()
            print(f"   {col:20s}: {unique_count} unique values")

        print("\n" + "="*80)


# =============================================================================
# STEP 3: PROFESSIONAL DATA CLEANER
# =============================================================================

class DataCleaner:
    """
    Professional data cleaning pipeline
    Each method handles one type of data quality issue
    """

    def __init__(self, df):
        self.df = df.copy()
        self.cleaning_log = []
        self.original_shape = df.shape
        print(f"\n✅ DataCleaner initialized with {df.shape[0]} rows, {df.shape[1]} columns")

    def log(self, message):
        """Log cleaning actions"""
        self.cleaning_log.append(message)
        print(f"   ✅ {message}")

    # =========================================================================
    # 1. HANDLE DUPLICATES
    # =========================================================================

    def remove_duplicates(self, subset=None):
        """Remove duplicate rows"""
        print("\n" + "-"*60)
        print("1️⃣ REMOVING DUPLICATES")

        before = len(self.df)
        self.df = self.df.drop_duplicates(subset=subset, keep='first')
        removed = before - len(self.df)

        self.log(f"Removed {removed} duplicate rows ({before} → {len(self.df)})")
        return self

    # =========================================================================
    # 2. HANDLE MISSING VALUES
    # =========================================================================

    def handle_missing_values(self):
        """
        Smart missing value handling - different strategy per column type
        """
        print("\n" + "-"*60)
        print("2️⃣ HANDLING MISSING VALUES")

        # Name: fill with 'Unknown'
        missing_names = self.df['name'].isnull().sum()
        if missing_names > 0:
            self.df['name'] = self.df['name'].fillna('Unknown Customer')
            self.log(f"Filled {missing_names} missing names with 'Unknown Customer'")

        # Age: fill with median (robust to outliers)
        missing_ages = self.df['age'].isnull().sum()
        if missing_ages > 0:
            median_age = self.df['age'].median()
            self.df['age'] = self.df['age'].fillna(median_age)
            self.log(f"Filled {missing_ages} missing ages with median ({median_age})")

        # Salary: fill with median by city (smarter!)
        missing_salary = self.df['salary'].isnull().sum()
        if missing_salary > 0:
            self.df['salary'] = self.df.groupby('city')['salary'].transform(
                lambda x: x.fillna(x.median())
            )
            # If still missing (city had no other salaries), use overall median
            self.df['salary'] = self.df['salary'].fillna(self.df['salary'].median())
            self.log(f"Filled {missing_salary} missing salaries with city median")

        # Purchase amount: fill with 0 (no purchase = 0)
        missing_purchase = self.df['purchase_amount'].isnull().sum()
        if missing_purchase > 0:
            self.df['purchase_amount'] = self.df['purchase_amount'].fillna(0)
            self.log(f"Filled {missing_purchase} missing purchase amounts with 0")

        # Phone: fill with 'Not Provided'
        missing_phone = self.df['phone'].isnull().sum()
        if missing_phone > 0:
            self.df['phone'] = self.df['phone'].fillna('Not Provided')
            self.log(f"Filled {missing_phone} missing phones with 'Not Provided'")

        return self

    # =========================================================================
    # 3. FIX DATA TYPES & FORMATS
    # =========================================================================

    def fix_data_types(self):
        """Fix incorrect data types"""
        print("\n" + "-"*60)
        print("3️⃣ FIXING DATA TYPES")

        # Age to integer (after filling missing)
        self.df['age'] = pd.to_numeric(self.df['age'], errors='coerce').astype('Int64')
        self.log("Converted age to integer type")

        # Salary to float
        self.df['salary'] = pd.to_numeric(self.df['salary'], errors='coerce')
        self.log("Converted salary to numeric")

        # Purchase amount to float
        self.df['purchase_amount'] = pd.to_numeric(
            self.df['purchase_amount'], errors='coerce'
        )
        self.log("Converted purchase_amount to numeric")

        return self

    # =========================================================================
    # 4. STANDARDIZE STRINGS
    # =========================================================================

    def standardize_strings(self):
        """
        Standardize text data:
        - Proper case for names
        - Title case for cities
        - Strip whitespace
        """
        print("\n" + "-"*60)
        print("4️⃣ STANDARDIZING STRINGS")

        # Names: strip whitespace + title case
        self.df['name'] = self.df['name'].str.strip().str.title()
        self.log("Standardized names to Title Case")

        # Cities: strip + title case (mumbai → Mumbai)
        self.df['city'] = self.df['city'].str.strip().str.title()
        self.log("Standardized cities to Title Case")

        return self

    # =========================================================================
    # 5. VALIDATE AND CLEAN WITH REGEX
    # =========================================================================

    def clean_with_regex(self):
        """
        Use regex for pattern-based cleaning
        """
        print("\n" + "-"*60)
        print("5️⃣ CLEANING WITH REGEX")

        # Clean phone numbers - keep only digits, standardize to 10 digits
        def clean_phone(phone):
            if pd.isna(phone) or phone in ['N/A', 'Not Provided']:
                return 'Not Provided'
            # Remove everything except digits
            digits = re.sub(r'\D', '', str(phone))
            # Keep last 10 digits
            if len(digits) >= 10:
                return digits[-10:]
            return 'Invalid'

        before_invalid = (self.df['phone'] == 'Invalid').sum()
        self.df['phone'] = self.df['phone'].apply(clean_phone)
        after_invalid = (self.df['phone'] == 'Invalid').sum()
        self.log(f"Standardized phone numbers to 10-digit format")

        # Validate emails using regex
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

        def validate_email(email):
            if pd.isna(email):
                return 'Invalid'
            if re.match(email_pattern, str(email)):
                return email.lower()
            return 'Invalid'

        invalid_emails = (~self.df['email'].str.contains(
            email_pattern, regex=True, na=True
        )).sum()
        self.df['email'] = self.df['email'].apply(validate_email)
        self.log(f"Validated emails - marked {invalid_emails} as invalid")

        return self

    # =========================================================================
    # 6. PARSE DATES
    # =========================================================================

    def standardize_dates(self):
        """
        Handle multiple date formats and standardize
        """
        print("\n" + "-"*60)
        print("6️⃣ STANDARDIZING DATES")

        def parse_date(date_str):
            if pd.isna(date_str):
                return None

            # Try multiple formats
            formats = [
                '%Y-%m-%d',   # 2022-01-15
                '%Y/%m/%d',   # 2022/01/15
                '%d-%m-%Y',   # 15-01-2022
                '%d/%m/%Y',   # 15/01/2022
            ]

            for fmt in formats:
                try:
                    return datetime.strptime(str(date_str), fmt).date()
                except ValueError:
                    continue

            return None  # Could not parse

        self.df['join_date'] = self.df['join_date'].apply(parse_date)
        self.df['join_date'] = pd.to_datetime(self.df['join_date'])

        failed = self.df['join_date'].isna().sum()
        self.log(f"Standardized all date formats ({failed} could not be parsed)")

        return self

    # =========================================================================
    # 7. HANDLE OUTLIERS
    # =========================================================================

    def handle_outliers(self):
        """
        Detect and handle outliers using IQR method
        """
        print("\n" + "-"*60)
        print("7️⃣ HANDLING OUTLIERS")

        def fix_outliers_iqr(series, column_name):
            """Replace outliers with median"""
            Q1 = series.quantile(0.25)
            Q3 = series.quantile(0.75)
            IQR = Q3 - Q1

            lower = Q1 - 1.5 * IQR
            upper = Q3 + 1.5 * IQR

            outliers = ((series < lower) | (series > upper)).sum()
            median_val = series.median()

            # Replace outliers with median
            series = series.clip(lower=lower, upper=upper)

            return series, outliers, lower, upper

        # Fix age outliers (also fix invalid: negative, > 100)
        self.df['age'] = self.df['age'].clip(lower=18, upper=80)
        self.log("Clipped age to valid range (18-80)")

        # Fix salary outliers using IQR
        clean_salary, n_outliers, lower, upper = fix_outliers_iqr(
            self.df['salary'].dropna(), 'salary'
        )
        self.df.loc[self.df['salary'].notna(), 'salary'] = \
            self.df['salary'].clip(lower=lower, upper=upper)
        self.log(f"Fixed {n_outliers} salary outliers (range: {lower:.0f}-{upper:.0f})")

        # Fix negative purchase amounts
        negative_purchases = (self.df['purchase_amount'] < 0).sum()
        self.df['purchase_amount'] = self.df['purchase_amount'].clip(lower=0)
        self.log(f"Fixed {negative_purchases} negative purchase amounts → set to 0")

        return self

    # =========================================================================
    # 8. ADD DERIVED FEATURES
    # =========================================================================

    def add_derived_features(self):
        """Add useful calculated columns"""
        print("\n" + "-"*60)
        print("8️⃣ ADDING DERIVED FEATURES")

        # Days since joining
        self.df['days_since_joining'] = (
            pd.Timestamp.now() - self.df['join_date']
        ).dt.days
        self.log("Added 'days_since_joining' column")

        # Customer value segment
        self.df['value_segment'] = pd.cut(
            self.df['purchase_amount'],
            bins=[0, 1000, 3000, 7000, float('inf')],
            labels=['Low', 'Medium', 'High', 'VIP']
        )
        self.log("Added 'value_segment' column based on purchase amount")

        # Salary bracket
        self.df['salary_bracket'] = pd.cut(
            self.df['salary'],
            bins=[0, 50000, 75000, 100000, float('inf')],
            labels=['Entry', 'Mid', 'Senior', 'Executive']
        )
        self.log("Added 'salary_bracket' column")

        return self

    # =========================================================================
    # SUMMARY REPORT
    # =========================================================================

    def summary(self):
        """Print cleaning summary"""
        print("\n" + "="*80)
        print("✅ CLEANING COMPLETE - SUMMARY")
        print("="*80)
        print(f"\n📊 Shape: {self.original_shape} → {self.df.shape}")
        print(f"\n📝 Actions taken ({len(self.cleaning_log)} total):")
        for i, action in enumerate(self.cleaning_log, 1):
            print(f"   {i:2d}. {action}")

        # Remaining issues
        remaining_missing = self.df.isnull().sum().sum()
        remaining_dupes = self.df.duplicated().sum()
        print(f"\n📈 Remaining Issues:")
        print(f"   Missing values: {remaining_missing}")
        print(f"   Duplicates: {remaining_dupes}")
        print(f"   Data quality: {'✅ CLEAN' if remaining_missing == 0 and remaining_dupes == 0 else '⚠️ NEEDS REVIEW'}")

        return self

    def get_clean_data(self):
        """Return the cleaned dataframe"""
        return self.df


# =============================================================================
# STEP 4: VISUALIZATION - BEFORE AND AFTER
# =============================================================================

def visualize_cleaning_results(dirty_df, clean_df):
    """Show before/after comparison"""
    print("\n" + "="*80)
    print("📊 VISUALIZING CLEANING RESULTS")
    print("="*80)

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Data Cleaning Results: Before vs After',
                 fontsize=16, fontweight='bold')

    # Chart 1: Missing values comparison
    ax1 = axes[0, 0]
    cols = dirty_df.columns.tolist()
    missing_before = [dirty_df[c].isnull().sum() for c in cols]
    missing_after  = [clean_df[c].isnull().sum() if c in clean_df.columns else 0 for c in cols]
    x = np.arange(len(cols))
    ax1.bar(x - 0.2, missing_before, 0.4, label='Before', color='#EF5350', alpha=0.8)
    ax1.bar(x + 0.2, missing_after,  0.4, label='After',  color='#43A047', alpha=0.8)
    ax1.set_title('Missing Values: Before vs After\n(green = 0 = fully cleaned ✅)')
    ax1.set_xticks(x)
    ax1.set_xticklabels(cols, rotation=45, ha='right')
    ax1.set_ylabel('Missing Count')
    ax1.yaxis.set_major_locator(plt.MaxNLocator(integer=True))
    ax1.legend()

    # Chart 2: Age distribution - shows outlier removal
    ax2 = axes[0, 1]
    dirty_ages = dirty_df['age'].dropna().astype(float)
    clean_ages  = clean_df['age'].dropna().astype(float)
    ax2.hist(dirty_ages, bins=20, alpha=0.6, color='#EF5350',
             label=f'Before (range: {int(dirty_ages.min())}–{int(dirty_ages.max())})')
    ax2.hist(clean_ages,  bins=20, alpha=0.7, color='#43A047',
             label=f'After  (range: {int(clean_ages.min())}–{int(clean_ages.max())})')
    ax2.axvline(18, color='green', linestyle='--', linewidth=1.5, alpha=0.8)
    ax2.axvline(80, color='green', linestyle='--', linewidth=1.5, alpha=0.8)
    ax2.set_title('Age Distribution: Before vs After')
    ax2.set_xlabel('Age')
    ax2.set_ylabel('Count')
    ax2.legend()

    # Chart 3: Salary - show clean distribution, annotate the removed outlier
    ax3 = axes[1, 0]
    dirty_salary = dirty_df['salary'].dropna().astype(float)
    clean_salary  = clean_df['salary'].dropna().astype(float)
    ax3.hist(clean_salary, bins=12, alpha=0.85, color='#43A047', label='After (outlier removed)')
    ax3.set_title('Salary Distribution: Before vs After')
    ax3.set_xlabel('Salary')
    ax3.set_ylabel('Count')
    ax3.text(0.97, 0.95,
             f'Before max: ₹{dirty_salary.max():,.0f}\nAfter  max: ₹{clean_salary.max():,.0f}',
             transform=ax3.transAxes, ha='right', va='top', fontsize=9,
             bbox=dict(boxstyle='round', facecolor='#FFCDD2', alpha=0.9))
    ax3.legend()

    # Chart 4: Customer value segments pie chart
    ax4 = axes[1, 1]
    seg = clean_df['value_segment'].value_counts()
    ax4.pie(seg, labels=seg.index, autopct='%1.1f%%',
            colors=['#FFCDD2', '#FFF9C4', '#C8E6C9', '#B2EBF2'], startangle=90)
    ax4.set_title('Customer Value Segments (After Cleaning)')

    plt.tight_layout()
    plt.savefig('cleaning_results.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("\n✅ Visualization saved: cleaning_results.png")


# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main():
    print("\n📋 OVERVIEW:")
    print("   This dataset simulates real messy data with ALL common problems:")
    print("   - Mixed date formats")
    print("   - Inconsistent capitalization")
    print("   - Duplicates")
    print("   - Missing values")
    print("   - Outliers")
    print("   - Invalid values")
    print("   - Messy phone numbers/emails")

    # Create messy dataset
    input("\nPress Enter to create messy dataset...")
    dirty_df = create_messy_dataset()
    print(f"\n📊 Created messy dataset: {dirty_df.shape}")
    print("\nFirst 5 rows of DIRTY data:")
    print(dirty_df.head().to_string())

    # Quality report
    input("\nPress Enter to see quality report...")
    report = DataQualityReport(dirty_df)
    report.full_report()

    # Clean the data
    input("\nPress Enter to start cleaning...")
    cleaner = DataCleaner(dirty_df)

    (cleaner
        .remove_duplicates(subset=['email'])
        .handle_missing_values()
        .fix_data_types()
        .standardize_strings()
        .clean_with_regex()
        .standardize_dates()
        .handle_outliers()
        .add_derived_features()
        .summary())

    clean_df = cleaner.get_clean_data()

    # Show result
    print("\n✅ First 5 rows of CLEAN data:")
    print(clean_df.head().to_string())

    # Visualize
    input("\nPress Enter to generate visualizations...")
    visualize_cleaning_results(dirty_df, clean_df)

    # Export
    clean_df.to_csv('cleaned_customer_data.csv', index=False)
    print("\n✅ Clean data exported to: cleaned_customer_data.csv")

    print("\n" + "="*80)
    print("🎉 DAY 18: DATA CLEANING MASTERCLASS COMPLETE!")
    print("="*80)
    print("\nTechniques mastered:")
    print("✅ Data quality assessment")
    print("✅ Smart missing value strategies (median by group!)")
    print("✅ Duplicate removal")
    print("✅ String standardization")
    print("✅ Regex for pattern cleaning")
    print("✅ Multi-format date parsing")
    print("✅ IQR outlier detection and treatment")
    print("✅ Derived feature creation")
    print("✅ Before/after visualization")


if __name__ == "__main__":
    main()