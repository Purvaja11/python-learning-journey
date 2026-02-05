# 🗄️ DAY 15: SQL Fundamentals for Data Analytics

**Date:** Day 15 of 30-Day Learning Journey  
**Topic:** SQL (Structured Query Language) - Database Queries  
**Focus:** Essential database skills for data analyst roles

---

## 🎯 Learning Objectives

Today's focus was on mastering SQL - the #1 most requested skill in data analyst job postings:

✅ Understanding relational databases and SQL  
✅ Writing SELECT queries with filtering and sorting  
✅ Using aggregation functions for statistical analysis  
✅ Joining multiple tables for complex queries  
✅ Grouping data and filtering aggregated results  
✅ Combining SQL with Python/Pandas workflows  
✅ Building production-ready database applications  

---

## 📚 Core Concepts Covered

### 1. **SQL Fundamentals**

**What is SQL?**
- Standard language for working with relational databases
- Used by 90%+ of companies for data storage
- Essential skill for data analysts, engineers, and scientists
- Much faster than Pandas for large datasets

**Database Concepts:**
- Tables (rows and columns)
- Primary keys (unique identifiers)
- Foreign keys (relationships between tables)
- Indexes (query optimization)
- Schemas (database structure)

### 2. **The 5 Core SQL Operations**

Every SQL interaction uses one of these:

1. **SELECT** - Read/query data (90% of analyst work)
2. **INSERT** - Add new records
3. **UPDATE** - Modify existing records
4. **DELETE** - Remove records
5. **CREATE** - Make new tables/databases

**For data analysts:** Focus on SELECT mastery!

### 3. **Query Structure (Sacred Order)**

SQL queries MUST be written in this exact order:

```sql
SELECT columns          -- 1. What you want
FROM table             -- 2. Where to find it
WHERE conditions       -- 3. Filter rows
GROUP BY columns       -- 4. Group data
HAVING conditions      -- 5. Filter groups
ORDER BY columns       -- 6. Sort results
LIMIT number;          -- 7. Limit output
```

**Memory aid:** **S**elect **F**rom **W**here **G**roup **H**aving **O**rder **L**imit = **SF WG HOL**

### 4. **The 5 Aggregation Functions**

Complete list (there are only 5 standard ones):

```sql
COUNT(*)          -- Count rows
COUNT(column)     -- Count non-null values
SUM(column)       -- Add up values
AVG(column)       -- Calculate average
MAX(column)       -- Find maximum
MIN(column)       -- Find minimum
```

### 5. **The 4 JOIN Types**

Exactly 4 ways to combine tables:

| JOIN Type | Returns | When to Use |
|-----------|---------|-------------|
| **INNER** | Only matches | "Show matching records only" |
| **LEFT** | All from left + matches | "Show all from first table" |
| **RIGHT** | All from right + matches | Rarely used (swap tables, use LEFT) |
| **FULL OUTER** | Everything from both | "Show all records from both" |

**Most common:** INNER (matching data) and LEFT (find missing data)

### 6. **WHERE vs HAVING**

Critical distinction for interviews:

| Aspect | WHERE | HAVING |
|--------|-------|--------|
| **When** | Before grouping | After grouping |
| **Filters** | Individual rows | Grouped results |
| **Can use** | Column values | Aggregation results |
| **Example** | `WHERE price > 100` | `HAVING AVG(price) > 100` |

---

## 💻 Projects Built

### 1. **Sales Database Analyzer** 

Complete SQL + Python analytics system with realistic business data.

**Database Schema:**
```
customers (50 records)
├── customer_id (PRIMARY KEY)
├── name
├── email
├── city
├── join_date
└── customer_type

products (15 records)
├── product_id (PRIMARY KEY)
├── product_name
├── category
├── price
└── stock_quantity

orders (100 records)
├── order_id (PRIMARY KEY)
├── customer_id (FOREIGN KEY)
├── product_id (FOREIGN KEY)
├── quantity
├── order_date
├── total_amount
└── status
```

