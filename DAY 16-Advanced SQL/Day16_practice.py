"""
DAY 16 PRACTICE: Advanced SQL (NO SOLUTIONS)
Window functions, CTEs, CASE statements - Professional level!

Complete these BEFORE checking solutions.
These are advanced patterns used in senior analyst roles!
"""

import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect('sales_analysis.db')

print("="*80)
print("🎯 DAY 16 ADVANCED SQL PRACTICE")
print("="*80)
print("\nThese are ADVANCED interview questions!")
print("Try to solve them yourself first.\n")

# =============================================================================
# EXERCISE 1: WINDOW FUNCTION - ROW_NUMBER
# =============================================================================
print("\n" + "="*80)
print("EXERCISE 1: Window Function - ROW_NUMBER")
print("="*80)
print("TASK: Find the first 3 orders for each customer")

#Tables: orders, customers
#Show:
#- customer name
#- order_date
#- total_amount
#- order_number (1, 2, 3 for each customer)

#Filter: Only show orders numbered 1, 2, or 3
#Sort by: customer name, order_number

#Hint: Use ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date)

#YOUR SQL QUERY HERE:

# TODO: Write your SQL query
solution_1 = '''
SELECT 
  c.name as customer_name,
  o.order_date
  o.total_amount,
  ROW_NUMBER() OVER(
    PARTITION BY c.customer_id 
    ORDER BY o.order_date
  ) as order_number
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
WHERE o.status = 'Completed'
  AND ROW_NUMBER() OVER (
    PARTITION BY c.customer_id
    ORDER BY o.order_date
  ) <= 3
ORDER BY c.name, order_number;
'''
# Alternative solution (better - using subquery)
solution_1_alt = '''
WITH numbered_orders AS (
  SELECT 
    c.name as customer_name,
    o.order_date,
    o.total_amount,
    ROW_NUMBER() OVER(
      PARTITION BY c.customer_id
      ORDER BY o.order_date
    ) as order_number
  FROM orders o
  JOIN customer c ON o.customer_id = c.customer_id
  WHERE o.status = 'Completed'
)
SELECT 
  customer_name,
  order_date,
  total_amount,
  order_number
FROM numbered_orders
WHERE order_number <= 3
ORDER BY customer_name, order_number;
'''
# Uncomment to test:
print("SOLUTION (Using CTE - recommened):")
print(solution_1_alt)
df1 = pd.read_sql_query(solution_1_alt, conn)
print("\nResults:")
print(df1.to_string(index=False))
print(f"\n {len(df1)} orders returned")

# =============================================================================
# EXERCISE 2: WINDOW FUNCTION - RANK
# =============================================================================
print("\n" + "="*80)
print("EXERCISE 2: Window Function - RANK")
print("="*80)
print("TASK: Rank cities by total revenue")

#Tables: customers, orders
#Show:
#- city
#- total revenue (SUM of completed orders)
#- number of orders
#- rank (1 = highest revenue)

#Filter: Only 'Completed' orders
#Sort by: rank

#Hint: Use RANK() OVER (ORDER BY total_revenue DESC)

#YOUR SQL QUERY HERE:


# TODO: Write your SQL query
solution_2 = '''
WITH city_revenue AS (
  SELECT 
    c.city,
    COUNT(o.order_id) as order_count,
    ROUND(SUM(o.total_amount), 2) as total_revenue
  FROM customers c
  JOIN orders o ON c.customer_id = o.customer_id
  WHERE o.status = 'Completed'
  GROUP BY c.city
)
SELECT
  city,
  order_count,
  total_revenue,
  RANK() OVER(ORDER BY total_revenue DESC) as rank
FROM city_revenue
ORDER BY rank;
'''


# Uncomment to test:
df2 = pd.read_sql_query(solution_2, conn)
print(df2.to_string(index=False))


# =============================================================================
# EXERCISE 3: TOP N PER GROUP (ADVANCED!)
# =============================================================================
print("\n" + "="*80)
print("EXERCISE 3: Top N Per Group (Interview Favorite!)")
print("="*80)
print("TASK: Find the top 3 customers by spending in EACH city")

#Tables: customers, orders
#Show:
#- city
#- customer name
#- total spent
#- rank within city (1, 2, 3)

#Filter: Only 'Completed' orders
#Show: Only ranks 1, 2, 3

#Hint: 
#1. Use a CTE or subquery to calculate spending per customer
#2. Use ROW_NUMBER() OVER (PARTITION BY city ORDER BY total_spent DESC)
#3. Filter WHERE rank <= 3

