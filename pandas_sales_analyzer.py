"""
Sales Data Analyzer with Pandas - Day 9 Project
Demonstrates: DataFrames, filtering, grouping, aggregation, real data analysis

This is REAL data analytics work!
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class SalesAnalyzer:
    """Analyze sales data using Pandas"""
    
    def __init__(self):
        self.df = None
    
    def create_sample_data(self):
        """Generate realistic sample sales data"""
        np.random.seed(42)
        
        # Generate 200 sales records over 30 days
        n_records = 200
        
        products = ['Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Webcam', 
                   'Headphones', 'USB Cable', 'External Drive', 'Router', 'Printer']
        categories = ['Electronics', 'Accessories', 'Accessories', 'Electronics', 'Accessories',
                     'Accessories', 'Accessories', 'Storage', 'Networking', 'Office']
        regions = ['North', 'South', 'East', 'West']
        customers = ['Customer_' + str(i) for i in range(1, 51)]
        
        # Generate dates
        start_date = datetime(2024, 1, 1)
        dates = [start_date + timedelta(days=np.random.randint(0, 30)) for _ in range(n_records)]
        
        # Generate data
        data = {
            'Date': dates,
            'Product': np.random.choice(products, n_records),
            'Category': [categories[products.index(p)] for p in np.random.choice(products, n_records)],
            'Quantity': np.random.randint(1, 20, n_records),
            'Unit_Price': np.random.randint(20, 2000, n_records),
            'Region': np.random.choice(regions, n_records),
            'Customer_ID': np.random.choice(customers, n_records)
        }
        
        self.df = pd.DataFrame(data)
        
        # Calculate total
        self.df['Total'] = self.df['Quantity'] * self.df['Unit_Price']
        
        # Convert date to datetime
        self.df['Date'] = pd.to_datetime(self.df['Date'])
        
        # Add derived columns
        self.df['Month'] = self.df['Date'].dt.month_name()
        self.df['Day'] = self.df['Date'].dt.day
        self.df['Weekday'] = self.df['Date'].dt.day_name()
        
        print(f"✓ Created {len(self.df)} sales records")
        return True
    
    def load_from_csv(self, filename):
        """Load data from CSV file"""
        try:
            self.df = pd.read_csv(filename)
            self.df['Date'] = pd.to_datetime(self.df['Date'])
            print(f"✓ Loaded {len(self.df)} records from {filename}")
            return True
        except Exception as e:
            print(f"✗ Error: {e}")
            return False
    
    def save_to_csv(self, filename='pandas_sales_data.csv'):
        """Save data to CSV"""
        try:
            self.df.to_csv(filename, index=False)
            print(f"✓ Data saved to {filename}")
            return True
        except Exception as e:
            print(f"✗ Error: {e}")
            return False
    
    def view_sample(self, n=10):
        """View sample data"""
        print("\n📋 SAMPLE DATA:")
        print("="*80)
        print(self.df.head(n))
        print(f"\nShowing first {n} of {len(self.df)} records")
    
    def get_summary_stats(self):
        """Get overall statistics"""
        print("\n📊 SUMMARY STATISTICS:")
        print("="*80)
        print(f"Total Records:     {len(self.df):,}")
        print(f"Date Range:        {self.df['Date'].min().date()} to {self.df['Date'].max().date()}")
        print(f"Total Revenue:     ${self.df['Total'].sum():,.2f}")
        print(f"Average Sale:      ${self.df['Total'].mean():,.2f}")
        print(f"Median Sale:       ${self.df['Total'].median():,.2f}")
        print(f"Total Units Sold:  {self.df['Quantity'].sum():,}")
        print(f"Unique Products:   {self.df['Product'].nunique()}")
        print(f"Unique Customers:  {self.df['Customer_ID'].nunique()}")
    
    def sales_by_product(self):
        """Analyze sales by product"""
        print("\n🏆 SALES BY PRODUCT:")
        print("="*80)
        
        product_sales = self.df.groupby('Product').agg({
            'Total': 'sum',
            'Quantity': 'sum',
            'Customer_ID': 'nunique'
        }).round(2)
        
        product_sales.columns = ['Revenue', 'Units_Sold', 'Unique_Customers']
        product_sales = product_sales.sort_values('Revenue', ascending=False)
        
        print(product_sales)
        
        # Top performer
        top_product = product_sales.index[0]
        top_revenue = product_sales.iloc[0]['Revenue']
        print(f"\n🌟 Top Product: {top_product} (${top_revenue:,.2f})")
    
    def sales_by_region(self):
        """Analyze sales by region"""
        print("\n🗺️ SALES BY REGION:")
        print("="*80)
        
        region_sales = self.df.groupby('Region').agg({
            'Total': ['sum', 'mean', 'count']
        }).round(2)
        
        region_sales.columns = ['Total_Revenue', 'Avg_Sale', 'Transactions']
        region_sales = region_sales.sort_values('Total_Revenue', ascending=False)
        
        print(region_sales)
        
        # Calculate percentages
        total_revenue = self.df['Total'].sum()
        region_sales['Percentage'] = (region_sales['Total_Revenue'] / total_revenue * 100).round(1)
        
        print("\n% of Total Revenue:")
        print(region_sales['Percentage'])
    
    def sales_by_category(self):
        """Analyze sales by category"""
        print("\n📦 SALES BY CATEGORY:")
        print("="*80)
        
        category_sales = self.df.groupby('Category').agg({
            'Total': 'sum',
            'Quantity': 'sum'
        }).round(2)
        
        category_sales.columns = ['Revenue', 'Units']
        category_sales = category_sales.sort_values('Revenue', ascending=False)
        
        print(category_sales)
    
    def daily_sales_trend(self):
        """Analyze daily sales trend"""
        print("\n📈 DAILY SALES TREND:")
        print("="*80)
        
        daily = self.df.groupby('Date')['Total'].sum().sort_index()
        
        print(f"Average daily revenue: ${daily.mean():,.2f}")
        print(f"Best day: {daily.idxmax().date()} (${daily.max():,.2f})")
        print(f"Worst day: {daily.idxmin().date()} (${daily.min():,.2f})")
        
        # Show trend
        first_week = daily.iloc[:7].mean()
        last_week = daily.iloc[-7:].mean()
        change = ((last_week - first_week) / first_week) * 100
        
        print(f"\nTrend: {'+' if change > 0 else ''}{change:.1f}% "
              f"({'Growing' if change > 0 else 'Declining'})")
    
    def top_customers(self, n=10):
        """Find top customers"""
        print(f"\n👥 TOP {n} CUSTOMERS:")
        print("="*80)
        
        customer_stats = self.df.groupby('Customer_ID').agg({
            'Total': 'sum',
            'Product': 'count'
        }).round(2)
        
        customer_stats.columns = ['Total_Spent', 'Num_Purchases']
        customer_stats = customer_stats.sort_values('Total_Spent', ascending=False)
        
        print(customer_stats.head(n))
    
    def filter_data(self, **kwargs):
        """Filter data based on criteria"""
        filtered = self.df.copy()
        
        if 'product' in kwargs:
            filtered = filtered[filtered['Product'] == kwargs['product']]
        
        if 'region' in kwargs:
            filtered = filtered[filtered['Region'] == kwargs['region']]
        
        if 'min_amount' in kwargs:
            filtered = filtered[filtered['Total'] >= kwargs['min_amount']]
        
        if 'date_from' in kwargs:
            filtered = filtered[filtered['Date'] >= kwargs['date_from']]
        
        print(f"\n🔍 FILTERED RESULTS: {len(filtered)} records")
        print("="*80)
        print(filtered.head(10))
        
        if len(filtered) > 0:
            print(f"\nFiltered Total Revenue: ${filtered['Total'].sum():,.2f}")
    
    def product_performance_matrix(self):
        """Create product performance matrix"""
        print("\n📊 PRODUCT PERFORMANCE MATRIX:")
        print("="*80)
        
        matrix = self.df.pivot_table(
            values='Total',
            index='Product',
            columns='Region',
            aggfunc='sum',
            fill_value=0
        ).round(2)
        
        print(matrix)
        
        # Add totals
        matrix['Total'] = matrix.sum(axis=1)
        print("\nWith Totals:")
        print(matrix.sort_values('Total', ascending=False))
    
    def weekday_analysis(self):
        """Analyze sales by day of week"""
        print("\n📅 WEEKDAY ANALYSIS:")
        print("="*80)
        
        weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 
                        'Friday', 'Saturday', 'Sunday']
        
        weekday_sales = self.df.groupby('Weekday')['Total'].agg(['sum', 'mean', 'count'])
        weekday_sales.columns = ['Total', 'Average', 'Transactions']
        
        # Reorder by weekday
        weekday_sales = weekday_sales.reindex(weekday_order)
        
        print(weekday_sales.round(2))
        
        best_day = weekday_sales['Total'].idxmax()
        print(f"\n🎯 Best Day: {best_day}")
    
    def generate_report(self, filename='pandas_sales_report.txt'):
        """Generate comprehensive report"""
        try:
            with open(filename, 'w') as f:
                f.write("="*80 + "\n")
                f.write("SALES ANALYSIS REPORT\n")
                f.write("="*80 + "\n\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
                
                # Summary stats
                f.write("-"*80 + "\n")
                f.write("SUMMARY STATISTICS\n")
                f.write("-"*80 + "\n")
                f.write(f"Total Records: {len(self.df):,}\n")
                f.write(f"Total Revenue: ${self.df['Total'].sum():,.2f}\n")
                f.write(f"Average Sale: ${self.df['Total'].mean():,.2f}\n\n")
                
                # Top products
                f.write("-"*80 + "\n")
                f.write("TOP 5 PRODUCTS\n")
                f.write("-"*80 + "\n")
                top_products = self.df.groupby('Product')['Total'].sum().sort_values(ascending=False).head(5)
                for i, (product, revenue) in enumerate(top_products.items(), 1):
                    f.write(f"{i}. {product}: ${revenue:,.2f}\n")
                
                f.write("\n" + "="*80 + "\n")
            
            print(f"✓ Report saved to {filename}")
            return True
        except Exception as e:
            print(f"✗ Error: {e}")
            return False

# Main program
def main():
    print("="*80)
    print("PANDAS SALES DATA ANALYZER")
    print("="*80)
    
    analyzer = SalesAnalyzer()
    
    while True:
        print("\n" + "="*80)
        print("MAIN MENU")
        print("="*80)
        print("1. Create sample data")
        print("2. Load from CSV")
        print("3. Exit")
        
        choice = input("\nChoose (1-3): ")
        
        if choice == "1":
            analyzer.create_sample_data()
            analyzer.save_to_csv()
        elif choice == "2":
            filename = input("Enter filename: ").strip()
            if not analyzer.load_from_csv(filename):
                continue
        elif choice == "3":
            print("\n👋 Goodbye!")
            break
        else:
            print("✗ Invalid choice!")
            continue
        
        # Analysis menu
        while True:
            print("\n" + "="*80)
            print("ANALYSIS MENU")
            print("="*80)
            print("1.  View sample data")
            print("2.  Summary statistics")
            print("3.  Sales by product")
            print("4.  Sales by region")
            print("5.  Sales by category")
            print("6.  Daily sales trend")
            print("7.  Top customers")
            print("8.  Product performance matrix")
            print("9.  Weekday analysis")
            print("10. Filter data")
            print("11. Generate report")
            print("12. Back to main menu")
            
            analysis = input("\nChoose (1-12): ")
            
            if analysis == "1":
                analyzer.view_sample()
            elif analysis == "2":
                analyzer.get_summary_stats()
            elif analysis == "3":
                analyzer.sales_by_product()
            elif analysis == "4":
                analyzer.sales_by_region()
            elif analysis == "5":
                analyzer.sales_by_category()
            elif analysis == "6":
                analyzer.daily_sales_trend()
            elif analysis == "7":
                n = int(input("How many top customers? (default 10): ") or 10)
                analyzer.top_customers(n)
            elif analysis == "8":
                analyzer.product_performance_matrix()
            elif analysis == "9":
                analyzer.weekday_analysis()
            elif analysis == "10":
                print("\nFilter options (press Enter to skip):")
                product = input("Product name: ").strip() or None
                region = input("Region: ").strip() or None
                min_amount = input("Minimum amount: ").strip()
                min_amount = float(min_amount) if min_amount else None
                
                filters = {}
                if product: filters['product'] = product
                if region: filters['region'] = region
                if min_amount: filters['min_amount'] = min_amount
                
                analyzer.filter_data(**filters)
            elif analysis == "11":
                analyzer.generate_report()
            elif analysis == "12":
                break
            else:
                print("✗ Invalid choice!")

if __name__ == "__main__":
    main()