**10 Real-World Queries Implemented:**

1. **Basic SELECT** - View customer data
2. **WHERE Filtering** - Find customers by criteria
3. **Aggregations** - Calculate total revenue, average order value
4. **GROUP BY** - Sales performance by city
5. **HAVING Clause** - High-value customers (spent > threshold)
6. **INNER JOIN** - Orders with customer and product details
7. **LEFT JOIN** - Find customers without orders
8. **Subqueries** - Products above average price
9. **Multi-level Grouping** - Category performance by city
10. **Date Analysis** - Monthly sales trends

**Business Intelligence Features:**
- KPI dashboard (total customers, orders, revenue)
- Top performing cities
- Best-selling products
- Customer segment analysis
- Order status breakdown
- Automated CSV exports for further analysis

### 2. **SQL Practice Suite**

Two versions for different learning needs:

**With Solutions (`Day15_practice.py`):**
- 10 interview-style questions
- Complete working solutions
- Results display and validation
- Business insights for each query

**Without Solutions (`Day15_practice_NO_SOLUTIONS.py`):**
- Same 10 exercises
- TODO sections for writing queries
- Commented test code
- Forces independent problem-solving
- Better interview preparation

**Exercise Coverage:**
- ✅ Basic filtering and sorting
- ✅ Aggregation functions
- ✅ Multi-table joins
- ✅ GROUP BY with HAVING
- ✅ Subqueries and nested queries
- ✅ Date-based analysis
- ✅ Business intelligence queries
- ✅ Customer lifetime value calculations
- ✅ Finding missing/inactive data

### 3. **SQL Reference Cheat Sheet**

Comprehensive quick-reference guide with 17 complete sections covering all essential SQL concepts, common patterns, interview questions, and best practices.

---

## 🎓 Key Patterns Mastered

### **Pattern 1: Basic Data Retrieval**

```sql
-- Filter, sort, limit
SELECT product_name, price, category
FROM products
WHERE price > 1000 AND category = 'Electronics'
ORDER BY price DESC
LIMIT 10;
```

**Time Complexity:** O(n) for full scan, O(log n) with index

---

### **Pattern 2: Aggregation and Statistics**

```sql
-- Calculate metrics
SELECT 
    category,
    COUNT(*) as product_count,
    AVG(price) as avg_price,
    MAX(price) as highest_price,
    MIN(price) as lowest_price
FROM products
GROUP BY category
ORDER BY avg_price DESC;
```

**Time Complexity:** O(n log n) due to grouping/sorting

---

### **Pattern 3: Multi-Table Joins**

```sql
-- Combine related data
SELECT 
    c.name,
    p.product_name,
    o.quantity,
    o.total_amount
FROM orders o
INNER JOIN customers c ON o.customer_id = c.customer_id
INNER JOIN products p ON o.product_id = p.product_id
WHERE o.status = 'Completed'
ORDER BY o.total_amount DESC;
```

**Time Complexity:** O(n + m) with hash join, O(n * m) nested loop

---

### **Pattern 4: Finding Missing Data**

```sql
-- LEFT JOIN to find gaps
SELECT c.name, c.email
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_id IS NULL;
```

**Use Case:** Find inactive customers, products that never sold

---

### **Pattern 5: Filtering Aggregated Results**

```sql
-- GROUP BY with HAVING
SELECT 
    city,
    COUNT(*) as order_count,
    SUM(total_amount) as revenue
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY city
HAVING COUNT(*) > 10
ORDER BY revenue DESC;
```

**Key:** WHERE filters rows, HAVING filters groups

---

## 📊 SQL vs Pandas - When to Use What

### **Decision Matrix:**

| Scenario | Use SQL When... | Use Pandas When... |
|----------|----------------|-------------------|
| **Data Size** | > 1 million rows | < 1 million rows |
| **Data Location** | In database | In CSV/Excel files |
| **Initial Filtering** | Need to reduce data | Need all data |
| **Team Sharing** | Non-Python team | Python-only team |
| **Performance** | Fast filtering needed | Complex transformations |
| **Joins** | Multiple large tables | Small datasets |

