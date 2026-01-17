"""
Complete Data Cleaning Pipeline - Day 11 Project
Handles: Missing values, duplicates, outliers, inconsistencies, validation

This is production-ready data cleaning!
"""

import pandas as pd
import numpy as np
from datetime import datetime

class DataCleaner:
    """Comprehensive data cleaning pipeline"""
    
    def __init__(self, df):
        self.df = df.copy()
        self.original_df = df.copy()
        self.cleaning_log = []
    
    def log_action(self, action):
        """Log cleaning actions"""
        self.cleaning_log.append(action)
        print(f"  ✓ {action}")
    
    def get_data_profile(self):
        """Generate data quality report"""
        print("\n" + "="*70)
        print("📊 DATA QUALITY REPORT")
        print("="*70)
        
        print(f"\nDataset Shape: {self.df.shape}")
        print(f"Rows: {self.df.shape[0]:,}, Columns: {self.df.shape[1]}")
        
        # Missing values
        print("\n" + "-"*70)
        print("MISSING VALUES:")
        missing = self.df.isnull().sum()
        missing_pct = (missing / len(self.df)) * 100
        
        for col in self.df.columns:
            if missing[col] > 0:
                print(f"  {col}: {missing[col]} ({missing_pct[col]:.1f}%)")
        
        if missing.sum() == 0:
            print("  ✓ No missing values")
        
        # Duplicates
        print("\n" + "-"*70)
        duplicates = self.df.duplicated().sum()
        print(f"DUPLICATES: {duplicates} rows")
        
        # Data types
        print("\n" + "-"*70)
        print("DATA TYPES:")
        for col, dtype in self.df.dtypes.items():
            print(f"  {col}: {dtype}")
        
        # Memory usage
        print("\n" + "-"*70)
        memory_mb = self.df.memory_usage(deep=True).sum() / 1024**2
        print(f"MEMORY USAGE: {memory_mb:.2f} MB")
    
    def handle_missing_values(self, strategy='auto'):
        """Handle missing values intelligently"""
        print("\n🔧 HANDLING MISSING VALUES...")
        
        for col in self.df.columns:
            missing_count = self.df[col].isnull().sum()
            
            if missing_count == 0:
                continue
            
            missing_pct = (missing_count / len(self.df)) * 100
            
            # If >50% missing, consider dropping column
            if missing_pct > 50:
                if input(f"  Column '{col}' has {missing_pct:.1f}% missing. Drop? (y/n): ").lower() == 'y':
                    self.df = self.df.drop(columns=[col])
                    self.log_action(f"Dropped column '{col}' (too many missing values)")
                    continue
            
            # Strategy based on data type
            if self.df[col].dtype in ['int64', 'float64']:
                # Numeric: fill with median
                median_val = self.df[col].median()
                self.df[col] = self.df[col].fillna(median_val)
                self.log_action(f"Filled {missing_count} missing values in '{col}' with median ({median_val:.2f})")
            
            else:
                # Categorical: fill with mode or 'Unknown'
                if self.df[col].mode().empty:
                    self.df[col] = self.df[col].fillna('Unknown')
                    self.log_action(f"Filled {missing_count} missing values in '{col}' with 'Unknown'")
                else:
                    mode_val = self.df[col].mode()[0]
                    self.df[col] = self.df[col].fillna(mode_val)
                    self.log_action(f"Filled {missing_count} missing values in '{col}' with mode ('{mode_val}')")
    
    def remove_duplicates(self):
        """Remove duplicate rows"""
        print("\n🔧 REMOVING DUPLICATES...")
        
        duplicates_before = self.df.duplicated().sum()
        
        if duplicates_before == 0:
            self.log_action("No duplicates found")
            return
        
        self.df = self.df.drop_duplicates()
        self.log_action(f"Removed {duplicates_before} duplicate rows")
    
    def handle_outliers(self, columns=None, method='iqr'):
        """Detect and handle outliers"""
        print("\n🔧 HANDLING OUTLIERS...")
        
        if columns is None:
            columns = self.df.select_dtypes(include=[np.number]).columns
        
        for col in columns:
            if col not in self.df.columns:
                continue
            
            # IQR method
            Q1 = self.df[col].quantile(0.25)
            Q3 = self.df[col].quantile(0.75)
            IQR = Q3 - Q1
            
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outliers = ((self.df[col] < lower_bound) | (self.df[col] > upper_bound)).sum()
            
            if outliers > 0:
                print(f"\n  Column: {col}")
                print(f"  Outliers detected: {outliers}")
                print(f"  Valid range: {lower_bound:.2f} to {upper_bound:.2f}")
                
                action = input(f"  Action? (1=Remove, 2=Cap, 3=Keep): ")
                
                if action == '1':
                    mask = (self.df[col] >= lower_bound) & (self.df[col] <= upper_bound)
                    removed = (~mask).sum()
                    self.df = self.df[mask]
                    self.log_action(f"Removed {removed} outliers from '{col}'")
                
                elif action == '2':
                    self.df[col] = self.df[col].clip(lower=lower_bound, upper=upper_bound)
                    self.log_action(f"Capped {outliers} outliers in '{col}'")
                
                else:
                    self.log_action(f"Kept {outliers} outliers in '{col}'")
    
    def standardize_text(self, columns=None):
        """Standardize text columns"""
        print("\n🔧 STANDARDIZING TEXT...")
        
        if columns is None:
            columns = self.df.select_dtypes(include=['object']).columns
        
        
        for col in columns:
            if col not in self.df.columns:
                continue
            if 'date' in col.lower():
                continue
        
            # Strip whitespace
            mask = self.df[col].notna()
            before = self.df.loc[mask, col].astype(str).str.strip()
            changed = (self.df.loc[mask, col] != before).sum()
            
            if changed > 0:
                self.df.loc[mask, col] = before
                self.log_action(f"Removed whitespace from {changed} values in '{col}'")
            
            # Standardize case (ask user)
            print(f"\n  Column: {col}")
            print(f"  Sample values: {self.df[col].head(3).tolist()}")
            case_action = input("  Standardize case? (1=Title, 2=Lower, 3=Upper, 4=Skip): ")
            
            if case_action == '1':
                self.df[col] = self.df[col].str.title()
                self.log_action(f"Converted '{col}' to title case")
            elif case_action == '2':
                self.df[col] = self.df[col].str.lower()
                self.log_action(f"Converted '{col}' to lowercase")
            elif case_action == '3':
                self.df[col] = self.df[col].str.upper()
                self.log_action(f"Converted '{col}' to uppercase")
    
    def fix_data_types(self):
        """Fix incorrect data types"""
        print("\n🔧 FIXING DATA TYPES...")
        
        skip_numeric = ['Employee_ID', 'Name', 'Department', 'City']
        for col in self.df.columns:
            if col in skip_numeric:
                continue

            # Try to convert to numeric if possible
            if self.df[col].dtype == 'object':
                try:
                    converted = pd.to_numeric(self.df[col], errors='coerce')
                    if converted.notna().sum() / len(converted) > 0.8:
                        self.df[col] = converted
                        self.log_action(f"Converted '{col}' to numeric")
                except:
                    pass
            
            # Check for date columns
            if 'date' in col.lower() or 'time' in col.lower():
                try:
                    self.df[col] = pd.to_datetime(self.df[col], errors='coerce')
                    if self.df[col].dtype == 'datetime64[ns]':
                        self.log_action(f"Converted '{col}' to datetime")
                except:
                    pass
    
    def validate_data(self):
        """Validate cleaned data"""
        print("\n" + "="*70)
        print("🔍 DATA VALIDATION")
        print("="*70)
        
        issues = []
        
        # Check missing values
        missing = self.df.isnull().sum().sum()
        if missing > 0:
            issues.append(f"Still has {missing} missing values")
        else:
            print("  ✓ No missing values")
        
        # Check duplicates
        duplicates = self.df.duplicated().sum()
        if duplicates > 0:
            issues.append(f"Still has {duplicates} duplicates")
        else:
            print("  ✓ No duplicates")
        
        # Check for negative values in numeric columns
        non_numeric_cols = ['Age', 'Salary', 'Years_Experience']
        for col in non_numeric_cols:
            if col in self.df.columns:
                negative = (self.df[col] < 0).sum()
                if negative > 0:
                    issues.append(f"'{col}' has {negative} negative values")
        
        if not issues:
            print("  ✓ All validation checks passed!")
        else:
            print("\n  ⚠️ Issues found:")
            for issue in issues:
                print(f"    - {issue}")
        
        return len(issues) == 0
    
    def get_cleaning_report(self):
        """Generate cleaning summary"""
        print("\n" + "="*70)
        print("📋 CLEANING SUMMARY")
        print("="*70)
        
        print(f"\nOriginal shape: {self.original_df.shape}")
        print(f"Cleaned shape:  {self.df.shape}")
        print(f"Rows removed:   {self.original_df.shape[0] - self.df.shape[0]}")
        
        print("\n" + "-"*70)
        print("ACTIONS PERFORMED:")
        for i, action in enumerate(self.cleaning_log, 1):
            print(f"{i}. {action}")
    
    def save_cleaned_data(self, filename='cleaned_data.csv'):
        """Save cleaned dataset"""
        try:
            self.df.to_csv(filename, index=False)
            print(f"\n✓ Cleaned data saved to '{filename}'")
            return True
        except Exception as e:
            print(f"\n✗ Error saving: {e}")
            return False

