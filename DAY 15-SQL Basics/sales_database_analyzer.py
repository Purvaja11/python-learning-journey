"""
DAY 15: SQL BASICS FOR DATA ANALYSTS
Sales Database Analysis System

This project demonstrates:
1. Creating and populating SQLite databases
2. Essential SQL queries for data analysis
3. Combining SQL with Pandas for advanced analytics
4. Generating business reports

Real-world skills NetWeb will test!
"""

import sqlite3
import pandas as pd
import random
from datetime import datetime, timedelta

class SalesDatabaseAnalyzer:
    """Complete SQL + Python analytics system"""
    
    def __init__(self, db_name='sales_analysis.db'):
        """Initialize database connection"""
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        print(f"✅ Connected to database: {db_name}")
    
    def create_tables(self):
        """Create database schema (like a real company database)"""
        
        # Customers table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                customer_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT UNIQUE,
                city TEXT,
                join_date DATE,
                customer_type TEXT
            )
        ''')
        
        # Products table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                product_id INTEGER PRIMARY KEY,
                product_name TEXT NOT NULL,
                category TEXT,
                price DECIMAL(10, 2),
                stock_quantity INTEGER
            )
        ''')
        
        # Orders table (links customers to products)
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                order_id INTEGER PRIMARY KEY,
                customer_id INTEGER,
                product_id INTEGER,
                quantity INTEGER,
                order_date DATE,
                total_amount DECIMAL(10, 2),
                status TEXT,
                FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
                FOREIGN KEY (product_id) REFERENCES products(product_id)
            )
        ''')
        
        self.conn.commit()
        print("✅ Database tables created successfully!")
    
    def populate_sample_data(self):
        """Generate realistic sample data (like a real company)"""
        
        # Sample data
        cities = ['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Pune', 'Hyderabad']
        customer_types = ['Regular', 'Premium', 'VIP']
        categories = ['Electronics', 'Clothing', 'Home & Kitchen', 'Books', 'Sports']
        statuses = ['Completed', 'Pending', 'Cancelled']
        
        # Insert customers
        customers = []
        for i in range(1, 51):  # 50 customers
            customers.append((
                i,
                f'Customer_{i}',
                f'customer{i}@email.com',
                random.choice(cities),
                (datetime.now() - timedelta(days=random.randint(30, 365))).date(),
                random.choice(customer_types)
            ))
        
        self.cursor.executemany('''
            INSERT OR IGNORE INTO customers 
            VALUES (?, ?, ?, ?, ?, ?)
        ''', customers)
        
        # Insert products
        products = []
        product_names = [
            'Laptop', 'Smartphone', 'Headphones', 'T-Shirt', 'Jeans',
            'Blender', 'Microwave', 'Novel', 'Textbook', 'Football',
            'Yoga Mat', 'Watch', 'Sunglasses', 'Backpack', 'Shoes'
        ]
        
        for i in range(1, 16):  # 15 products
            products.append((
                i,
                product_names[i-1],
                random.choice(categories),
                round(random.uniform(100, 5000), 2),
                random.randint(10, 100)
            ))
        
        self.cursor.executemany('''
            INSERT OR IGNORE INTO products 
            VALUES (?, ?, ?, ?, ?)
        ''', products)
        
        # Insert orders (100 orders)
        orders = []
        for i in range(1, 101):
            customer_id = random.randint(1, 50)
            product_id = random.randint(1, 15)
            quantity = random.randint(1, 5)
            
            # Get product price
            self.cursor.execute('SELECT price FROM products WHERE product_id = ?', (product_id,))
            price = self.cursor.fetchone()[0]
            
            orders.append((
                i,
                customer_id,
                product_id,
                quantity,
                (datetime.now() - timedelta(days=random.randint(1, 90))).date(),
                round(price * quantity, 2),
                random.choice(statuses)
            ))
        
        self.cursor.executemany('''
            INSERT OR IGNORE INTO orders 
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', orders)
        
        self.conn.commit()
        print("✅ Sample data inserted successfully!")
        print(f"   📊 50 customers, 15 products, 100 orders")
    
    def run_sql_query(self, query, description):
        """Execute SQL query and display results"""
        print(f"\n{'='*80}")
        print(f"📊 QUERY: {description}")
        print(f"{'='*80}")
        print(f"\nSQL:\n{query}\n")
        
        df = pd.read_sql_query(query, self.conn)
        print(df.to_string(index=False))
        print(f"\n📈 Results: {len(df)} rows returned")
        return df
    
    def query_1_basic_select(self):
        """Query 1: Basic SELECT - View all customers"""
        query = '''
        SELECT customer_id, name, city, customer_type
        FROM customers
        LIMIT 10;
        '''
        return self.run_sql_query(query, "View first 10 customers")
    
    def query_2_where_filter(self):
        """Query 2: WHERE clause - Filter by condition"""
        query = '''
        SELECT name, email, city
        FROM customers
        WHERE city = 'Mumbai' AND customer_type = 'Premium';
        '''
        return self.run_sql_query(query, "Premium customers from Mumbai")
    
    def query_3_aggregation(self):
        """Query 3: Aggregation - Calculate statistics"""
        query = '''
        SELECT 
            COUNT(*) as total_orders,
            SUM(total_amount) as total_revenue,
            AVG(total_amount) as avg_order_value,
            MAX(total_amount) as highest_order,
            MIN(total_amount) as lowest_order
        FROM orders
        WHERE status = 'Completed';
        '''
        return self.run_sql_query(query, "Overall sales statistics (completed orders)")
    
    def query_4_group_by(self):
        """Query 4: GROUP BY - Sales by city"""
        query = '''
        SELECT 
            c.city,
            COUNT(o.order_id) as total_orders,
            SUM(o.total_amount) as total_revenue,
            AVG(o.total_amount) as avg_order_value
        FROM customers c
        JOIN orders o ON c.customer_id = o.customer_id
        WHERE o.status = 'Completed'
        GROUP BY c.city
        ORDER BY total_revenue DESC;
        '''
        return self.run_sql_query(query, "Sales performance by city")
    
    def query_5_having_clause(self):
        """Query 5: HAVING - Filter grouped results"""
        query = '''
        SELECT 
            c.customer_id,
            c.name,
            COUNT(o.order_id) as order_count,
            SUM(o.total_amount) as total_spent
        FROM customers c
        JOIN orders o ON c.customer_id = o.customer_id
        WHERE o.status = 'Completed'
        GROUP BY c.customer_id, c.name
        HAVING SUM(o.total_amount) > 5000
        ORDER BY total_spent DESC;
        '''
        return self.run_sql_query(query, "High-value customers (spent > ₹5000)")
    
    def query_6_inner_join(self):
        """Query 6: INNER JOIN - Orders with customer & product details"""
        query = '''
        SELECT 
            o.order_id,
            c.name as customer_name,
            p.product_name,
            o.quantity,
            o.total_amount,
            o.order_date,
            o.status
        FROM orders o
        INNER JOIN customers c ON o.customer_id = c.customer_id
        INNER JOIN products p ON o.product_id = p.product_id
        ORDER BY o.order_date DESC
        LIMIT 10;
        '''
        return self.run_sql_query(query, "Recent orders with full details")
    
    def query_7_left_join(self):
        """Query 7: LEFT JOIN - Find customers without orders"""
        query = '''
        SELECT 
            c.customer_id,
            c.name,
            c.email,
            c.city,
            COUNT(o.order_id) as order_count
        FROM customers c
        LEFT JOIN orders o ON c.customer_id = o.customer_id
        GROUP BY c.customer_id, c.name, c.email, c.city
        HAVING COUNT(o.order_id) = 0;
        '''
        return self.run_sql_query(query, "Customers who never ordered (potential leads!)")
    
    def query_8_subquery(self):
        """Query 8: Subquery - Products above average price"""
        query = '''
        SELECT 
            product_name,
            category,
            price,
            ROUND((price - (SELECT AVG(price) FROM products)), 2) as price_vs_avg
        FROM products
        WHERE price > (SELECT AVG(price) FROM products)
        ORDER BY price DESC;
        '''
        return self.run_sql_query(query, "Premium products (above average price)")
    
    def query_9_advanced_grouping(self):
        """Query 9: Multi-level grouping - Category performance by city"""
        query = '''
        SELECT 
            c.city,
            p.category,
            COUNT(o.order_id) as orders,
            SUM(o.total_amount) as revenue
        FROM orders o
        JOIN customers c ON o.customer_id = c.customer_id
        JOIN products p ON o.product_id = p.product_id
        WHERE o.status = 'Completed'
        GROUP BY c.city, p.category
        ORDER BY c.city, revenue DESC;
        '''
        return self.run_sql_query(query, "Category performance by city")
    
    def query_10_date_analysis(self):
        """Query 10: Date-based analysis - Monthly sales trend"""
        query = '''
        SELECT 
            strftime('%Y-%m', order_date) as month,
            COUNT(*) as orders,
            SUM(total_amount) as revenue,
            AVG(total_amount) as avg_order_value
        FROM orders
        WHERE status = 'Completed'
        GROUP BY strftime('%Y-%m', order_date)
        ORDER BY month DESC;
        '''
        return self.run_sql_query(query, "Monthly sales trend")
    
    def generate_business_report(self):
        """Generate comprehensive business insights report"""
        print("\n" + "="*80)
        print("📊 COMPREHENSIVE BUSINESS ANALYTICS REPORT")
        print("="*80)
        
        # 1. Overall metrics
        query1 = '''
        SELECT 
            COUNT(DISTINCT c.customer_id) as total_customers,
            COUNT(DISTINCT o.order_id) as total_orders,
            SUM(o.total_amount) as total_revenue,
            AVG(o.total_amount) as avg_order_value
        FROM customers c
        LEFT JOIN orders o ON c.customer_id = o.customer_id
        WHERE o.status = 'Completed';
        '''
        df1 = pd.read_sql_query(query1, self.conn)
        
        print("\n📈 KEY PERFORMANCE INDICATORS")
        print("-" * 80)
        print(f"Total Customers: {df1['total_customers'][0]}")
        print(f"Total Orders: {df1['total_orders'][0]}")
        print(f"Total Revenue: ₹{df1['total_revenue'][0]:,.2f}")
        print(f"Average Order Value: ₹{df1['avg_order_value'][0]:,.2f}")
        
        # 2. Top performing cities
        query2 = '''
        SELECT 
            c.city,
            SUM(o.total_amount) as revenue
        FROM customers c
        JOIN orders o ON c.customer_id = o.customer_id
        WHERE o.status = 'Completed'
        GROUP BY c.city
        ORDER BY revenue DESC
        LIMIT 3;
        '''
        df2 = pd.read_sql_query(query2, self.conn)
        
        print("\n🏆 TOP 3 CITIES BY REVENUE")
        print("-" * 80)
        for idx, row in df2.iterrows():
            print(f"{idx+1}. {row['city']}: ₹{row['revenue']:,.2f}")
        
        # 3. Best selling products
        query3 = '''
        SELECT 
            p.product_name,
            SUM(o.quantity) as units_sold,
            SUM(o.total_amount) as revenue
        FROM products p
        JOIN orders o ON p.product_id = o.product_id
        WHERE o.status = 'Completed'
        GROUP BY p.product_name
        ORDER BY revenue DESC
        LIMIT 5;
        '''
        df3 = pd.read_sql_query(query3, self.conn)
        
        print("\n🌟 TOP 5 BEST-SELLING PRODUCTS")
        print("-" * 80)
        for idx, row in df3.iterrows():
            print(f"{idx+1}. {row['product_name']}: {row['units_sold']} units sold (₹{row['revenue']:,.2f})")
        
        # 4. Customer insights
        query4 = '''
        SELECT 
            customer_type,
            COUNT(*) as customer_count,
            AVG(total_spent) as avg_spent
        FROM (
            SELECT 
                c.customer_type,
                SUM(o.total_amount) as total_spent
            FROM customers c
            LEFT JOIN orders o ON c.customer_id = o.customer_id
            WHERE o.status = 'Completed'
            GROUP BY c.customer_id, c.customer_type
        )
        GROUP BY customer_type;
        '''
        df4 = pd.read_sql_query(query4, self.conn)
        
        print("\n👥 CUSTOMER SEGMENT ANALYSIS")
        print("-" * 80)
        for idx, row in df4.iterrows():
            print(f"{row['customer_type']}: {row['customer_count']} customers, "
                  f"Avg spent: ₹{row['avg_spent']:,.2f}")
        
        # 5. Order status breakdown
        query5 = '''
        SELECT 
            status,
            COUNT(*) as order_count,
            SUM(total_amount) as revenue
        FROM orders
        GROUP BY status;
        '''
        df5 = pd.read_sql_query(query5, self.conn)
        
        print("\n📦 ORDER STATUS BREAKDOWN")
        print("-" * 80)
        for idx, row in df5.iterrows():
            print(f"{row['status']}: {row['order_count']} orders (₹{row['revenue']:,.2f})")
        
        print("\n" + "="*80)
        print("✅ Report generated successfully!")
        print("="*80)
    
    def export_to_csv(self, query, filename):
        """Export query results to CSV (for Pandas analysis)"""
        df = pd.read_sql_query(query, self.conn)
        df.to_csv(filename, index=False)
        print(f"\n✅ Exported to {filename} ({len(df)} rows)")
        return df
    
    def close(self):
        """Close database connection"""
        self.conn.close()
        print("\n✅ Database connection closed")