### **Best Practice: Combine Both!**

```python
# 1. Use SQL to filter and aggregate (fast!)
query = '''
    SELECT customer_id, SUM(amount) as total
    FROM orders
    WHERE order_date >= '2024-01-01'
    GROUP BY customer_id
    HAVING total > 1000
'''

# 2. Load filtered data into Pandas (manageable size)
df = pd.read_sql_query(query, conn)

# 3. Use Pandas for complex analysis
df['rank'] = df['total'].rank(ascending=False)

# 4. Visualize
df.plot(kind='bar')
```

---

## 💡 Common Interview Questions

### **Question 1: "Find top 5 customers by spending"**

```sql
SELECT 
    customer_id,
    SUM(total_amount) as total_spent
FROM orders
WHERE status = 'Completed'
GROUP BY customer_id
ORDER BY total_spent DESC
LIMIT 5;
```

---

### **Question 2: "Show customers who never ordered"**

```sql
SELECT c.name, c.email
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_id IS NULL;
```

---

### **Question 3: "Calculate average order by city"**

```sql
SELECT 
    c.city,
    AVG(o.total_amount) as avg_order
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE o.status = 'Completed'
GROUP BY c.city
ORDER BY avg_order DESC;
```

**These patterns cover 80% of data analyst SQL interviews!**

---

## 📈 Skills Progression

### **Before Day 15:**
- ❌ Only worked with CSV/Excel files
- ❌ Couldn't query databases
- ❌ Limited to small datasets
- ❌ No experience joining tables

### **After Day 15:**
- ✅ Can write complex SQL queries
- ✅ Understand database relationships
- ✅ Join multiple tables confidently
- ✅ Combine SQL with Python
- ✅ Ready for SQL interview questions
- ✅ Build database-driven applications

---

## ✅ Completion Checklist

### **Core Knowledge:**
- ✅ Understand relational database concepts
- ✅ Know the 5 core SQL operations
- ✅ Master SELECT query structure
- ✅ Use all 5 aggregation functions
- ✅ Understand 4 JOIN types
- ✅ Apply WHERE vs HAVING correctly

### **Practical Skills:**
- ✅ Built complete database application
- ✅ Wrote 10+ real-world queries
- ✅ Combined SQL with Python
- ✅ Generated business reports
- ✅ Exported data for analysis

### **Interview Ready:**
- ✅ Can write queries without reference
- ✅ Explain query logic clearly
- ✅ Understand performance implications
- ✅ Know when to use SQL vs Pandas
- ✅ Solve problems independently

---

## 📁 Files in This Module

```
Day 15 - SQL Basics/
├── sales_database_analyzer.py        # Main project
├── sales_analysis.db                 # SQLite database
├── Day15_practice.py                 # With solutions
├── Day15_practice_NO_SOLUTIONS.py    # Practice version
├── SQL_cheat_sheet.py                # Quick reference
└── README.md                         # This file
```

---

## 💪 Key Takeaways

### **Why SQL Matters:**

**Statistics:**
- 70% of data analyst jobs require SQL
- #1 most requested technical skill
- Higher salary for SQL proficiency
- Essential for career growth

**The Power of SQL:**

```
Before SQL: "Can you send me the sales data?"
With SQL:   "Let me query that right now..."

Before SQL: Wait hours/days for data team
With SQL:   Get answers in seconds

Before SQL: Limited to provided exports
With SQL:   Ask any question of the data
```

---

## 🎉 Achievement Unlocked

**🏆 SQL Analyst**
- Master of SELECT queries
- JOIN expert
- Aggregation wizard
- Database-ready professional

**You can now:**
- Query production databases
- Answer business questions with data
- Build SQL-powered applications
- Compete for data analyst roles

---

*Created: February 2025*  
*Part of: 30-Day Python Data Analytics Learning Journey*  
*Repository: [GitHub - Python Learning Journey](https://github.com/Purvaja11/python-learning-journey)*
