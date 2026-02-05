"""
DAY 15 PRACTICE: SQL Interview Questions (NO SOLUTIONS)
Real questions asked in data analyst interviews!

Practice these before your NetWeb interview!
Complete each exercise BEFORE looking at the solutions file.
"""

import sqlite3
import pandas as pd

# Connect to the database we created
conn = sqlite3.connect('sales_analysis.db')

print("="*80)
print("🎯 DAY 15 SQL PRACTICE EXERCISES")
print("="*80)

# =============================================================================
# EXERCISE 1: BASIC SELECT & FILTERING
# =============================================================================
print("\n" + "="*80)
print("EXERCISE 1: Basic SELECT & WHERE")
print("="*80)

print("TASK: Find all Electronics products priced between ₹500 and ₹3000\n")

#Tables: products
#Columns needed: product_name, price, category
#Filter: category = 'Electronics' AND price between 500 and 3000
#Sort by: price (ascending)

#YOUR SQL QUERY HERE:


# TODO: Write your SQL query
solution_1 = '''
SELECT product_name, price, category
FROM products
WHERE category ='Electronics' AND price BETWEEN 500 AND 3000
ORDER BY price;
'''

# Uncomment to test:
df1 = pd.read_sql_query(solution_1, conn)
print(df1.to_string(index=False))


# =============================================================================
# EXERCISE 2: AGGREGATIONS
# =============================================================================
print("\n" + "="*80)
print("EXERCISE 2: Aggregation Functions")
print("="*80)
print("TASK: Calculate statistics per category\n")

#Tables: products
#Show: 
#- category
#- COUNT(*) as product_count
#- AVG(price) as avg_price (rounded to 2 decimals)
#- MIN(price) as cheapest
#- MAX(price) as most_expensive

#Group by: category
#Sort by: avg_price (descending)

#YOUR SQL QUERY HERE:


# TODO: Write your SQL query
solution_2 = '''
SELECT 
    category,
    COUNT(*) as product_name,
    ROUND(AVG(price), 2) as avg_price,
    MIN(price) as cheapest,
    MAX(price) as most_expensive
FROM products
GROUP BY category
ORDER BY avg_price DESC;
'''

# Uncomment to test:
df2 = pd.read_sql_query(solution_2, conn)
print(df2.to_string(index=False))


# =============================================================================
# EXERCISE 3: JOINS (MOST COMMON INTERVIEW QUESTION!)
# =============================================================================
print("\n" + "="*80)
print("EXERCISE 3: INNER JOIN (Interview Favorite!)")
print("="*80)
print("TASK: Show all completed orders with customer name and product name\n")

#Tables: orders, customers, products

#Columns needed: 
#- order_id
#- customer name (from customers table)
#- product name (from products table)
#- quantity
#- total_amount
#- order_date

#Filter: Only 'Completed' orders
#Sort by: total_amount (descending)
#Limit: Top 10 orders

#Hint: You need to JOIN three tables!

#YOUR SQL QUERY HERE:


# TODO: Write your SQL query
solution_3 = '''
SELECT 
    o.order_id,
    c.name as customer_name,
    p.product_name,
    o.quantity,
    o.total_amount,
    o.order_date
FROM orders o
INNER JOIN customers c ON o.customer_id = c.customer_id
INNER JOIN products p ON o.product_id = p.product_id
WHERE o.status = 'Completed'
ORDER BY o.total_amount DESC
LIMIT 10
'''

# Uncomment to test:
df3 = pd.read_sql_query(solution_3, conn)
print(df3.to_string(index=False))


# =============================================================================
# EXERCISE 4: GROUP BY with HAVING
# =============================================================================
print("\n" + "="*80)
print("EXERCISE 4: GROUP BY with HAVING")
print("="*80)
print("TASK: Find cities with more than 5 completed orders\n")

#Tables: customers, orders
#Show:
#- city name
#- order count (COUNT)
#- total revenue (SUM of total_amount, rounded)
#- average order value (AVG of total_amount, rounded)

#Filter: Only 'Completed' orders
#Group by: city
#Having: More than 5 orders
#Sort by: total_revenue (descending)

#YOUR SQL QUERY HERE:


# TODO: Write your SQL query
solution_4 = '''
SELECT 
    c.city as city_name,
    COUNT(o.order_id) as order_count,
    ROUND(SUM(o.total_amount), 2) as total_revenue,
    ROUND(AVG(o.total_amount), 2) as average_order_value
FROM customers c
JOIN orders o  ON c.customer_id = o.customer_id
WHERE o.status = 'Completed'
GROUP BY city
HAVING COUNT(o.order_id) > 5
ORDER BY total_revenue DESC;
'''