#YOUR SQL QUERY HERE:

# TODO: Write your SQL query
solution_3 = '''
WITH customer_spending AS (
  SELECT
    c.customer_id,
    c.name,
    c.city,
    SUM(o.total_amount) as total_spent
  FROM customers c
  JOIN orders o ON c.customer_id = o.customer_id
  WHERE o.status = 'Completed'
  GROUP BY c.customer_id, c.name, c.city
),
ranked_customers AS (
  SELECT
    city,
    name,
    total_apent,
    ROW_NUMBER() OVER (
      PARTITION BY city
      ORDER BY total_spent DESC
    ) as rank_in_city
  FROM customer_spending
)
SELECT
  city,
  name,
  ROUND(total_spent, 2) as total_spent,
  rank_in_city
FROM ranked_customers
WHERE rank_in_city <= 3
ORDER BY city, rank_in_city;
'''

# Uncomment to test:
df3 = pd.read_sql_query(solution_3, conn)
print(df3.to_string(index=False))


# =============================================================================
# EXERCISE 4: RUNNING TOTAL
# =============================================================================
print("\n" + "="*80)
print("EXERCISE 4: Running Total (Cumulative Sum)")
print("="*80)
print("TASK: Calculate cumulative revenue by date")

#Tables: orders
#Show:
#- order_date
#- daily_revenue (sum for that day)
#- running_total (cumulative sum up to that date)

#Filter: Only 'Completed' orders
#Sort by: order_date

#Hint: Use SUM() OVER (ORDER BY date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)

#YOUR SQL QUERY HERE:


# TODO: Write your SQL query
solution_4 = '''
WITH daily_revenue AS (
  SELECT 
    DATE(order_date) as order_date,
    ROUND(SUM(total_amount), 2) as daily_revenue
  FROM orders
  WHERE status = 'Completed'
  GROUP BY DATE(order_date)
)
SELECT
  order_date,
  daily_revenue,
  ROUND(
    SUM(daily_revenue) OVER (
      ORDER BY order_date
      ROWS BETWEEN UNBOUNDED PECEDING AND CURRENT ROW
    ),
    2
  ) as running_total
FROM daily_revenue
ORDER BY order_date DESC
LIMIT 15;
'''

# Uncomment to test:
df4 = pd.read_sql_query(solution_4, conn)
print(df4.to_string(index=False))


# =============================================================================
# EXERCISE 5: COMMON TABLE EXPRESSION (CTE)
# =============================================================================
print("\n" + "="*80)
print("EXERCISE 5: CTE - Clean Complex Query")
print("="*80)
print("TASK: Find customers who spent more than the average customer")

#Use CTE to make it readable!

#Step 1: CTE to calculate average spending per customer
#Step 2: Main query to find customers above that average

#Show:
#- customer name
#- total spent
#- difference from average

#Sort by: total spent (descending)

#YOUR SQL QUERY HERE:


# TODO: Write your SQL query
solution_5 = '''
WITH customer_spending AS (
  SELECT 
    c.customer_id,
    c.name,
    SUM(o.total_amount) as total_spent
  FROM customers c
  JOIN orders o ON c.customer_id = o.customer_id
  WHERE o.status = 'Completed'
  GROUP BY c.customer_id, c.name
),
average_spending AS (
  SELECT AVG(total_spent) as avg_spent
  FROM customer_spending
)
SELECT
  cs.name,
  ROUND(cs.total_spent, 2) as total_apent,
  ROUND(avg.avg_spent, 2) as average_spent,
  ROUND(cs.total_spent - avg.avg_spent, 2) as difference_from_avg
FROM customer_spending cs
CROSS JOIN average_spending avg
WHERE cs.total_spent > avg.avg_spent
ORDER BY cs.total_spent DESC;
'''

# Uncomment to test:
df5 = pd.read_sql_query(solution_5, conn)
print(df5.to_string(index=False))


# =============================================================================
# EXERCISE 6: MULTIPLE CTEs
# =============================================================================
print("\n" + "="*80)
print("EXERCISE 6: Multiple CTEs - Month-over-Month Growth")
print("="*80)
print("TASK: Calculate month-over-month revenue growth")

#Use multiple CTEs:
#1. monthly_revenue - sum revenue per month
#2. revenue_with_previous - add previous month's revenue using LAG()
#3. Main query - calculate growth percentage

#Show:
#- month (YYYY-MM format)
#- current_revenue
#- previous_revenue
#- growth_percent (rounded to 2 decimals)

