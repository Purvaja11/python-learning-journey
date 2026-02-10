"""
DAY 16: ADVANCED SQL ANALYTICS SYSTEM
Window functions, CTEs, CASE statements, and complex business queries

Skills: Advanced SQL patterns used in real data analyst work
"""

import sqlite3
import pandas as pd
from datetime import datetime

class AdvancedSQLAnalyzer:
    """Advanced SQL techniques for professional data analysis"""
    
    def __init__(self, db_name='sales_analysis.db'):
        """Connect to existing database from Day 15"""
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        print(f"✅ Connected to: {db_name}")
        print("📊 Using database from Day 15\n")
    
    def run_query(self, query, description):
        """Execute and display query results"""
        print("=" * 80)
        print(f"📊 {description}")
        print("=" * 80)
        print(f"\nSQL Query:\n{query}\n")
        
        try:
            df = pd.read_sql_query(query, self.conn)
            print("Results:")
            print(df.to_string(index=False))
            print(f"\n✅ {len(df)} rows returned\n")
            return df
        except Exception as e:
            print(f"❌ Error: {e}\n")
            return None
    
    # =========================================================================
    # WINDOW FUNCTIONS
    # =========================================================================
    
    def query_1_row_number(self):
        """Window Function 1: ROW_NUMBER - Number orders per customer"""
        query = '''
        SELECT 
            c.name as customer_name,
            o.order_date,
            o.total_amount,
            ROW_NUMBER() OVER (
                PARTITION BY c.customer_id 
                ORDER BY o.order_date
            ) as order_number
        FROM orders o
        JOIN customers c ON o.customer_id = c.customer_id
        WHERE o.status = 'Completed'
        ORDER BY c.name, o.order_date
        LIMIT 20;
        '''
        return self.run_query(query, 
            "WINDOW FUNCTION: ROW_NUMBER - Track order sequence per customer")
    
    def query_2_rank_products(self):
        """Window Function 2: RANK - Rank products by sales"""
        query = '''
        WITH product_sales AS (
            SELECT 
                p.product_name,
                p.category,
                SUM(o.quantity) as units_sold,
                SUM(o.total_amount) as revenue
            FROM products p
            JOIN orders o ON p.product_id = o.product_id
            WHERE o.status = 'Completed'
            GROUP BY p.product_id, p.product_name, p.category
        )
        SELECT 
            product_name,
            category,
            units_sold,
            revenue,
            RANK() OVER (ORDER BY revenue DESC) as overall_rank,
            RANK() OVER (PARTITION BY category ORDER BY revenue DESC) as rank_in_category
        FROM product_sales
        ORDER BY overall_rank;
        '''
        return self.run_query(query,
            "WINDOW FUNCTION: RANK - Product rankings overall and within category")
    
    def query_3_top_n_per_group(self):
        """Window Function 3: Top 2 products per category"""
        query = '''
        WITH ranked_products AS (
            SELECT 
                p.category,
                p.product_name,
                SUM(o.total_amount) as revenue,
                ROW_NUMBER() OVER (
                    PARTITION BY p.category 
                    ORDER BY SUM(o.total_amount) DESC
                ) as rank_in_category
            FROM products p
            JOIN orders o ON p.product_id = o.product_id
            WHERE o.status = 'Completed'
            GROUP BY p.category, p.product_name
        )
        SELECT 
            category,
            product_name,
            revenue,
            rank_in_category
        FROM ranked_products
        WHERE rank_in_category <= 2
        ORDER BY category, rank_in_category;
        '''
        return self.run_query(query,
            "TOP N PER GROUP: Best 2 products in each category (Interview Pattern!)")
    
    def query_4_running_total(self):
        """Window Function 4: Running total (cumulative sum)"""
        query = '''
        WITH daily_sales AS (
            SELECT 
                DATE(order_date) as sale_date,
                SUM(total_amount) as daily_revenue
            FROM orders
            WHERE status = 'Completed'
            GROUP BY DATE(order_date)
        )
        SELECT 
            sale_date,
            daily_revenue,
            SUM(daily_revenue) OVER (
                ORDER BY sale_date
                ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
            ) as running_total
        FROM daily_sales
        ORDER BY sale_date DESC
        LIMIT 15;
        '''
        return self.run_query(query,
            "RUNNING TOTAL: Cumulative revenue over time")
    
    # =========================================================================
    # COMMON TABLE EXPRESSIONS (CTEs)
    # =========================================================================
    
    def query_5_multiple_ctes(self):
        """CTEs: Chain multiple CTEs for complex analysis"""
        query = '''
        WITH 
        -- CTE 1: Calculate customer totals
        customer_totals AS (
            SELECT 
                customer_id,
                COUNT(*) as order_count,
                SUM(total_amount) as total_spent,
                AVG(total_amount) as avg_order
            FROM orders
            WHERE status = 'Completed'
            GROUP BY customer_id
        ),
        -- CTE 2: Calculate overall averages
        overall_stats AS (
            SELECT 
                AVG(total_spent) as avg_customer_value,
                AVG(order_count) as avg_orders_per_customer
            FROM customer_totals
        ),
        -- CTE 3: Compare customers to averages
        customer_comparison AS (
            SELECT 
                ct.*,
                os.avg_customer_value,
                os.avg_orders_per_customer,
                CASE
                    WHEN ct.total_spent > os.avg_customer_value * 2 THEN 'Top Tier'
                    WHEN ct.total_spent > os.avg_customer_value THEN 'Above Average'
                    WHEN ct.total_spent > os.avg_customer_value * 0.5 THEN 'Average'
                    ELSE 'Below Average'
                END as performance_tier
            FROM customer_totals ct
            CROSS JOIN overall_stats os
        )
        SELECT 
            c.name,
            c.city,
            c.customer_type,
            cc.order_count,
            ROUND(cc.total_spent, 2) as total_spent,
            ROUND(cc.avg_order, 2) as avg_order,
            cc.performance_tier
        FROM customer_comparison cc
        JOIN customers c ON cc.customer_id = c.customer_id
        ORDER BY cc.total_spent DESC
        LIMIT 15;
        '''
        return self.run_query(query,
            "MULTIPLE CTEs: Customer performance tiers vs. averages")
    
    def query_6_recursive_cte(self):
        """CTEs: Month-over-month growth analysis"""
        query = '''
        WITH monthly_revenue AS (
            SELECT 
                strftime('%Y-%m', order_date) as month,
                SUM(total_amount) as revenue
            FROM orders
            WHERE status = 'Completed'
            GROUP BY strftime('%Y-%m', order_date)
        ),
        revenue_with_previous AS (
            SELECT 
                month,
                revenue,
                LAG(revenue, 1) OVER (ORDER BY month) as prev_month_revenue
            FROM monthly_revenue
        )
        SELECT 
            month,
            ROUND(revenue, 2) as current_revenue,
            ROUND(prev_month_revenue, 2) as previous_revenue,
            ROUND(revenue - prev_month_revenue, 2) as revenue_change,
            ROUND(
                ((revenue - prev_month_revenue) / prev_month_revenue * 100), 
                2
            ) as growth_percent
        FROM revenue_with_previous
        WHERE prev_month_revenue IS NOT NULL
        ORDER BY month DESC;
        '''
        return self.run_query(query,
            "GROWTH ANALYSIS: Month-over-month revenue change (CTE + LAG)")
    
    # =========================================================================
    # CASE STATEMENTS
    # =========================================================================
    
    def query_7_case_segmentation(self):
        """CASE: Customer segmentation"""
        query = '''
        WITH customer_metrics AS (
            SELECT 
                c.customer_id,
                c.name,
                c.city,
                c.customer_type,
                COUNT(o.order_id) as order_count,
                SUM(o.total_amount) as total_spent,
                AVG(o.total_amount) as avg_order_value,
                MAX(o.order_date) as last_order_date,
                julianday('now') - julianday(MAX(o.order_date)) as days_since_last_order
            FROM customers c
            LEFT JOIN orders o ON c.customer_id = o.customer_id
            WHERE o.status = 'Completed' OR o.status IS NULL
            GROUP BY c.customer_id, c.name, c.city, c.customer_type
        )
        SELECT 
            name,
            city,
            order_count,
            ROUND(total_spent, 2) as total_spent,
            ROUND(avg_order_value, 2) as avg_order,
            CASE
                WHEN order_count = 0 THEN 'Never Purchased'
                WHEN days_since_last_order > 60 THEN 'At Risk'
                WHEN days_since_last_order > 30 THEN 'Needs Attention'
                WHEN total_spent > 5000 THEN 'VIP Active'
                ELSE 'Active'
            END as customer_status,
            CASE
                WHEN total_spent > 10000 THEN 'Platinum'
                WHEN total_spent > 5000 THEN 'Gold'
                WHEN total_spent > 2000 THEN 'Silver'
                WHEN total_spent > 0 THEN 'Bronze'
                ELSE 'Prospect'
            END as loyalty_tier
        FROM customer_metrics
        ORDER BY total_spent DESC;
        '''
        return self.run_query(query,
            "CASE STATEMENTS: Customer segmentation with multiple tiers")
    
    def query_8_case_pivot(self):
        """CASE: Pivot-style aggregation (orders by status per customer)"""
        query = '''
        SELECT 
            c.customer_id,
            c.name,
            COUNT(o.order_id) as total_orders,
            SUM(CASE WHEN o.status = 'Completed' THEN 1 ELSE 0 END) as completed,
            SUM(CASE WHEN o.status = 'Pending' THEN 1 ELSE 0 END) as pending,
            SUM(CASE WHEN o.status = 'Cancelled' THEN 1 ELSE 0 END) as cancelled,
            ROUND(
                SUM(CASE WHEN o.status = 'Completed' THEN 1 ELSE 0 END) * 100.0 / 
                COUNT(o.order_id), 
                1
            ) as completion_rate
        FROM customers c
        JOIN orders o ON c.customer_id = o.customer_id
        GROUP BY c.customer_id, c.name
        HAVING COUNT(o.order_id) > 2
        ORDER BY completion_rate DESC
        LIMIT 15;
        '''
        return self.run_query(query,
            "CASE + PIVOT: Order status breakdown per customer")
    
    # =========================================================================
    # ADVANCED DATE ANALYSIS
    # =========================================================================
    
    def query_9_date_analysis(self):
        """Advanced date analysis: Sales by day of week"""
        query = '''
        SELECT 
            CASE CAST(strftime('%w', order_date) AS INTEGER)
                WHEN 0 THEN 'Sunday'
                WHEN 1 THEN 'Monday'
                WHEN 2 THEN 'Tuesday'
                WHEN 3 THEN 'Wednesday'
                WHEN 4 THEN 'Thursday'
                WHEN 5 THEN 'Friday'
                WHEN 6 THEN 'Saturday'
            END as day_of_week,
            CAST(strftime('%w', order_date) AS INTEGER) as day_num,
            COUNT(*) as order_count,
            ROUND(SUM(total_amount), 2) as total_revenue,
            ROUND(AVG(total_amount), 2) as avg_order_value
        FROM orders
        WHERE status = 'Completed'
        GROUP BY day_num
        ORDER BY day_num;
        '''
        return self.run_query(query,
            "DATE ANALYSIS: Sales patterns by day of week")
    
    def query_10_cohort_analysis(self):
        """Advanced: Customer cohort analysis"""
        query = '''
        WITH customer_first_order AS (
            SELECT 
                customer_id,
                strftime('%Y-%m', MIN(order_date)) as cohort_month,
                MIN(order_date) as first_order_date
            FROM orders
            WHERE status = 'Completed'
            GROUP BY customer_id
        ),
        cohort_stats AS (
            SELECT 
                cfo.cohort_month,
                COUNT(DISTINCT cfo.customer_id) as customers_in_cohort,
                COUNT(DISTINCT o.order_id) as total_orders,
                ROUND(SUM(o.total_amount), 2) as total_revenue,
                ROUND(AVG(o.total_amount), 2) as avg_order_value
            FROM customer_first_order cfo
            JOIN orders o ON cfo.customer_id = o.customer_id
            WHERE o.status = 'Completed'
            GROUP BY cfo.cohort_month
        )
        SELECT 
            cohort_month,
            customers_in_cohort,
            total_orders,
            total_revenue,
            avg_order_value,
            ROUND(total_revenue / customers_in_cohort, 2) as revenue_per_customer,
            ROUND(total_orders * 1.0 / customers_in_cohort, 2) as orders_per_customer
        FROM cohort_stats
        ORDER BY cohort_month;
        '''
        return self.run_query(query,
            "COHORT ANALYSIS: Performance by customer acquisition month")
    
    def generate_executive_summary(self):
        """Generate comprehensive executive summary"""
        print("\n" + "=" * 80)
        print("📊 EXECUTIVE SUMMARY REPORT")
        print("=" * 80)
        
        # Overall metrics
        query = '''
        SELECT 
            COUNT(DISTINCT c.customer_id) as total_customers,
            COUNT(DISTINCT CASE WHEN o.order_id IS NOT NULL THEN c.customer_id END) as active_customers,
            COUNT(o.order_id) as total_orders,
            SUM(CASE WHEN o.status = 'Completed' THEN 1 ELSE 0 END) as completed_orders,
            ROUND(SUM(CASE WHEN o.status = 'Completed' THEN o.total_amount ELSE 0 END), 2) as total_revenue,
            ROUND(AVG(CASE WHEN o.status = 'Completed' THEN o.total_amount END), 2) as avg_order_value
        FROM customers c
        LEFT JOIN orders o ON c.customer_id = o.customer_id;
        '''
        
        df = pd.read_sql_query(query, self.conn)
        
        print("\n📈 KEY METRICS:")
        print(f"Total Customers:     {df['total_customers'][0]}")
        print(f"Active Customers:    {df['active_customers'][0]}")
        print(f"Total Orders:        {df['total_orders'][0]}")
        print(f"Completed Orders:    {df['completed_orders'][0]}")
        print(f"Total Revenue:       ₹{df['total_revenue'][0]:,.2f}")
        print(f"Avg Order Value:     ₹{df['avg_order_value'][0]:,.2f}")
        
        # Customer segments
        query = '''
        WITH customer_spending AS (
            SELECT 
                CASE
                    WHEN SUM(total_amount) > 10000 THEN 'Platinum'
                    WHEN SUM(total_amount) > 5000 THEN 'Gold'
                    WHEN SUM(total_amount) > 2000 THEN 'Silver'
                    ELSE 'Bronze'
                END as tier,
                COUNT(*) as customer_count,
                SUM(total_amount) as tier_revenue
            FROM orders
            WHERE status = 'Completed'
            GROUP BY customer_id
        )
        SELECT 
            tier,
            SUM(customer_count) as customers,
            ROUND(SUM(tier_revenue), 2) as revenue,
            ROUND(AVG(tier_revenue), 2) as avg_customer_value
        FROM customer_spending
        GROUP BY tier
        ORDER BY 
            CASE tier
                WHEN 'Platinum' THEN 1
                WHEN 'Gold' THEN 2
                WHEN 'Silver' THEN 3
                ELSE 4
            END;
        '''
        
        df = pd.read_sql_query(query, self.conn)
        print("\n💎 CUSTOMER TIERS:")
        print(df.to_string(index=False))
        
        print("\n" + "=" * 80)
        print("✅ Executive Summary Complete")
        print("=" * 80)
    
    def close(self):
        """Close database connection"""
        self.conn.close()
        print("\n✅ Database connection closed")