# Uncomment to test:
df4 = pd.read_sql_query(solution_4, conn)
print(df4.to_string(index=False))


# =============================================================================
# EXERCISE 5: SUBQUERY (Advanced!)
# =============================================================================
print("\n" + "="*80)
print("EXERCISE 5: Subquery")
print("="*80)
print("TASK: Find customers who spent MORE than the average customer\n")

#Tables: customers, orders
#Show:
#- customer name
#- total spent (rounded to 2 decimals)
#- difference from average (rounded to 2 decimals)

#Filter: Only 'Completed' orders
#Having: Total spent > average total spent per customer
#Sort by: total_spent (descending)
#Limit: Top 10

#Hint: Use a subquery to calculate the average spending per customer first!

#YOUR SQL QUERY HERE:


# TODO: Write your SQL query
solution_5 = '''
SELECT 
    c.name,
    ROUND(SUM(o.total_amount), 2) as total_spent,
    ROUND(SUM(o.total_amount) - (
        SELECT AVG(total_per_customer)
        FROM (
            SELECT SUM(total_amount) as total_per_customer
            FROM orders
            WHERE status = 'Completed'
            GROUP BY customer_id
        )
    ), 2) as above_average
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE o.status = 'Completed'
GROUP BY c.customer_id, c.name
HAVING SUM(o.total_amount) > (
    SELECT AVG(total_per_customer)
    FROM(
        SELECT SUM(total_amount) as total_per_customer
        FROM orders
        WHERE status = 'Completed'
        GROUP BY customer_id
    )
)
ORDER BY total_spent DESC
LIMIT 10;
'''

# Uncomment to test:
df5 = pd.read_sql_query(solution_5, conn)
print(df5.to_string(index=False))


# =============================================================================
# EXERCISE 6: LEFT JOIN (Find missing data)
# =============================================================================
print("\n" + "="*80)
print("EXERCISE 6: LEFT JOIN - Find Inactive Customers")
print("="*80)
print("TASK: Find customers who registered but NEVER placed ANY order\n")

#Tables: customers, orders
#Show:
#- customer_id
#- name
#- email
#- city
#- join_date
#- order_count (should be 0)

#Hint: Use LEFT JOIN and find where order_id IS NULL
#Or: Use LEFT JOIN, GROUP BY, and HAVING COUNT = 0

#YOUR SQL QUERY HERE:


# TODO: Write your SQL query
solution_6 = '''
SELECT
    c.customer_id,
    c.name,
    c.email,
    c.city,
    c.join_date,
    COUNT(o.order_id) as order_count
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name, c.city, c.join_date
HAVING COUNT(o.order_id) =0;
'''

# Uncomment to test:
df6 = pd.read_sql_query(solution_6, conn)
print(df6.to_string(index=False))
print(f"\n💡 Found {len(df6)} inactive customers - potential marketing targets!")


# =============================================================================
# EXERCISE 7: DATE ANALYSIS
# =============================================================================
print("\n" + "="*80)
print("EXERCISE 7: Date-Based Analysis")
print("="*80)
print("TASK: Show orders placed in the last 30 days\n")

#Tables: orders, customers, products
#Show:
#- order_date
#- customer name
#- product name
#- quantity
#- total_amount
#- status

#Filter: order_date >= 30 days ago from today
#Sort by: order_date (descending)

#Hint: Use date('now', '-30 days') for SQLite

#YOUR SQL QUERY HERE:


# TODO: Write your SQL query
solution_7 = '''
SELECT 
    o.order_date,
    c.name as customer_name,
    p.product_name,
    o.quantity,
    o.total_amount,
    o.status
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN products p ON o.product_id = p.product_id
WHERE o.order_date >= date('now', '-30 days')
ORDER BY order_date DESC;
'''

# Uncomment to test:
df7 = pd.read_sql_query(solution_7, conn)
print(df7.to_string(index=False))
print(f"\n📊 {len(df7)} orders in last 30 days")


# =============================================================================
# EXERCISE 8: TOP N per GROUP
# =============================================================================
print("\n" + "="*80)
print("EXERCISE 8: Best-Selling Product per Category")
print("="*80)
print("TASK: Find the best-selling product in EACH category\n")

#Tables: products, orders
#Show:
#- category
#- product_name
#- total units sold (SUM of quantity)

#Filter: Only 'Completed' orders
#Hint: This is ADVANCED! You might need to use ROW_NUMBER() or a subquery

#For now, try showing all products with their sales, grouped by category:
#- Group by category and product_name
#- Sum the quantity
#- Sort by category and units_sold descending

#YOUR SQL QUERY HERE:


