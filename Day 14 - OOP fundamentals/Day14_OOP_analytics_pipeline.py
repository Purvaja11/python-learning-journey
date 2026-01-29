"""
Day 14: Object-Oriented Programming for Data Analytics
Complete Analytics Pipeline using OOP principles

This demonstrates how OOP makes data analysis code:
- Reusable
- Organized
- Professional
- Easy to maintain
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

print("=" * 80)
print("🎯 DAY 14: OOP FOR DATA ANALYTICS")
print("=" * 80)


# ============================================================================
# BASE CLASS: DataAnalyzer
# ============================================================================

class DataAnalyzer:
    """
    Base class for data analysis operations
    Provides common functionality for all analyzers
    """
    
    def __init__(self, data_file, name="Dataset"):
        """
        Initialize the analyzer
        
        Parameters:
        -----------
        data_file : str
            Path to CSV file
        name : str
            Name for this dataset
        """
        self.name = name
        self.file_path = data_file
        self.df = None
        self.cleaned = False
        
        print(f"\n📊 Initializing {self.name} Analyzer...")
        self.load_data()
    
    def load_data(self):
        """Load data from CSV file"""
        try:
            self.df = pd.read_csv(self.file_path)
            print(f"✅ Loaded {len(self.df):,} records")
            print(f"   Columns: {list(self.df.columns)}")
        except FileNotFoundError:
            print(f"❌ File not found: {self.file_path}")
        except Exception as e:
            print(f"❌ Error loading data: {e}")
    
    def get_info(self):
        """Display dataset information"""
        if self.df is None:
            print("No data loaded!")
            return
        
        print(f"\n📋 {self.name} Information:")
        print(f"   Shape: {self.df.shape[0]:,} rows × {self.df.shape[1]} columns")
        print(f"   Memory: {self.df.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB")
        print(f"   Cleaned: {'Yes' if self.cleaned else 'No'}")
    
    def get_missing_summary(self):
        """Get summary of missing values"""
        if self.df is None:
            return None
        
        missing = self.df.isnull().sum()
        total = len(self.df)
        
        summary = pd.DataFrame({
            'Missing_Count': missing,
            'Percentage': (missing / total * 100).round(2)
        })
        
        return summary[summary['Missing_Count'] > 0].sort_values('Missing_Count', ascending=False)
    
    def preview(self, n=5):
        """Show first n rows"""
        if self.df is None:
            print("No data loaded!")
            return
        
        print(f"\n👀 First {n} rows of {self.name}:")
        print(self.df.head(n))


# ============================================================================
# DERIVED CLASS: SalesAnalyzer (Inherits from DataAnalyzer)
# ============================================================================

class SalesAnalyzer(DataAnalyzer):
    """
    Specialized analyzer for sales/transaction data
    Extends DataAnalyzer with sales-specific methods
    """
    
    def __init__(self, data_file):
        # Call parent class constructor
        super().__init__(data_file, name="Sales Data")
        
        # Sales-specific attributes
        self.revenue_column = None
        self.date_column = None
        self.category_column = None
    
    def set_columns(self, revenue_col, date_col, category_col=None):
        """
        Configure column names for analysis
        
        Parameters:
        -----------
        revenue_col : str
            Name of revenue/amount column
        date_col : str
            Name of date column
        category_col : str, optional
            Name of category column
        """
        self.revenue_column = revenue_col
        self.date_column = date_col
        self.category_column = category_col
        
        # Convert date column to datetime
        if self.date_column in self.df.columns:
            self.df[self.date_column] = pd.to_datetime(self.df[self.date_column])
            print(f"✅ Configured columns for analysis")
    
    def clean_data(self):
        """Clean the sales data"""
        if self.df is None:
            print("No data to clean!")
            return
        
        print(f"\n🧹 Cleaning {self.name}...")
        
        initial_rows = len(self.df)
        
        # Remove rows with missing revenue
        if self.revenue_column:
            self.df = self.df.dropna(subset=[self.revenue_column])
        
        # Fill missing categories with 'Unknown'
        if self.category_column and self.category_column in self.df.columns:
            self.df[self.category_column].fillna('Unknown', inplace=True)
        
        # Remove duplicates
        duplicates = self.df.duplicated().sum()
        if duplicates > 0:
            self.df = self.df.drop_duplicates()
            print(f"   Removed {duplicates} duplicates")
        
        rows_removed = initial_rows - len(self.df)
        if rows_removed > 0:
            print(f"   Removed {rows_removed} rows ({rows_removed/initial_rows*100:.1f}%)")
        
        self.cleaned = True
        print(f"✅ Cleaning complete! {len(self.df):,} records remain")
    
    def get_revenue_summary(self):
        """Calculate revenue statistics"""
        if not self.revenue_column:
            print("Revenue column not set!")
            return None
        
        stats = {
            'Total Revenue': self.df[self.revenue_column].sum(),
            'Average Sale': self.df[self.revenue_column].mean(),
            'Median Sale': self.df[self.revenue_column].median(),
            'Min Sale': self.df[self.revenue_column].min(),
            'Max Sale': self.df[self.revenue_column].max(),
            'Std Dev': self.df[self.revenue_column].std()
        }
        
        print(f"\n💰 Revenue Summary:")
        for key, value in stats.items():
            print(f"   {key}: ${value:,.2f}")
        
        return stats
    
    def get_top_categories(self, n=5):
        """Get top n categories by revenue"""
        if not self.category_column or not self.revenue_column:
            print("Category or revenue column not set!")
            return None
        
        top_categories = self.df.groupby(self.category_column)[self.revenue_column].sum().sort_values(ascending=False).head(n)
        
        print(f"\n🏆 Top {n} Categories by Revenue:")
        for i, (category, revenue) in enumerate(top_categories.items(), 1):
            print(f"   {i}. {category}: ${revenue:,.2f}")
        
        return top_categories
    
    def plot_revenue_trend(self, period='M'):
        """
        Plot revenue over time
        
        Parameters:
        -----------
        period : str
            'D' for daily, 'W' for weekly, 'M' for monthly
        """
        if not self.date_column or not self.revenue_column:
            print("Date or revenue column not set!")
            return
        
        # Group by period
        self.df.set_index(self.date_column, inplace=True)
        revenue_trend = self.df[self.revenue_column].resample(period).sum()
        self.df.reset_index(inplace=True)
        
        # Plot
        plt.figure(figsize=(12, 6))
        plt.plot(revenue_trend.index, revenue_trend.values, 
                marker='o', linewidth=2, markersize=6)
        
        period_names = {'D': 'Daily', 'W': 'Weekly', 'M': 'Monthly'}
        plt.title(f'{period_names.get(period, period)} Revenue Trend', 
                 fontsize=16, fontweight='bold', pad=20)
        plt.xlabel('Date', fontsize=12)
        plt.ylabel('Revenue ($)', fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        filename = f'revenue_trend_{period}.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.show()
        
        print(f"✅ Saved: {filename}")


# ============================================================================
# DERIVED CLASS: CustomerAnalyzer
# ============================================================================

class CustomerAnalyzer(DataAnalyzer):
    """
    Specialized analyzer for customer data
    """
    
    def __init__(self, data_file):
        super().__init__(data_file, name="Customer Data")
        self.age_column = None
        self.gender_column = None
    
    def set_columns(self, age_col, gender_col=None):
        """Configure demographic columns"""
        self.age_column = age_col
        self.gender_column = gender_col
        print(f"✅ Configured customer columns")
    
    def get_age_distribution(self):
        """Analyze age distribution"""
        if not self.age_column:
            print("Age column not set!")
            return
        
        ages = self.df[self.age_column].dropna()
        
        print(f"\n👥 Age Distribution:")
        print(f"   Mean Age: {ages.mean():.1f}")
        print(f"   Median Age: {ages.median():.1f}")
        print(f"   Age Range: {ages.min():.0f} - {ages.max():.0f}")
        
        # Create age groups
        age_groups = pd.cut(ages, bins=[0, 25, 35, 45, 60, 100],
                           labels=['18-25', '26-35', '36-45', '46-60', '60+'])
        
        group_counts = age_groups.value_counts().sort_index()
        
        print(f"\n   Age Groups:")
        for group, count in group_counts.items():
            pct = count / len(ages) * 100
            print(f"   {group}: {count:,} ({pct:.1f}%)")
        
        return group_counts
    
    def plot_demographics(self):
        """Plot customer demographics"""
        if not self.gender_column:
            print("Gender column not set!")
            return
        
        gender_counts = self.df[self.gender_column].value_counts()
        
        plt.figure(figsize=(8, 8))
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
        plt.pie(gender_counts.values, labels=gender_counts.index,
               autopct='%1.1f%%', colors=colors, startangle=90)
        plt.title('Customer Gender Distribution', 
                 fontsize=16, fontweight='bold', pad=20)
        plt.tight_layout()
        
        plt.savefig('customer_demographics.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print("✅ Saved: customer_demographics.png")


# ============================================================================
# DEMONSTRATION
# ============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("🚀 DEMONSTRATION: OOP Analytics Pipeline")
    print("=" * 80)
    
    # Example 1: Sales Analysis
    print("\n" + "-" * 80)
    print("EXAMPLE 1: Sales Analysis with OOP")
    print("-" * 80)
    
    # Create sales analyzer
    sales = SalesAnalyzer('ecommerce_orders.csv')
    
    # Configure columns
    sales.set_columns(revenue_col='Final_Amount', 
                     date_col='Order_Date',
                     category_col='Category')
    
    # Get basic info
    sales.get_info()
    
    # Preview data
    sales.preview(3)
    
    # Check for missing data
    print("\n📋 Missing Data:")
    print(sales.get_missing_summary())
    
    # Clean data
    sales.clean_data()
    
    # Analyze
    sales.get_revenue_summary()
    sales.get_top_categories(5)
    
    # Visualize
    sales.plot_revenue_trend('M')
    
    
    # Example 2: Customer Analysis
    print("\n" + "-" * 80)
    print("EXAMPLE 2: Customer Analysis with OOP")
    print("-" * 80)
    
    # Create customer analyzer
    customers = CustomerAnalyzer('ecommerce_customers.csv')
    
    # Configure columns
    customers.set_columns(age_col='Age', gender_col='Gender')
    
    # Analyze
    customers.get_age_distribution()
    customers.plot_demographics()
    
    
    print("\n" + "=" * 80)
    print("✅ OOP ANALYTICS DEMONSTRATION COMPLETE!")
    print("=" * 80)
    
    print("""
    
🎯 KEY OOP CONCEPTS DEMONSTRATED:

1. CLASSES & OBJECTS:
   ✅ Created reusable analyzer classes
   ✅ Instantiated multiple analyzer objects

2. INHERITANCE:
   ✅ DataAnalyzer (base class)
   ✅ SalesAnalyzer (inherits from DataAnalyzer)
   ✅ CustomerAnalyzer (inherits from DataAnalyzer)

3. ENCAPSULATION:
   ✅ Data stored as private attributes
   ✅ Accessed through public methods
   ✅ Validation in methods

4. METHODS:
   ✅ __init__ (constructor)
   ✅ Instance methods (using self)
   ✅ Reusable analysis functions

5. CODE REUSE:
   ✅ Common functionality in base class
   ✅ Specialized methods in derived classes
   ✅ Don't repeat yourself (DRY principle)

    """)