#Filter: Only show months that have a previous month
#Sort by: month descending

#YOUR SQL QUERY HERE:


# TODO: Write your SQL query
solution_6 = '''
WITH 
monthly_revenue AS (
  SELECT 
    strftime('%Y-%m', order_date) as month,
    ROUND(SUM(total_amount), 2) as revenue 
  FROM orders
  WHERE status = 'Completed'
  GROUP BY strftime('%Y-%m', order_date)
),
revenue_with_previous AS (
  SELECT 
    month,
    revenue,
    LAG(revenue, 1) OVER (ORDER BY month) as previous_revenue
  FROM monthly_revenue
)
SELECT
  month,
  revenue as current_revenue,
  previous_revenue,
  ROUND(revenue - previous_revenue, 2) as revenue_change,
  ROUND(
    ((revenue - previous_revenue) / previous_revenue * 100),
    2
  ) as growth_percent
FROM revenue_with_previous
WHERE previous_revenue IS NOT NULL
ORDER BY month DESC;
'''

# Uncomment to test:
df6 = pd.read_sql_query(solution_6, conn)
print(df6.to_string(index=False))


# =============================================================================
# EXERCISE 7: CASE STATEMENT - SEGMENTATION
# =============================================================================
print("\n" + "="*80)
print("EXERCISE 7: CASE Statement - Customer Segmentation")
print("="*80)
print("TASK: Segment customers by their total spending")

#Tables: customers, orders
#Show:
#- customer name
#- total spent
#- segment:
  #* 'High Value' if spent > 8000
  #* 'Medium Value' if spent > 3000
  #* 'Low Value' if spent > 0
 # * 'No Purchases' if spent = 0

#Filter: Only 'Completed' orders (but include customers with 0 orders)
#Sort by: total spent descending

#Hint: Use LEFT JOIN and CASE WHEN

#YOUR SQL QUERY HERE:


# TODO: Write your SQL query
solution_7 = '''
SELECT 
  c.name,
  COALESCE(ROUND(SUM(o.total_amount), 2), 0) as total_spent,
  CASE
    WHEN COALESCE(SUM(o.total_amount), 0) > 8000 THEN 'High Value'
    WHEN COALESCE(SUM(o.total_amount), 0) > 3000 THEN 'Medium Value'
    WHEN COALESCE(SUM(o.total_amount), 0) > 0 THEN ' Low Value'
    ELSE 'No Purchases'
  END as segment
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
  AND o.status= 'Completed'
GROUP BY c.customer_id, c.name
ORDER BY total_spent DESC;
'''

# Uncomment to test:
df7 = pd.read_sql_query(solution_7, conn)
print(df7.to_string(index=False))


# =============================================================================
# EXERCISE 8: CASE STATEMENT - PIVOT
# =============================================================================
print("\n" + "="*80)
print("EXERCISE 8: CASE for PIVOT - Order Status by City")
print("="*80)
print("TASK: Show order status breakdown per city (pivot-style)")

#Tables: customers, orders
#Show:
#- city
#- total_orders (count all)
#- completed (count of completed)
#- pending (count of pending)
#- cancelled (count of cancelled)
#- completion_rate (completed / total * 100)

#Sort by: completion_rate descending

#Hint: Use SUM(CASE WHEN status = 'X' THEN 1 ELSE 0 END)

#YOUR SQL QUERY HERE:


# TODO: Write your SQL query
solution_8 = '''
SELECT
  c.city,
  COUNT(o.order_id) as total_orders,
  SUM(CASE WHEN o.status = 'Completed' THEN 1 ELSE 0 END) as completed,
  SUM(CASE WHEN o.status = 'Pending' THEN 1 ELSE 0 END) as pending,
  SUM(CASE WHEN o.status = 'Cancelled' THEN 1 ELSE 0 END) as cancelled,
  ROUND(
    SUM(CASE WHEN o.status = 'Completed' THEN 1 ELSE 0 END) * 100 /
    COUNT(o.order_id),
    1
  ) as completion_rate
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.city
ORDER BY completion_rate DESc;
'''

# Uncomment to test:
df8 = pd.read_sql_query(solution_8, conn)
print(df8.to_string(index=False))


# =============================================================================
# EXERCISE 9: DATE ANALYSIS - DAY OF WEEK
# =============================================================================
print("\n" + "="*80)
print("EXERCISE 9: Advanced Date Analysis")
print("="*80)
print("TASK: Find which day of week has most sales")

