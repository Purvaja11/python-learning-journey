"""
DAY 17: E-COMMERCE ANALYTICS PLATFORM
Complete end-to-end analytics application

This is a PORTFOLIO PROJECT - production-ready, professional code!

Features:
- Data ingestion from multiple sources
- Automated data cleaning and validation
- Advanced SQL analytics
- Customer segmentation (RFM Analysis)
- Cohort analysis
- Automated visulaization generation
- Professional Excel reports
- CSV exports for further analysis
"""

import pandas as pd
import numpy as np
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import random
import os
from pathlib import Path

# Set style for professional visualizations
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

class EcommerceAnalyticsPlatform:
    """
    Complete analytics platform for e-commerce business

    This class demonstrates production-ready analytics code:
    - Clean architecture
    - Error handling
    - Logging
    - Modular design
    - Professional documentation
    """

    def __init__(self, db_name='ecommerce_analytics.db'):
        """ Inititalize the analytics platform"""
        self.db_name = db_name
        self.conn = None
        self.reports_dir = Path('analytics_reports')
        self.charts_dir = Path('analytics_charts')
        self.data_dir = Path('exported_data')

        # Create directories
        self.reports_dir.mkdir(exist_ok=True)
        self.charts_dir.mkdir(exist_ok=True)
        self.data_dir.mkdir(exist_ok=True)

        print("="*80)
        print(" E-COMMERCE ANALYTICS PLATFORM")
        print("="*80)
        print(f"\nInititalized:")
        print(f"     📁 Reports: {self.reports_dir}/")
        print(f"     📊 Charts: {self.charts_dir}/")
        print(f"     💾 Data: {self.data_dir}/")
        print()

    
    def connect_database(self):
        """Connect to database"""
        self.conn = sqlite3.connect(self.db_name)
        print(f"✅ Connected to database: {self.db_name}")

    def close_database(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            print("\n✅ Database connection closed")

    # =========================================================================
    # PART 1: DATA GENERATION (Simulating real data sources)
    # =========================================================================

    def generate_sample_data(self, n_customers=200, n_products=50, n_orders=100):
        """
        Generate realistic sample data for the platform
        In production, this would be replaced with actual data ingestion
        """
        print("\n" + "="*80)
        print("📥 PART 1: DATA GENERATION")
        print("="*80)

        np.random.seed(42)
        random.seed(42)

        # Generate customers
        print("\n1️⃣ Generating customers...")
        cities = ['Mumbai', 'Delhi', 'Banglore', 'Chennai', 'Pune',
                  'Hyderabad', 'Kolkata', 'Ahmedabad']
        customer_types = ['Regular', 'Premium', 'VIP']

        customers = []
        for i in range(1, n_customers + 1):
            customers.append({
                'customer_id': i,
                'name': f'Customer_{i}',
                'email': f'customer{i}@email.com',
                'city': random.choice(cities),
                'customer_type': random.choices(
                    customer_types,
                    weights=[0.7, 0.2, 0.1]
                )[0],
                'join_date': (datetime.now() - timedelta(days=random.randint(30, 730))).date()
            })
        
        self.customers_df = pd.DataFrame(customers)
        print(f"    ✅ Generated {len(self.customers_df)} customers")

        # Generate products
        print("\n2️⃣ Generating products...")
        categories = ['Electronics', 'Clothing', 'Home & kitchen',
                      'Books', 'Sports', 'Beauty', 'Toys']
        
        products = []
        for i in range(1, n_products + 1):
            category = random.choice(categories)
            base_price = random.uniform(100, 5000)

            products.append({
                'product_id': i,
                'product_name': f'Product_{category}_{i}',
                'category': category,
                'price': round(base_price, 2),
                'cost': round(base_price *0.6, 2),   # 40% margin
                'stock_quantity': random.randint(10, 500)
            })

        self.products_df = pd.DataFrame(products)
        print(f"    ✅ Generated {len(self.products_df)} products")

        # Generate orders
        print("\n3️⃣ Generating orders...")
        statuses = ['Completed', 'Pending', 'Cancelled', 'Returned']

        orders = []
        for i in range(1, n_orders + 1):
            customer_id = random.randint(1, n_customers)
            product_id = random.randint(1, n_products)

            # Get product price
            product_price = self.products_df[
                self.products_df['product_id'] == product_id
            ]['price'].values[0]

            quantity = random.randint(1, 5)
            discount = random.choice([0, 5, 10, 15, 20]) / 100

            subtotal = product_price * quantity
            discount_amount = subtotal * discount
            total_amount = subtotal - discount_amount

            # Recent orders more likely
            days_ago = int(np.random.exponential(30))
            days_ago = min(days_ago, 365)

            orders.append({
                'order_id': i,
                'customer_id': customer_id,
                'product_id': product_id,
                'quantity': quantity,
                'order_date': (datetime.now() - timedelta(days=days_ago)).date(),
                'subtotal' : round(subtotal, 2),
                'discount_percent': discount * 100,
                'discount_amount': round(discount_amount, 2),
                'total_amount': round(total_amount, 2),
                'status': random.choices(
                    statuses,
                    weights=[0.75, 0.15, 0.07, 0.03]
                )[0]
            })

        self.orders_df = pd.DataFrame(orders)
        print(f"    ✅ Generated {len(self.orders_df)} orders")

        return self.customers_df, self.products_df, self.orders_df
    
    # =========================================================================
    # PART 2: DATA CLEANING & VALIDATION
    # =========================================================================

    def clean_and_validate_data(self):
        """
        Clean and validate data before loading to database
        Production-ready data quality checks
        """
        print("\n" + "="*80)
        print("🧹 PART 2: DATA CLEANING & VALIDATION")
        print("="*80)

        issues_found = []

        # Validate customers
        print("\n1️⃣ Validating customers..")

        # Check for duplicates
        duplicates = self.customers_df['email'].duplicated().sum()
        if duplicates > 0:
            issues_found.append(f"Found {duplicates} duplicate emails")
            self.customers_df = self.customers_df.drop_duplicates(subset=['email'])

        # Check for missing values
        missing = self.customers_df.isnull().sum().sum()
        if missing > 0:
            issues_found.append(f"Found {missing} missing values in customers")
            self.customers_df = self.customers_df.dropna()

        print(f"    ✅ Validated {len(self.customers_df)} customers")

        # Validate products
        print("\n2️⃣ Validating products...")

        # Check for negative prices
        negative_prices = (self.products_df['price'] < 0).sum()
        if negative_prices > 0:
            issues_found.append(f"Found {negative_prices} negative prices")
            self.products_df = self.products_df[self.products_df['price'] >= 0]

        # Check price > cost
        invalid_margin = (self.products_df['price'] < self.products_df['cost']).sum()
        if invalid_margin > 0:
            issues_found.append(f"Found {invalid_margin} products with price < cost")
            # Fix by setting cost to 60% of price
            mask = self.products_df['price'] < self.products_df['cost']
            self.products_df.loc[mask, 'cost'] = self.products_df.loc[mask, 'price'] * 0.6

        print(f"    ✅ Validated {len(self.products_df)} products")

        # Validate orders
        print("\n3️⃣ Validating orders...")

        # Check for invalid customer IDs
        valid_customers = self.customers_df['customer_id'].values
        invalid_customers = ~self.orders_df['customer_id'].isin(valid_customers)
        if invalid_customers.sum() > 0:
            issues_found.append(f"Found {invalid_customers.sum()} orders with invalid customer IDs")
            self.orders_df = self.orders_df[~invalid_customers]

        # Check for invalid product IDs
        valid_products = self.products_df['product_id'].values
        invalid_products = ~self.orders_df['product_id'].isin(valid_products)
        if invalid_products.sum() > 0:
            issues_found.append(f"Found {invalid_products.sum()} orders with invalid product IDs")
            self.orders_df = self.orders_df[~invalid_products]

        # Check for negative quantites 
        negative_qty = (self.orders_df['quantity'] <= 0).sum()
        if negative_qty > 0:
            issues_found.append(f"Found {negative_qty} orders with invalid quantity")
            self.orders_df = self.orders_df[self.orders_df['quantity'] > 0]

        print(f"    ✅ Validated {len(self.orders_df)} orders")

        # Summary
        if issues_found:
            print("\n⚠️ Issues found and fixed:")
            for issue in issues_found:
                print(f"    - {issue}")

        else:
            print("\n✅ No data quality issues found!")

        return len(issues_found)
    
    # =========================================================================
    # PART 3: DATABASE SETUP
    # =========================================================================

    def create_database_schema(self):
        """
        Create normalized databse schema
        Following database design practices
        """
        print("\n" + "="*80)
        print("🗄️  PART 3: DATABASE SCHEMA CREATION")
        print("="*80)

        cursor = self.conn.cursor()

        # Drop existing tables
        cursor.execute("DROP TABLE IF EXISTS orders")
        cursor.execute("DROP TABLE IF EXISTS products")
        cursor.execute("DROP TABLE IF EXISTS customers")

        # Create customers table
        print("\n1️⃣ Creating customers table...")
        cursor.execute('''
            CREATE TABLE customers (
                       customer_id INTEGER PRIMARY KEY,
                       name TEXT NOT NULL,
                       email TEXT UNIQUE NOT NULL,
                       city TEXT,
                       customer_type TEXT CHECK(customer_type IN ('Regular', 'Premium', 'VIP')),
                       join_date DATE NOT NULL
                       )
                ''')
        
        # Create products table
        print("2️⃣ Creating products table...")
        cursor.execute('''
            CREATE TABLE products (
                       product_id INTEGER PRIMARY KEY,
                       product_name TEXT NOT NULL,
                       category TEXT NOT NULL,
                       price DECIMAL(10, 2) NOT NULL CHECK(price >= 0),
                       cost DECIMAL(10, 2) NOT NULL CHECK(cost >= 0),
                       stock_quantity INTEGER NOT NULL CHECK(stock_quantity >=0)
                       )
                ''')
        
        # Create orders table
        print("3️⃣ Creating orders table...")
        cursor.execute('''
            CREATE TABLE orders(
                       order_id INTEGER PRIMARY KEY,
                       customer_id INTEGER NOT NULL,
                       product_id INTEGER NOT NULL,
                       quantity INTEGER NOT NULL CHECK(quantity > 0),
                       order_date DATE NOT NULL,
                       subtotal DECIMAL(10, 2) NOT NULL,
                       discount_percent DECIMAL(5, 2) DEFAULT 0,
                       discount_amount DECIMAL(10, 2) DEFAULT 0,
                       total_amount DECIMAL(10, 2) NOT NULL,
                       status TEXT CHECK(status IN ('Completed', 'Pending', 'Cancelled', 'Returned')),
                       FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
                       FOREIGN KEY (product_id) REFERENCES products(product_id)
                       )
                ''')
        
        # Create indexes for performance
        print("4️⃣ Creating indexes...")
        cursor.execute('CREATE INDEX idx_orders_customer ON orders(customer_id)')
        cursor.execute('CREATE INDEX idx_orders_product ON orders(product_id)')
        cursor.execute('CREATE INDEX idx_orders_date ON orders(order_date)')
        cursor.execute('CREATE INDEX idx_orders_status ON orders(status)')

        self.conn.commit()
        print("\n✅ Database schema created with indexes")

    def load_data_to_database(self):
        """ Load cleaned data into database:"""
        print("\n" + "="*80)
        print("📤 PART 4: LOADING DATA TO DATABASE")
        print("="*80)

        print("\n1️⃣ Loading customers:...")
        self.customers_df.to_sql('customers', self.conn, if_exists='append', index=False)
        print(f"   ✅ Loaded {len(self.customers_df)} customers")

        print(f"\n2️⃣ Loading products...")
        self.products_df.to_sql('products', self.conn, if_exists='append', index=False)
        print(f"   ✅ Loaded {len(self.products_df)} products")

        print("\n3️⃣ Loading orders...")
        self.orders_df.to_sql('orders', self.conn, if_exists='append', index=False)
        print(f"   ✅ Loaded {len(self.orders_df)} orders")

        # Verify
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM customers")
        customer_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM products")
        product_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM orders")
        order_count = cursor.fetchone()[0]

        print(f"\n✅ Database populated successfully!")
        print(f"    📊 {customer_count} customers")
        print(f"    📦 {product_count} products")
        print(f"    🛒 {order_count} orders")

    # =========================================================================
    # PART 5: ADVANCED ANALYTICS
    # =========================================================================

    def perform_rfm_analysis(self):
        """
        RFM Analysis (Recency, Frequency, Monetary)
        Professional customer segmentation technique
        """
        print("\n" + "="*80)
        print("🎯 PART 5: RFM CUSTOMER SEGMENTATION")
        print("="*80)

        query = '''
        WITH customer_metrics AS (
            SELECT
                c.customer_id,
                c.name,
                c.city,
                c.customer_type,
                MAX(o.order_date) as last_order_date,
                julianday('now') - julianday(MAX(o.order_date)) as recency_days,
                COUNT(o.order_id) as frequency,
                SUM(o.total_amount) as monetary
            FROM customers c
            LEFT JOIN orders o ON c.customer_id = o.customer_id
            WHERE o.status = 'Completed'
            GROUP BY c.customer_id, c.name, c.city, c.customer_type
        )
        SELECT
            customer_id,
            name,
            city,
            customer_type,
            CAST(recency_days AS INTEGER) as recency_days,
            frequency,
            ROUND(monetary, 2) as monetary,
            CASE
                WHEN recency_days <= 30 AND frequency >= 5 AND monetary >= 5000 THEN 'Champions'
                WHEN recency_days <= 60 AND frequency >= 3 AND monetary >= 3000 THEN 'Loyal'
                WHEN recency_days <= 90 AND frequency >= 2 And monetary >= 1000 THEN 'Potential'
                WHEN recency_days > 90 AND monetary >= 2000 THEN 'At Risk'
                WHEN recency_days > 180 THEN 'Lost'
                ELSE 'New/Low Value'
            END as rfm_segment
        FROM customer_metrics
        ORDER BY monetary DESC;
        '''

        rfm_df = pd.read_sql_query(query, self.conn)

        # Display segment distribution
        print("\n📊 RFM Segment Distribution:")
        segment_counts = rfm_df['rfm_segment'].value_counts()
        for segment, count in segment_counts.items():
            pct = (count / len(rfm_df)) * 100
            print(f"     {segment:20s}: {count:3d} customers ({pct:5.1f}%)")

        # Save to CSV
        output_file = self.data_dir / 'rfm_analysis.csv'
        rfm_df.to_csv(output_file, index=False)
        print(f"\n✅ RFM analysis saved to: {output_file}")

        return rfm_df
    
    def analyze_cohorts(self):
        """
        Cohort analysis - track customer behaviour by acquistion month
        """
        print("\n" + "="*80)
        print("👥 COHORT ANALYSIS")
        print("="*80)

        query = '''
        WITH customer_cohorts AS (
            SELECT 
                customer_id,
                strftime('%Y-%m', MIN(order_date)) as cohort_month
            FROM  orders
            WHERE status = 'Completed'
            GROUP BY customer_id
        )
        SELECT
            cc.cohort_month,
            COUNT(DISTINCT cc.customer_id) as customers,
            COUNT(o.order_id) as orders,
            ROUND(SUM(o.total_amount), 2) as revenue,
            ROUND(AVG(o.total_amount), 2) as avg_order_value,
            ROUND(SUM(o.total_amount) / COUNT(DISTINCT cc.customer_id), 2) as revenue_per_customer
        FROM customer_cohorts cc
        JOIN orders o ON cc.customer_id = o.customer_id
        WHERE o.status = 'Completed'
        GROUP BY cc.cohort_month
        ORDER BY cohort_month;
        '''

        cohort_df = pd.read_sql_query(query, self.conn)

        print("\n📊 Cohort Performance:")
        print(cohort_df.to_string(index=False))

        # Save
        output_file = self.data_dir / 'cohort_analysis.csv'
        cohort_df.to_csv(output_file, index=False)
        print(f"\n✅ Cohort analysis saved to: {output_file}")

        return cohort_df
    
    def analyze_product_performance(self):
        """Product performance with profitablity analysis"""
        print("\n" + "="*80)
        print("📦 PRODUCT PERFORMANCE ANALYSIS")
        print("="*80)

        query = '''
        SELECT
            p.product_id,
            p.product_name,
            p.category,
            p.price,
            p.cost,
            ROUND((p.price - p.cost) / p.price * 100, 2) as margin_percent,
            COUNT(o.order_id) as times_ordered,
            SUM(o.quantity) as units_sold,
            ROUND(SUM(o.subtotal), 2) as gross_revenue,
            ROUND(SUM(o.discount_amount), 2) as total_discounts,
            ROUND(SUM(o.total_amount), 2) as net_revenue,
            ROUND(SUM((p.price - p.cost) * o.quantity), 2) as profit,
            ROUND(AVG(o.total_amount), 2) as avg_order_value
        FROM products p 
        LEFT JOIN orders o ON p.product_id = o.product_id AND o.status = 'Completed'
        GROUP BY p.product_id, p.product_name, p.category, p.price, p.cost
        HAVING units_sold > 0
        ORDER BY profit DESC
        LIMIT 20;
        '''

        product_df = pd.read_sql_query(query, self.conn)

        print("\n🏆 Top 20 Products by Profit:")
        print(product_df[['product_name', 'category', 'units_sold', 'net_revenue', 'profit',]].to_string(index=False))

        # Save
        output_file =self.data_dir / 'product_performance.csv'
        product_df.to_csv(output_file, index=False)
        print(f"\n✅ Product analysis saved to: {output_file}")

        return product_df
    
    def generate_executive_summary(self):
        """Generate executive KPI dashboard"""
        print("\n" + "="*80)
        print("📊 EXECUTIVE SUMMARY")
        print("="*80)

        query = '''
        SELECT
            COUNT(DISTINCT c.customer_id) as total_customers,
            COUNT(DISTINCT CASE WHEN o.order_id IS NOT NULL THEN c.customer_id END) as active_customers,
            COUNT(o.order_id) as total_orders,
            SUM(CASE WHEN o.status = 'Completed' THEN 1 ELSE 0 END) as completed_orders,
            ROUND(SUM(CASE WHEN o.status = 'Completed' THEN o.subtotal ELSE 0 END), 2) as gross_revenue,
            ROUND(SUM(CASE WHEN o.status = 'Completed' THEN o.discount_amount ELSE 0 END), 2) as total_discount,
            ROUND(SUM(CASE WHEN o.status = 'Completed' THEN o.total_amount ELSE 0 END), 2) as net_revenue,
            ROUND(AVG(CASE WHEN o.status = 'Completed' THEN o. total_amount END), 2) as avg_order_value,
            ROUND(SUM(CASE WHEN o.status = 'Completed' THEN o.total_amount END) /
            COUNT(DISTINCT CASE WHEN o.status = 'Completed' THEN c.customer_id END), 2) as revenue_per_customer
        FROM customers c
        LEFT JOIN orders o ON c.customer_id = o.customer_id;
        '''

        summary = pd.read_sql_query(query, self.conn).iloc[0]

        print("\n📈 KEY PERFORMANCE INDICATORS:")
        print(f"    Total Customers:        {summary['total_customers']:,}")
        print(f"    Active Customers:       {summary['active_customers']:,}")
        print(f"    Total Orders:           {summary['total_orders']:,}")
        print(f"    Completed Orders:       {summary['completed_orders']:,}")
        print(f"    Gross Revenue:          ₹{summary['gross_revenue']:,.2f}")
        print(f"    Total Discounts:        ₹{summary['total_discount']:,.2f}")
        print(f"    Net Revenue:            ₹{summary['net_revenue']:,.2f}")
        print(f"    Avg Order Value:        ₹{summary['avg_order_value']:,.2f}")
        print(f"    Revenue per Customer:   ₹{summary['revenue_per_customer']:,.2f}")

        return summary
    

    # =========================================================================
    # PART 6: VISUALIZATIONS
    # =========================================================================

    def create_visualizations(self):
        """Generate professional analytics visualizations"""
        print("\n" + "="*80)
        print("📊 GENERATING VISUALIZATIONS")
        print("="*80)

        # 1. Revenue by Category 
        print("\n Creating revenue by category chart...")
        query = '''
        SELECT
            p.category,
            SUM(o.total_amount) as revenue
        FROM  products p
        JOIN orders o ON p.product_id = o.product_id
        WHERE o.status = 'Completed'
        GROUP BY p.category
        ORDER BY revenue DESC;
        '''
        df = pd.read_sql_query(query, self.conn)

        plt.figure(figsize=(12, 6))
        sns.barplot(data=df, x='category', y='revenue', hue='category', palette='viridis', legend=False)
        plt.title('Revenue by Product Category', fontsize=16, fontweight='bold')
        plt.xlabel('Category', fontsize=12)
        plt.ylabel('Revenue (₹)', fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(self.charts_dir / 'revenue_by_category.png', dpi=300)
        plt.close()
        print(f"   ✅ Saved: revenue_by_category.png")

        # 2. Monthly Revenue Trend
        print("\n2️⃣ Creating monthly trend chart...")
        query = '''
        SELECT
            strftime('%Y-%m', order_date) as month,
            SUM(total_amount) as revenue,
            COUNT(*) as orders
        FROM orders
        WHERE status = 'Completed'
        GROUP BY month
        ORDER BY month;
        '''
        df = pd.read_sql_query(query, self.conn)

        fig, ax1 = plt.subplots(figsize=(14, 6))

        ax1.plot(df['month'], df['revenue'], marker='o', linewidth=2, color='#2E86AB')
        ax1.set_xlabel('Month', fontsize=12)
        ax1.set_ylabel('Revenue', fontsize=12)
        ax1.tick_params(axis='y', labelcolor='#2E86AB')
        ax1.grid(True, alpha=0.3)

        ax2 = ax1.twinx()
        ax2.bar(df['month'], df['orders'], alpha=0.3, color='#A23B72', label='Orders')
        ax2.set_ylabel('Number of Orders', fontsize=12, color='#A23B72')
        ax2.tick_params(axis='y', labelcolor='#A23B72')

        plt.title('Monthly Revenue and Order Trends', fontsize=16, fontweight='bold')
        plt.xticks(rotation=45, ha='right')
        fig.tight_layout()
        plt.savefig(self.charts_dir / 'monthly_trend.png', dpi=300)
        plt.close()
        print(f"   ✅ Saved: montly_trends.png")

        print(f"\n ✅ All visualizations saved to: {self.charts_dir}/")

    # =========================================================================
    # PART 7: EXCEL REPORTING
    # =========================================================================

    def generate_excel_report(self):
        """Generate comprehensive Excel report"""
        print("\n" + "="*80)
        print("📄 GENERATING EXCEL REPORT")
        print("="*80)

        output_file = self.reports_dir / f'Analytics_Report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            # Sheet 1: Executive Summary
            print("\n1️⃣ Creating Executive Summary sheet...")
            summary_query = '''
            SELECT
                'Total Customers' as Metric,
                COUNT(DISTINCT customer_id) as Value
            FROM customers
            UNION ALL
            SELECT 'Total Revenue', ROUND(SUM(CASE WHEN status = 'Completed' THEN total_amount ELSE 0 END), 2)
            FROM orders;
            '''
            pd.read_sql_query(summary_query, self.conn).to_excel(
                writer, sheet_name='Executive Summary', index=False
            )

            # Sheet 2: Top Customers
            print("2️⃣ Creating Top Customers sheet...")
            customers_query = '''
            SELECT 
                c.name as Customer,
                c.city as City,
                COUNT(o.order_id) as Orders,
                ROUND(SUM(o.total_amount), 2) as Total_Spent
            FROM customers c
            JOIN orders o ON c.customer_id = o.customer_id
            WHERE o.status = 'Completed'
            GROUP BY c.customer_id
            ORDER BY Total_Spent DESC
            LIMIT 50;
            '''
            pd.read_sql_query(customers_query, self.conn).to_excel(
                writer, sheet_name='Top Customers', index=False
            )

        print(f"\n✅ Excel report saved: {output_file}")
        return output_file
    

def main():
    """Main Execution"""

    # Initialize platform
    platform = EcommerceAnalyticsPlatform()

    try:
        # Connect to database
        platform.connect_database()

        # Part 1: Generate data
        platform.generate_sample_data(n_customers=200, n_products=50, n_orders=1000)

        # Part 2: Clean and validate 
        platform.clean_and_validate_data()

        # Part 3: Create database
        platform.create_database_schema()

        # Part 4: Load data
        platform.load_data_to_database()

        # Part 5: Analytics
        input("\nPress Enter to perform RFM analysis...")
        platform.perform_rfm_analysis()

        input("\nPress Enter to perform cohort analysis...")
        platform.analyze_cohorts()

        input("\nPress Enter to analyze product performance...")
        platform.analyze_product_performance()

        input("\nPress Enter to view executive summary...")
        platform.generate_executive_summary()

        # Part 6: Visualizations
        input("\nPress Enter to generate visualizations...")
        platform.create_visualizations()

        # Part 7: Excel Report
        input("\nPress Enter to generate Excel report...")
        platform.generate_excel_report()

        # Success
        print("\n" + "="*80)
        print("🎉 E-COMMERCE ANALYTICS PLATFORM - COMPLETE!")
        print("="*80)
        print("\n✅ Deliverables:")
        print(f"   📊 Database: ecommerce_analytics.db")
        print(f"   📈 Charts: {platform.charts_dir}/")
        print(f"   📄 Reports: {platform.reports_dir}/")
        print(f"   💾 Data: {platform.data_dir}/")

    finally:
        # Always close database
        platform.close_database()



if __name__ == "__main__":
    main()