def main():
    """Main execution function"""
    
    print("="*80)
    print("🎯 DAY 15: SQL BASICS FOR DATA ANALYSTS")
    print("Sales Database Analysis System")
    print("="*80)
    
    # Initialize analyzer
    analyzer = SalesDatabaseAnalyzer('sales_analysis.db')
    
    # Setup database
    print("\n📋 STEP 1: Setting up database...")
    analyzer.create_tables()
    analyzer.populate_sample_data()
    
    # Run all SQL queries (these are what you'll face in interviews!)
    print("\n\n📊 STEP 2: Running SQL queries...")
    
    analyzer.query_1_basic_select()
    input("\nPress Enter to continue to next query...")
    
    analyzer.query_2_where_filter()
    input("\nPress Enter to continue...")
    
    analyzer.query_3_aggregation()
    input("\nPress Enter to continue...")
    
    analyzer.query_4_group_by()
    input("\nPress Enter to continue...")
    
    analyzer.query_5_having_clause()
    input("\nPress Enter to continue...")
    
    analyzer.query_6_inner_join()
    input("\nPress Enter to continue...")
    
    analyzer.query_7_left_join()
    input("\nPress Enter to continue...")
    
    analyzer.query_8_subquery()
    input("\nPress Enter to continue...")
    
    analyzer.query_9_advanced_grouping()
    input("\nPress Enter to continue...")
    
    analyzer.query_10_date_analysis()
    input("\nPress Enter to continue to report...")
    
    # Generate business report
    print("\n\n📊 STEP 3: Generating business report...")
    analyzer.generate_business_report()
    
    # Export data for further analysis
    print("\n\n📁 STEP 4: Exporting data for Pandas analysis...")
    query = '''
    SELECT 
        o.order_id,
        c.name as customer_name,
        c.city,
        c.customer_type,
        p.product_name,
        p.category,
        o.quantity,
        o.total_amount,
        o.order_date,
        o.status
    FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id
    JOIN products p ON o.product_id = p.product_id;
    '''
    analyzer.export_to_csv(query, 'sales_export.csv')
    
    # Close connection
    analyzer.close()
    
    print("\n" + "="*80)
    print("🎉 DAY 15 COMPLETE!")
    print("="*80)
    print("\nYou've learned:")
    print("✅ Creating databases and tables")
    print("✅ SELECT queries with WHERE, ORDER BY")
    print("✅ Aggregations (COUNT, SUM, AVG, MAX, MIN)")
    print("✅ GROUP BY and HAVING")
    print("✅ JOINS (INNER, LEFT)")
    print("✅ Subqueries")
    print("✅ Date-based analysis")
    print("✅ Combining SQL with Pandas")
    print("\n🎯 These are the EXACT skills NetWeb will test!")


if __name__ == "__main__":
    main()