#Tables: orders
#Show:
#- day_of_week (Monday, Tuesday, etc.)
#- order_count
#- total_revenue
#- avg_order_value

#Filter: Only 'Completed' orders
#Sort by: day of week (Monday first)

#Hint: Use strftime('%w', date) to get day number (0=Sunday, 1=Monday...)
#Then use CASE to convert to names

#YOUR SQL QUERY HERE:


# TODO: Write your SQL query
solution_9 = '''
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
  ROUND(avg(total_amount), 2) as avg_order_value
FROM orders
WHERE status = 'Completed'
GROUP BY day_num
ORDER BY day_num;
'''

# Uncomment to test:
df9 = pd.read_sql_query(solution_9, conn)
print(df9.to_string(index=False))


# =============================================================================
# EXERCISE 10: COHORT ANALYSIS (VERY ADVANCED!)
# =============================================================================
print("\n" + "="*80)
print("EXERCISE 10: Cohort Analysis (Advanced!)")
print("="*80)
print("TASK: Analyze customer behavior by cohort (first purchase month)")

#Tables: orders, customers
#Show:
#- cohort_month (YYYY-MM of first purchase)
#- customers_in_cohort (count of unique customers)
#- total_revenue (sum of all their orders)
#- avg_customer_value (revenue / customer count)

#Filter: Only 'Completed' orders
#Sort by: cohort_month

#Steps:
#1. CTE to find each customer's first order month
#2. Join back to orders to get their total spending
#3. Group by cohort month

#This shows which acquisition months brought best customers!

#YOUR SQL QUERY HERE:


# TODO: Write your SQL query
solution_10 = '''
WITH customer_cohorts AS (
  SELECT
    customer_id,
    strftime('%Y-%m', MIN(order_date)) as cohort_month,
    MIN(order_date) as first_order_date\
  FROM orders
  WHERE status = 'Completed'
  GROUP BY customer_id
)
SELECT 
  cc.cohot_month,
  COUNT(DISTINCT cc.customer_id) as customers_in_cohort,
  COUNT(o.order_id) as total_orders,
  ROUND(SUM(o.total_amount), 2) as total_revenue,
  ROUND(SUM(O.total_amount) / COUNT(DISTINCT cc.customer_id), 2) as avg_customer_value
FROM customer_cohorts cc
JOIN orders o ON cc.customer_id = o.customer_id
WHERE o.status = 'Completed'
GROUP BY cc.cohort_month
ORDER BY cc.cohort_month;
'''

# Uncomment to test:
df10 = pd.read_sql_query(solution_10, conn)
print(df10.to_string(index=False))

# Close connection
conn.close()

print("\n\n" + "="*80)
print("✅ COMPLETION CHECKLIST")
print("="*80)
print("""
□ Exercise 1: ROW_NUMBER for first N per customer
□ Exercise 2: RANK cities by revenue
□ Exercise 3: Top N per group (advanced pattern!)
□ Exercise 4: Running total / cumulative sum
□ Exercise 5: CTE for readable queries
□ Exercise 6: Multiple CTEs + LAG function
□ Exercise 7: CASE for segmentation
□ Exercise 8: CASE for pivot-style aggregation
□ Exercise 9: Day of week analysis
□ Exercise 10: Cohort analysis (very advanced!)


💡 DIFFICULTY LEVELS:
Exercises 1-2: Medium (window functions basics)
Exercises 3-4: Medium-Hard (window + filtering)
Exercises 5-6: Hard (CTEs + LAG)
Exercises 7-8: Medium (CASE statements)
Exercise 9: Medium (date manipulation)
Exercise 10: Very Hard (cohort analysis)
Bonus: Expert level!

💪 LEARNING STRATEGY:
1. Try each exercise independently (no peeking!)
2. If stuck after 10-15 minutes, check the solution file
3. Understand WHY the solution works
4. Try writing it again from memory
5. Modify it to answer a different question

🚀 WHEN YOU'RE STUCK:
• Break problem into smaller steps
• Write the inner query first, then add window function
• Test each CTE separately before combining
• Use simple data first, then add complexity
• Draw the logic on paper before coding

🎓 MASTERY INDICATORS:
You've mastered advanced SQL when you can:
✓ Write window functions without reference
✓ Explain PARTITION BY vs GROUP BY
✓ Chain multiple CTEs naturally
✓ Use CASE for complex logic
✓ Solve "top N per group" instantly
✓ Explain your query logic clearly
✓ Optimize slow queries

""")

print("\n" + "="*80)
print("Good luck! These are ADVANCED patterns! 💪")
print("="*80)
