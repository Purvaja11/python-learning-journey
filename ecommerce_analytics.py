"""
E-commerce Analytics Dashboard - Day 10 Project
Advanced Pandas: Merging, time series, pivot tables, real analytics

This mimics real data analyst work!
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class EcommerceAnalytics:
    """Advanced e-commerce data analysis"""
    
    def __init__(self):
        self.customers = None
        self.orders = None
        self.products = None
        self.order_items = None
        self.merged_data = None
    
    def generate_sample_data(self):
        """Generate realistic e-commerce data"""
        np.random.seed(42)
        
        # Generate customers
        n_customers = 100
        self.customers = pd.DataFrame({
            'Customer_ID': range(1, n_customers + 1),
            'Name': [f'Customer_{i}' for i in range(1, n_customers + 1)],
            'Email': [f'customer{i}@email.com' for i in range(1, n_customers + 1)],
            'City': np.random.choice(['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Pune'], n_customers),
            'Join_Date': pd.date_range(start='2023-01-01', periods=n_customers, freq='3D')
        })
        
        # Generate products
        products_list = ['Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Headphones', 
                        'Webcam', 'USB Cable', 'Router', 'External Drive', 'Printer']
        self.products = pd.DataFrame({
            'Product_ID': range(1, len(products_list) + 1),
            'Product_Name': products_list,
            'Category': ['Electronics', 'Accessories', 'Accessories', 'Electronics', 'Accessories',
                        'Accessories', 'Accessories', 'Networking', 'Storage', 'Office'],
            'Unit_Price': [50000, 500, 1500, 15000, 2000, 3000, 200, 3500, 4000, 8000],
            'Stock': np.random.randint(10, 100, len(products_list))
        })
        
        # Generate orders (300 orders over 60 days)
        n_orders = 300
        start_date = datetime(2024, 1, 1)
        
        order_dates = [start_date + timedelta(days=np.random.randint(0, 60)) for _ in range(n_orders)]
        
        self.orders = pd.DataFrame({
            'Order_ID': range(1, n_orders + 1),
            'Customer_ID': np.random.randint(1, n_customers + 1, n_orders),
            'Order_Date': order_dates,
            'Status': np.random.choice(['Delivered', 'Shipped', 'Processing', 'Cancelled'], 
                                      n_orders, p=[0.7, 0.15, 0.1, 0.05])
        })
        
        self.orders['Order_Date'] = pd.to_datetime(self.orders['Order_Date'])
        
        # Generate order items (1-3 items per order)
        order_items_list = []
        for order_id in range(1, n_orders + 1):
            n_items = np.random.randint(1, 4)
            for _ in range(n_items):
                order_items_list.append({
                    'Order_Item_ID': len(order_items_list) + 1,
                    'Order_ID': order_id,
                    'Product_ID': np.random.randint(1, len(products_list) + 1),
                    'Quantity': np.random.randint(1, 5)
                })
        
        self.order_items = pd.DataFrame(order_items_list)
        
        print(f"✓ Generated sample data:")
        print(f"  Customers: {len(self.customers)}")
        print(f"  Products: {len(self.products)}")
        print(f"  Orders: {len(self.orders)}")
        print(f"  Order Items: {len(self.order_items)}")
        
        return True
    
    def merge_all_data(self):
        """Merge all tables for comprehensive analysis"""
        print("\n🔗 Merging all data...")
        
        # Step 1: Merge order_items with products
        items_products = pd.merge(
            self.order_items,
            self.products,
            on='Product_ID',
            how='left'
        )
        
        # Calculate line total
        items_products['Line_Total'] = items_products['Quantity'] * items_products['Unit_Price']
        
        # Step 2: Merge with orders
        items_orders = pd.merge(
            items_products,
            self.orders,
            on='Order_ID',
            how='left'
        )
        
        # Step 3: Merge with customers
        self.merged_data = pd.merge(
            items_orders,
            self.customers,
            on='Customer_ID',
            how='left'
        )
        
        # Add time-based columns
        self.merged_data['Month'] = self.merged_data['Order_Date'].dt.month_name()
        self.merged_data['Week'] = self.merged_data['Order_Date'].dt.isocalendar().week
        self.merged_data['Weekday'] = self.merged_data['Order_Date'].dt.day_name()
        
        print(f"✓ Merged data shape: {self.merged_data.shape}")
        return True
    
    def sales_overview(self):
        """Overall sales statistics"""
        print("\n" + "="*70)
        print("📊 SALES OVERVIEW")
        print("="*70)
        
        # Filter delivered orders only
        delivered = self.merged_data[self.merged_data['Status'] == 'Delivered']
        
        total_revenue = delivered['Line_Total'].sum()
        total_orders = delivered['Order_ID'].nunique()
        total_customers = delivered['Customer_ID'].nunique()
        avg_order_value = total_revenue / total_orders
        
        print(f"\nTotal Revenue:        ₹{total_revenue:,.0f}")
        print(f"Total Orders:         {total_orders:,}")
        print(f"Unique Customers:     {total_customers:,}")
        print(f"Average Order Value:  ₹{avg_order_value:,.0f}")
        print(f"Repeat Customer Rate: {(total_orders - total_customers) / total_orders * 100:.1f}%")
    
    def product_analysis(self):
        """Analyze product performance"""
        print("\n" + "="*70)
        print("🏆 PRODUCT PERFORMANCE")
        print("="*70)
        
        delivered = self.merged_data[self.merged_data['Status'] == 'Delivered']
        
        product_stats = delivered.groupby('Product_Name').agg({
            'Line_Total': 'sum',
            'Quantity': 'sum',
            'Order_ID': 'nunique'
        }).round(0)
        
        product_stats.columns = ['Revenue', 'Units_Sold', 'Orders']
        product_stats = product_stats.sort_values('Revenue', ascending=False)
        
        print("\nTop 5 Products by Revenue:")
        print(product_stats.head())
        
        # Category analysis
        print("\n" + "-"*70)
        category_stats = delivered.groupby('Category')['Line_Total'].sum().sort_values(ascending=False)
        print("\nRevenue by Category:")
        print(category_stats)
    
    def customer_analysis(self):
        """Analyze customer behavior"""
        print("\n" + "="*70)
        print("👥 CUSTOMER ANALYSIS")
        print("="*70)
        
        delivered = self.merged_data[self.merged_data['Status'] == 'Delivered']
        
        customer_stats = delivered.groupby('Customer_ID').agg({
            'Line_Total': 'sum',
            'Order_ID': 'nunique'
        })
        
        customer_stats.columns = ['Total_Spent', 'Order_Count']
        customer_stats = customer_stats.sort_values('Total_Spent', ascending=False)
        
        print("\nTop 10 Customers:")
        top_10 = customer_stats.head(10)
        print(top_10)
        
        # Customer segmentation
        print("\n" + "-"*70)
        print("Customer Segmentation:")
        
        high_value = len(customer_stats[customer_stats['Total_Spent'] > 100000])
        medium_value = len(customer_stats[(customer_stats['Total_Spent'] >= 50000) & 
                                         (customer_stats['Total_Spent'] <= 100000)])
        low_value = len(customer_stats[customer_stats['Total_Spent'] < 50000])
        
        print(f"High Value (>₹1L):     {high_value} customers")
        print(f"Medium Value (₹50K-1L): {medium_value} customers")
        print(f"Low Value (<₹50K):      {low_value} customers")
    
    def time_series_analysis(self):
        """Analyze trends over time"""
        print("\n" + "="*70)
        print("📈 TIME SERIES ANALYSIS")
        print("="*70)
        
        delivered = self.merged_data[self.merged_data['Status'] == 'Delivered']
        
        # Daily sales
        daily_sales = delivered.groupby('Order_Date')['Line_Total'].sum().sort_index()
        
        print(f"\nDate Range: {daily_sales.index.min().date()} to {daily_sales.index.max().date()}")
        print(f"Average Daily Revenue: ₹{daily_sales.mean():,.0f}")
        print(f"Best Day: {daily_sales.idxmax().date()} (₹{daily_sales.max():,.0f})")
        
        # Weekly trends
        print("\n" + "-"*70)
        print("Average Sales by Weekday:")
        weekday_sales = delivered.groupby('Weekday')['Line_Total'].mean()
        weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        weekday_sales = weekday_sales.reindex(weekday_order)
        print(weekday_sales.round(0))
        
        # Monthly trends
        print("\n" + "-"*70)
        monthly_sales = delivered.groupby('Month')['Line_Total'].sum()
        print("\nMonthly Revenue:")
        print(monthly_sales.round(0))
    
    def regional_analysis(self):
        """Analyze sales by region"""
        print("\n" + "="*70)
        print("🗺️ REGIONAL ANALYSIS")
        print("="*70)
        
        delivered = self.merged_data[self.merged_data['Status'] == 'Delivered']
        
        regional_stats = delivered.groupby('City').agg({
            'Line_Total': ['sum', 'mean'],
            'Order_ID': 'nunique',
            'Customer_ID': 'nunique'
        }).round(0)
        
        regional_stats.columns = ['Total_Revenue', 'Avg_Order', 'Orders', 'Customers']
        regional_stats = regional_stats.sort_values('Total_Revenue', ascending=False)
        
        print(regional_stats)
    
    def create_pivot_reports(self):
        """Create pivot table reports"""
        print("\n" + "="*70)
        print("📋 PIVOT TABLE REPORTS")
        print("="*70)
        
        delivered = self.merged_data[self.merged_data['Status'] == 'Delivered']
        
        # Product-Region pivot
        print("\nRevenue by Product & Region:")
        pivot1 = delivered.pivot_table(
            values='Line_Total',
            index='Product_Name',
            columns='City',
            aggfunc='sum',
            fill_value=0
        ).round(0)
        print(pivot1)
        
        # Category-Month pivot
        print("\n" + "-"*70)
        print("\nRevenue by Category & Month:")
        pivot2 = delivered.pivot_table(
            values='Line_Total',
            index='Category',
            columns='Month',
            aggfunc='sum',
            fill_value=0
        ).round(0)
        print(pivot2)
    
    def order_status_analysis(self):
        """Analyze order statuses"""
        print("\n" + "="*70)
        print("📦 ORDER STATUS ANALYSIS")
        print("="*70)
        
        status_counts = self.orders['Status'].value_counts()
        status_percentages = (status_counts / len(self.orders) * 100).round(1)
        
        print("\nOrder Status Distribution:")
        for status, count in status_counts.items():
            pct = status_percentages[status]
            print(f"  {status:12s}: {count:4d} orders ({pct:5.1f}%)")
        
        # Cancelled order analysis
        cancelled_items = self.merged_data[self.merged_data['Status'] == 'Cancelled']
        if len(cancelled_items) > 0:
            lost_revenue = cancelled_items['Line_Total'].sum()
            print(f"\nPotential Lost Revenue (Cancelled): ₹{lost_revenue:,.0f}")
    
    def save_reports(self):
        """Save analysis to CSV files"""
        try:
            # Save merged data
            self.merged_data.to_csv('ecommerce_full_data.csv', index=False)
            
            # Save summary reports
            delivered = self.merged_data[self.merged_data['Status'] == 'Delivered']
            
            # Product summary
            product_summary = delivered.groupby('Product_Name').agg({
                'Line_Total': 'sum',
                'Quantity': 'sum'
            }).sort_values('Line_Total', ascending=False)
            product_summary.to_csv('ecommerce_product_summary.csv')
            
            # Customer summary
            customer_summary = delivered.groupby('Customer_ID').agg({
                'Line_Total': 'sum',
                'Order_ID': 'nunique'
            }).sort_values('Line_Total', ascending=False)
            customer_summary.to_csv('ecommerce_customer_summary.csv')
            
            print("\n✓ Reports saved:")
            print("  - ecommerce_full_data.csv")
            print("  - product_summary.csv")
            print("  - customer_summary.csv")
            
        except Exception as e:
            print(f"✗ Error saving reports: {e}")

# Main program
def main():
    print("="*70)
    print("E-COMMERCE ANALYTICS DASHBOARD")
    print("="*70)
    
    analytics = EcommerceAnalytics()
    
    print("\n1. Generating sample data...")
    analytics.generate_sample_data()
    
    print("\n2. Merging all datasets...")
    analytics.merge_all_data()
    
    while True:
        print("\n" + "="*70)
        print("ANALYTICS MENU")
        print("="*70)
        print("1.  Sales Overview")
        print("2.  Product Analysis")
        print("3.  Customer Analysis")
        print("4.  Time Series Analysis")
        print("5.  Regional Analysis")
        print("6.  Pivot Table Reports")
        print("7.  Order Status Analysis")
        print("8.  Run All Reports")
        print("9.  Save Reports to CSV")
        print("10. Exit")
        
        choice = input("\nChoose (1-10): ")
        
        if choice == "1":
            analytics.sales_overview()
        elif choice == "2":
            analytics.product_analysis()
        elif choice == "3":
            analytics.customer_analysis()
        elif choice == "4":
            analytics.time_series_analysis()
        elif choice == "5":
            analytics.regional_analysis()
        elif choice == "6":
            analytics.create_pivot_reports()
        elif choice == "7":
            analytics.order_status_analysis()
        elif choice == "8":
            print("\n🚀 Running all reports...\n")
            analytics.sales_overview()
            analytics.product_analysis()
            analytics.customer_analysis()
            analytics.time_series_analysis()
            analytics.regional_analysis()
            analytics.create_pivot_reports()
            analytics.order_status_analysis()
            print("\n✓ All reports complete!")
        elif choice == "9":
            analytics.save_reports()
        elif choice == "10":
            print("\n👋 Goodbye!")
            break
        else:
            print("✗ Invalid choice!")

if __name__ == "__main__":
    main()