def main():
    """Main execution"""
    print("=" * 80)
    print("🎯 DAY 16: ADVANCED SQL ANALYTICS")
    print("=" * 80)
    print("\nAdvanced SQL techniques for professional data analysis:\n")
    print("• Window Functions (ROW_NUMBER, RANK, LAG)")
    print("• Common Table Expressions (CTEs)")
    print("• CASE statements for segmentation")
    print("• Advanced date analysis")
    print("• Cohort analysis")
    print("\n" + "=" * 80)
    
    # Initialize analyzer
    analyzer = AdvancedSQLAnalyzer()
    
    # Run all advanced queries
    print("\n🔥 PART 1: WINDOW FUNCTIONS")
    input("Press Enter to continue...")
    analyzer.query_1_row_number()
    input("Press Enter to continue...")
    analyzer.query_2_rank_products()
    input("Press Enter to continue...")
    analyzer.query_3_top_n_per_group()
    input("Press Enter to continue...")
    analyzer.query_4_running_total()
    
    print("\n🔥 PART 2: COMMON TABLE EXPRESSIONS")
    input("Press Enter to continue...")
    analyzer.query_5_multiple_ctes()
    input("Press Enter to continue...")
    analyzer.query_6_recursive_cte()
    
    print("\n🔥 PART 3: CASE STATEMENTS")
    input("Press Enter to continue...")
    analyzer.query_7_case_segmentation()
    input("Press Enter to continue...")
    analyzer.query_8_case_pivot()
    
    print("\n🔥 PART 4: ADVANCED DATE ANALYSIS")
    input("Press Enter to continue...")
    analyzer.query_9_date_analysis()
    input("Press Enter to continue...")
    analyzer.query_10_cohort_analysis()
    
    print("\n🔥 PART 5: EXECUTIVE SUMMARY")
    input("Press Enter to generate report...")
    analyzer.generate_executive_summary()
    
    # Close connection
    analyzer.close()
    
    print("\n" + "=" * 80)
    print("🎉 DAY 16 ADVANCED SQL COMPLETE!")
    print("=" * 80)
    print("\nYou've mastered:")
    print("✅ Window functions (ROW_NUMBER, RANK)")
    print("✅ Common Table Expressions (CTEs)")
    print("✅ CASE statements for logic")
    print("✅ Advanced date analysis")
    print("✅ Cohort analysis")
    print("✅ Complex business queries")
    print("\n🎯 These are ADVANCED skills that set you apart!")


if __name__ == "__main__":
    main()