# Main function
def main():
    print("="*70)
    print("DATA CLEANING PIPELINE")
    print("="*70)
    
    # Load data
    print("\n1. Load your dataset")
    print("  Option 1: Use sample messy data")
    print("  Option 2: Load from CSV file")
    
    choice = input("\nChoice (1/2): ")
    
    if choice == '1':
        # Generate sample messy data
        df = pd.DataFrame({
            'Name': ['  Alice  ', 'Bob', 'Charlie', 'Alice', None, 'Diana'],
            'Age': [25, 999, 30, 25, 28, -5],
            'Salary': [50000, 60000, np.nan, 50000, 52000, 65000],
            'City': ['mumbai', 'DELHI', 'Bangalore', 'Mumbai', 'delhi', 'bangalore'],
            'Date': ['2024-01-01', '2024-01-02', 'invalid', '2024-01-01', '2024-01-04', '2024-01-05']
        })
        print("\n✓ Sample messy data loaded")
    
    else:
        filename = input("Enter CSV filename: ")
        try:
            df = pd.read_csv(filename)
            print(f"\n✓ Loaded {len(df)} rows from '{filename}'")
        except Exception as e:
            print(f"\n✗ Error: {e}")
            return
    
    # Create cleaner
    cleaner = DataCleaner(df)
    
    # Show initial profile
    cleaner.get_data_profile()
    
    # Interactive cleaning
    while True:
        print("\n" + "="*70)
        print("CLEANING MENU")
        print("="*70)
        print("1. Handle missing values")
        print("2. Remove duplicates")
        print("3. Handle outliers")
        print("4. Standardize text")
        print("5. Fix data types")
        print("6. Validate data")
        print("7. View cleaning report")
        print("8. Save cleaned data")
        print("9. Exit")
        
        choice = input("\nChoose (1-9): ")
        
        if choice == '1':
            cleaner.handle_missing_values()
        elif choice == '2':
            cleaner.remove_duplicates()
        elif choice == '3':
            cleaner.handle_outliers()
        elif choice == '4':
            cleaner.standardize_text()
        elif choice == '5':
            cleaner.fix_data_types()
        elif choice == '6':
            cleaner.validate_data()
        elif choice == '7':
            cleaner.get_cleaning_report()
        elif choice == '8':
            filename = input("Enter filename (default: 'cleaned_data.csv'): ").strip()
            if not filename:
                filename = 'cleaned_data.csv'
            cleaner.save_cleaned_data(filename)
        elif choice == '9':
            print("\n✓ Cleaning complete!")
            cleaner.get_cleaning_report()
            print("\n👋 Goodbye!")
            break
        else:
            print("✗ Invalid choice!")

if __name__ == "__main__":
    main()