# TODO: Write your SQL query
solution_8 = '''
SELECT 
    p.category,
    p.product_name,
    SUM(o.quantity) as units_sold
FROM products p
JOIN orders o ON p.product_id = o.product_id
WHERE o.status = 'Completed'
GROUP BY p.category, p.product_name
ORDER BY p.category, units_sold DESC;
'''


# Uncomment to test:
df8 = pd.read_sql_query(solution_8, conn)
print(df8.to_string(index=False))


# =============================================================================
# EXERCISE 9: MULTIPLE AGGREGATIONS
# =============================================================================
print("\n" + "="*80)
print("EXERCISE 9: Customer Lifetime Value (CLV)")
print("="*80)
print("TASK: Calculate each customer's total value\n")

#Tables: customers, orders
#Show:
#- customer_id
#- name
#- city
#- customer_type
#- order_count (COUNT)
#- total_spent (SUM, rounded)
#- avg_order_value (AVG, rounded)

#Filter: Only 'Completed' orders
#Sort by: total_spent (descending)
#Limit: Top 15 customers

#YOUR SQL QUERY HERE:


# TODO: Write your SQL query
solution_9 = '''
SELECT 
    c.customer_id,
    c.name,
    c.city,
    c.customer_type,
    COUNT(o.order_id) as order_count,
    ROUND(SUM(o.total_amount), 2) as total_spent,
    ROUND(AVG(o.total_amount), 2) as avg_order_value,
    ROUND(SUM(o.total_amount) / COUNT(o.order_id), 2) as calculated_avg
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE o.status = 'Completed'
GROUP BY c.customer_id, c.name, c.city, c.customer_type
ORDER BY total_spent DESC
LIMIT 15;
'''

# Uncomment to test:
df9 = pd.read_sql_query(solution_9, conn)
print(df9.to_string(index=False))


# =============================================================================
# EXERCISE 10: COMPLEX BUSINESS QUESTION
# =============================================================================
print("\n" + "="*80)
print("EXERCISE 10: Real Business Question (Interview Style!)")
print("="*80)
print("TASK: Which customer type (Regular/Premium/VIP) generates most revenue?\n")

#Tables: customers, orders
#Show:
#- customer_type
#- customer_count (count distinct customers)
#- total_orders (count all orders)
#- total_revenue (sum of amounts, rounded)
#- avg_order_value (average amount, rounded)
#- revenue_per_customer (total_revenue / customer_count, rounded)

#Filter: Only 'Completed' orders
#Group by: customer_type
#Sort by: total_revenue (descending)

#This tells us which customer segment to focus marketing on!

#YOUR SQL QUERY HERE:


# TODO: Write your SQL query
solution_10 = '''
SELECT 
    c.customer_type,
    COUNT(DISTINCT c.customer_id) as customer_count,
    COUNT(o.order_id) as total_orders,
    ROUND(SUM(o.total_amount), 2) as total_revenue,
    ROUND(AVG(o.total_amount), 2) as avg_order_value,
    ROUND(SUM(o.total_amount) / COUNT(DISTINCT c.customer_id), 2) as revenue_per_customer
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE o.status = 'Completed'
GROUP BY c.customer_type
ORDER BY total_revenue DESC;
'''

# Uncomment to test:
df10 = pd.read_sql_query(solution_10, conn)
print(df10.to_string(index=False))
print("\n💡 BUSINESS INSIGHT:")
print("From this analysis, you can see which customer segment is most valuable.")


# Close connection when done
conn.close()

print("\n\n" + "="*80)
print("✅ COMPLETION CHECKLIST")
print("="*80)
print("""
□ Exercise 1: Basic SELECT with WHERE
□ Exercise 2: Aggregations (COUNT, SUM, AVG)
□ Exercise 3: INNER JOIN with 3 tables
□ Exercise 4: GROUP BY with HAVING
□ Exercise 5: Subquery for comparisons
□ Exercise 6: LEFT JOIN for missing data
□ Exercise 7: Date-based filtering
□ Exercise 8: Top N per group
□ Exercise 9: Customer lifetime value
□ Exercise 10: Business intelligence query

💡 LEARNING TIPS:
1. Try writing the query BEFORE running it
2. Build queries incrementally (start simple, add complexity)
3. Test each part separately
4. Use meaningful table aliases (c for customers, o for orders)
5. Format your SQL for readability

🎯 INTERVIEW PREPARATION:
- Practice explaining your query logic OUT LOUD
- Time yourself (aim for 5-10 minutes per query)
- Can you write queries from memory?
- Understand WHY each query works, not just WHAT it does

""")

print("\n" + "="*80)
print("Good luck! You've got this! 💪")
print("="*80)