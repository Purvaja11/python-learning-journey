"""Retail Analytics Dashboard - Day 10 Task 3 Project
Advanced Pandas: Merging, time series, pivot tables, real analytics

This mimics real data analyst work!
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class RetailAnalytics:
    """Advanced Retail data analysis"""

    def __init__(self):
        self.customers = None
        self.transaction = None
        self.merged_data = None

    def load_from_first_csv(self, filename):
        """Load data from first csv file"""
        try:
            self.customers = pd.read_csv(filename)
            self.customers['Date'] = pd.to_datetime(self.customers['registration_date'])
            
            print(f"✓ Loaded {len(self.customers)} records from {filename}")
            
            return True
        except Exception as e:
            print(f"X Error: {e}")
            return False
        
    def load_from_second_csv(self, filename):
        """Load data from second csv file"""
        try:
            self.transaction = pd.read_csv(filename)
            self.transaction['Date'] = pd.to_datetime(self.transaction['transaction_date'])
            print(f"✓ Loaded {len(self.transaction)} records from {filename}")
            return True
        except Exception as e:
            print(f"X Error: {e}")
            return False

    def merge_all_data(self):
        """Merge all tables for comprehensive analysis"""
        print("\n🔗 Merging all data...")
        #Merge customers and transcation
        self.merged_data = pd.merge(
            self.customers,
            self.transaction,
            on='customer_id',
            how='left'
        )

        self.merged_data.rename(columns={
        'Date_x': 'Registration_Date',
        'Date_y': 'Transaction_Date'
        },inplace=True)
        # Ensure datetime
        self.merged_data['Transaction_Date'] = pd.to_datetime(self.merged_data['Transaction_Date'])

        #Calculate total
        self.merged_data['Total'] = self.merged_data['quantity'] * self.merged_data['price']

        # Add time-based columns
        self.merged_data['Month'] = self.merged_data['Transaction_Date'].dt.month_name()
        self.merged_data['Week'] = self.merged_data['Transaction_Date'].dt.isocalendar().week
        self.merged_data['Weekday'] = self.merged_data['Transaction_Date'].dt.day_name()

        print(f"✓ Merged data shape: {self.merged_data.shape}")
        return True
    
    def sales_overview(self):
        """Overall sales statistics"""
        print("\n" + "="*70)
        print("📊 SALES OVERVIEW")
        print("="*70)

        total_revenue = self.merged_data['Total'].sum()
        total_orders = self.merged_data['transaction_id'].nunique()
        total_customers = self.merged_data['customer_id'].nunique()
        avg_order_value = total_revenue / total_orders

        print(f"\nTotal Revenue:        ₹{total_revenue:,.0f}")
        print(f"Total Transacation:    {total_orders:,}")
        print(f"Unique Order Value:    {total_customers:,}")
        print(f"Average Order Value:   ₹{avg_order_value}")
        print(f"Repeat Customer Rate:  {(total_orders - total_customers) / total_orders * 100:.1f}%")

    def product_analysis(self):
        """Analyze product performance"""
        print("\n" + "="*70)
        print("🏆 PRODUCT PERFORMANCE")
        print("="*70)

        product_stats = self.merged_data.groupby('product_name').agg({
            'Total': 'sum',
            'quantity':'sum',
            'transaction_id':'nunique'
        }).round(0)

        product_stats.columns = ['Revenue', 'Units_Sold', 'Orders']
        product_stats = product_stats.sort_values('Revenue', ascending=False)

        print("\nTop 5 Products by Revenue: ")
        print(product_stats.head())
        
        #category analysis
        category_stats = self.merged_data.groupby('product_category')['Total'].sum().sort_values(ascending=False)
        print("\nRevenue by Category: ")
        print(category_stats)

    def customer_analysis(self):
        """Analyze customer behaviour"""
        print("\n" + "="*70)
        print("👥 CUSTOMER ANALYSIS")
        print("="*70)

        customer_stats = self.merged_data.groupby('customer_id').agg({
            'Total':'sum',
            'transaction_id':'nunique'
        })

        customer_stats.columns = ['Total_Spent', 'Order_Count']
        customer_stats = customer_stats.sort_values('Total_Spent', ascending=False)

        print("\nTop 10 Customers:")
        top_10 = customer_stats.head(10)
        print(top_10)

        # Customer segmentation
        print("\n" + "-"*70)
        print("Customer Segmentation:")

        high_value = len(customer_stats[customer_stats['Total_Spent'] > 10000])
        medium_value = len(customer_stats[(customer_stats['Total_Spent'] >= 5000)&
                                          (customer_stats['Total_Spent'] <= 10000)])
        low_value = len(customer_stats[customer_stats['Total_Spent'] < 5000])

        print(f"High Value (>₹10K):      {high_value} customers")
        print(f"Medium Value (₹5K-10K):  {medium_value} customers")
        print(f"Low Value (<₹5K):        {low_value} customers")

    def time_series_analysis(self):
        """Analyze trends over time"""
        print("\n" + "="*70)
        print("📈 TIME SERIES ANALYSIS")
        print("="*70)

        #Daily sales
        daily_sales = self.merged_data.groupby('Transaction_Date')['Total'].sum().sort_values(ascending=False)

        print(f"\nDate Range: {daily_sales.index.min().date()} to {daily_sales.index.max().date()}")
        print(f"Average Daily Revenue: ₹{daily_sales.mean():,.0f}")
        print(f"Best Day: {daily_sales.idxmax().date()} (₹{daily_sales.max():,.0f})")

        #Weekly trends
        print("\n" + "-"*70)
        print("Average Sales by Weekday:")
        weekday_sales = self.merged_data.groupby('Weekday')['Total'].mean()
        weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        weekday_sales = weekday_sales.reindex(weekday_order)
        print(weekday_sales.round(0))

        #Monthly trends
        print("\n" + "-"*70)
        print("\nMonthly Revenue:")
        monthly_sales = self.merged_data.groupby('Month')['Total'].sum()
        print(monthly_sales.round(0))

    def regional_analysis(self):
        """Analyze sales by region"""
        print("\n" + "="*70)
        print("🗺️ REGIONAL ANALYSIS")
        print("="*70)

        regional_stats = self.merged_data.groupby('state').agg({
            'Total':['sum','mean'],
            'transaction_id':'nunique',
            'customer_id':'nunique'
        }).round(0)

        regional_stats.columns = ['Total_Revenue', 'Avg_Order', 'Orders', 'Customers']
        regional_stats = regional_stats.sort_values('Total_Revenue', ascending=False)

        print(regional_stats)

    def create_pivot_reports(self):
        """Create pivot table reports"""
        print("\n" + "="*70)
        print("📋 PIVOT TABLE REPORTS")
        print("="*70)
        
        #Product-Region pivot
        print("\nRevenue by Product & Region:")
        pivot1 = self.merged_data.pivot_table(
            values='Total',
            index='product_name',
            columns='state',
            aggfunc='sum',
            fill_value=0
        ).round(0)
        print(pivot1)

        # Category-Month pivot
        print("\n" + "-"*70)
        print("\nRevenue by Category & Month:")
        pivot2 = self.merged_data.pivot_table(
            values='Total',
            index='product_category',
            columns='Month',
            aggfunc='sum',
            fill_value=0
        ).round(0)
        print(pivot2)

    def save_reports(self):
        """Save analysis to CSV files"""
        try:
            #save merged data
            self.merged_data.to_csv('Retail_full_data.csv', index=False)

            #save summary reports
            #product summary 
            product_summary = self.merged_data.groupby('product_name').agg({
                'Total':'sum',
                'quantity':'nunique'
            }).sort_values('Total', ascending=False)
            product_summary.to_csv('retail_product_summary.csv')

            #customer summary
            customer_summary = self.merged_data.groupby('customer_id').agg({
                'Total':'sum',
                'transaction_id':'nunique'
            }).sort_values('Total', ascending=False)
            customer_summary.to_csv('Retail_customer_summary.csv')

            print("\n✓ Reports saved:")
            print("  - Retail_full_data.csv")
            print("  - Retail_product_summary.csv")
            print("  - Retail_customer_summary.csv")

        except Exception as e:
            print(f"✗ Error saving reports: {e}")


# Main Program
def main():
    print("="*70)
    print("RETAIL ANALYTICS DASHBOARD")
    print("="*70)

    analytics = RetailAnalytics()

    while True:
        print("\n" + "="*70)
        print("ANALYTICS MENU")
        print("="*70)
        print("1. Load First CSV File")
        print("2. Load Second CSV File")
        print("3. Merge All Data")
        print("4. Sales Overview")
        print("5. Product Analysis")
        print("6. Customer Analysis")
        print("7. Time Series Analysis")
        print("8. Regional Analysis")
        print("9. Pivot Table Reports")
        print("10. Run All Reports")
        print("11. Save Reports to CSV")
        print("12. Exit")

        choice = input("\nChoose (1-12): ")
        if choice == "1":
            filename = input("Enter First filename: ").strip()
            if not analytics.load_from_first_csv(filename):
                continue
        elif choice == "2":
            filename = input("Enter Second Filename: ").strip()
            if not analytics.load_from_second_csv(filename):
                continue
        elif choice == "3":
            analytics.merge_all_data()
        elif choice == "4":
            analytics.sales_overview()
        elif choice == "5":
            analytics.product_analysis()
        elif choice == "6":
            analytics.customer_analysis()
        elif choice == "7":
            analytics.time_series_analysis()
        elif choice == "8":
            analytics.regional_analysis()
        elif choice == "9":
            analytics.create_pivot_reports()
        elif choice == "10":
            analytics.sales_overview()
            analytics.product_analysis()
            analytics.customer_analysis()
            analytics.time_series_analysis()
            analytics.regional_analysis()
            analytics.create_pivot_reports()
            print("\n✓ All reports complete!")
        elif choice =="11":
            analytics.save_reports()
        elif choice == "12":
            print("\n👋 Goodbye!")
            break
        else:
            print("✗ Invalid choice!")

if __name__ == "__main__":
    main()