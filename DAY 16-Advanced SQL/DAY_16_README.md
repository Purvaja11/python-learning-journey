# 🚀 DAY 16: Advanced SQL + File Automation

**Date:** Day 16 of 30-Day Learning Journey  
**Topic:** Advanced SQL Techniques + Python File Automation  
**Focus:** Production-ready skills for senior data analyst roles

---

## 🎯 Learning Objectives

Today's focus was on mastering advanced SQL techniques and file automation - skills that separate junior from senior analysts:

✅ Window functions (ROW_NUMBER, RANK, DENSE_RANK, LAG)  
✅ Common Table Expressions (CTEs) for readable queries  
✅ CASE statements for conditional logic  
✅ Advanced date manipulation and time series analysis  
✅ Cohort analysis and customer segmentation  
✅ Excel automation with Python (openpyxl)  
✅ Automated report generation from SQL queries  
✅ Combining SQL + Excel + CSV workflows  

---

## 📚 Core Concepts Covered

### **1. Window Functions (Game Changer!)**

**What are Window Functions?**
- Perform calculations across rows related to current row
- Don't collapse rows like GROUP BY does
- Keep all original data + add calculated columns
- Essential for rankings, running totals, and comparisons

**The Main Window Functions:**

```sql
ROW_NUMBER()   -- Assigns unique sequential numbers (1, 2, 3, 4...)
RANK()         -- Same value gets same rank, skips next (1, 2, 2, 4...)
DENSE_RANK()   -- Same value gets same rank, no skip (1, 2, 2, 3...)
LAG()          -- Access previous row's value
LEAD()         -- Access next row's value
```

**Time Complexity:** O(n log n) - requires sorting

---

### **2. Window Function Syntax**

```sql
function_name() OVER (
    PARTITION BY column1, column2    -- Split into groups (optional)
    ORDER BY column3                  -- Define sequence (required)
    ROWS/RANGE ...                    -- Window frame (optional)
)
```

**Key Concepts:**
- **PARTITION BY** - Like GROUP BY but doesn't collapse rows
- **ORDER BY** - Defines the sequence for calculations
- **OVER()** - Defines the window specification

---

### **3. Common Table Expressions (CTEs)**

**What are CTEs?**
- Temporary named result sets
- Make complex queries readable and maintainable
- Can be referenced multiple times
- Better than nested subqueries for clarity

**Syntax:**
```sql
WITH cte_name AS (
    -- Your query here
    SELECT ...
)
SELECT * FROM cte_name;
```

**Multiple CTEs:**
```sql
WITH 
cte1 AS (SELECT ...),
cte2 AS (SELECT ... FROM cte1),
cte3 AS (SELECT ... FROM cte2)
SELECT * FROM cte3;
```

**Benefits:**
- Improves query readability
- Makes debugging easier
- Enables step-by-step query building
- Can reference earlier CTEs

---

### **4. CASE Statements**

**SQL's if-else Logic:**

```sql
CASE
    WHEN condition1 THEN result1
    WHEN condition2 THEN result2
    ELSE default_result
END
```

**Uses:**
- Creating categories/segments
- Conditional aggregations (pivot-style)
- Dynamic column values
- Business rule implementation

---

## 💻 Projects Built

### **1. Advanced SQL Analyzer**

Complete implementation of 10 advanced SQL patterns used in professional data analysis.

**Patterns Implemented:**

1. **ROW_NUMBER()** - Sequential numbering within groups
2. **RANK()** - Ranking with ties
3. **Top N per Group** - The interview favorite pattern!
4. **Running Totals** - Cumulative sums over time
5. **Multiple CTEs** - Complex chained queries
6. **LAG() Function** - Month-over-month growth calculations
7. **CASE Segmentation** - Customer tier classification
8. **CASE Pivot** - Status breakdown aggregations
9. **Advanced Date Analysis** - Day-of-week patterns
10. **Cohort Analysis** - Customer behavior by acquisition month

**Each Pattern Includes:**
- Complete working SQL query
- Business context explanation
- Results display and validation
- Performance considerations

---

### **2. SQL Practice Suite**

**Two Versions:**

**Without Solutions** (`Day16_practice_NO_SOLUTIONS.py`):
- 10 advanced exercises
- TODO sections for writing queries
- Commented test code
- Forces independent problem-solving
- Better for learning and interview prep

**With Solutions** (`Day16_practice_WITH_SOLUTIONS.py`):
- Complete solutions to all 10 exercises
- Explanations of approach
- Alternative solutions where applicable
- 5 bonus challenges
- Learning tips and patterns

**Exercise Coverage:**
- Window functions (basics to advanced)
- CTEs (single and multiple)
- CASE statements
- Date manipulation
- Cohort analysis

---

### **3. Excel Automation System**

Professional report generation combining SQL with Excel.

**Features:**

**Multi-Sheet Reports:**
- Executive Summary (KPIs)
- Top Customers Analysis
- Product Performance Metrics
- City-wise Sales Breakdown
- Monthly Trends Analysis

**Professional Formatting:**
- Header styling (colors, fonts, alignment)
- Auto-adjusted column widths
- Cell borders and formatting
- Number formatting for currency
- Conditional formatting ready

**Chart Generation:**
- Bar charts for product comparisons
- Line charts for time trends
- Automated chart placement
- Professional styling

**Data Export:**
- Complete orders (all details)
- Customer summaries
- Product performance metrics
- CSV format for further analysis
- Organized folder structure

---

## 🎓 Key Patterns Mastered

### **Pattern 1: Top N Per Group (CRITICAL!)**

**Problem:** Find top 3 products in each category

```sql
WITH ranked_products AS (
    SELECT 
        category,
        product_name,
        revenue,
        ROW_NUMBER() OVER (
            PARTITION BY category 
            ORDER BY revenue DESC
        ) as rank
    FROM product_sales
)
SELECT *
FROM ranked_products
WHERE rank <= 3;
```

**Why It's Critical:**
- Asked in 50%+ of SQL interviews
- Tests understanding of window functions
- Real-world business need
- Can't be done easily with GROUP BY alone

---

### **Pattern 2: Running Total**

**Problem:** Calculate cumulative revenue over time

```sql
SELECT 
    date,
    daily_revenue,
    SUM(daily_revenue) OVER (
        ORDER BY date 
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) as running_total
FROM daily_sales;
```

**Use Cases:**
- Financial reporting
- Inventory tracking
- Goal progress monitoring

---

### **Pattern 3: Month-over-Month Growth**

**Problem:** Calculate percentage change from previous month

```sql
WITH monthly_revenue AS (
    SELECT 
        month,
        SUM(revenue) as revenue,
        LAG(SUM(revenue)) OVER (ORDER BY month) as prev_month
    FROM sales
    GROUP BY month
)
SELECT 
    month,
    revenue,
    prev_month,
    (revenue - prev_month) / prev_month * 100 as growth_pct
FROM monthly_revenue;
```

**Use Cases:**
- Business performance tracking
- Trend analysis
- Executive dashboards

---

### **Pattern 4: Customer Segmentation**

**Problem:** Classify customers by spending behavior

```sql
SELECT 
    customer_id,
    total_spent,
    CASE
        WHEN total_spent > 10000 THEN 'VIP'
        WHEN total_spent > 5000 THEN 'Premium'
        WHEN total_spent > 1000 THEN 'Regular'
        ELSE 'New'
    END as segment
FROM customer_totals;
```

**Use Cases:**
- Marketing campaigns
- Personalized offers
- Resource allocation

---

### **Pattern 5: Cohort Analysis**

**Problem:** Analyze customers by acquisition month

```sql
WITH customer_cohorts AS (
    SELECT 
        customer_id,
        DATE_TRUNC('month', MIN(order_date)) as cohort_month
    FROM orders
    GROUP BY customer_id
)
SELECT 
    cohort_month,
    COUNT(DISTINCT customer_id) as customers,
    SUM(revenue) as total_revenue,
    AVG(revenue) as avg_revenue_per_customer
FROM customer_cohorts
JOIN orders USING (customer_id)
GROUP BY cohort_month;
```

**Use Cases:**
- Customer retention analysis
- LTV (Lifetime Value) calculations
- Marketing ROI tracking

---

## 📊 Window Functions vs GROUP BY

### **Decision Matrix:**

| Need | Use GROUP BY | Use Window Functions |
|------|-------------|---------------------|
| **Aggregate data** | ✅ Yes | ❌ No |
| **Reduce rows** | ✅ Yes | ❌ No |
| **Keep all rows** | ❌ No | ✅ Yes |
| **Add calculations** | Limited | ✅ Yes |
| **Rankings** | ❌ No | ✅ Yes |
| **Running totals** | ❌ No | ✅ Yes |
| **Compare to prev row** | ❌ No | ✅ Yes |

**Example:**

```sql
-- GROUP BY (collapses to 3 rows - one per category)
SELECT category, SUM(sales) as total_sales
FROM products
GROUP BY category;

-- Window Function (keeps all rows, adds column)
SELECT 
    product_name,
    category,
    sales,
    SUM(sales) OVER (PARTITION BY category) as category_total
FROM products;
```

---

## 🔥 Excel Automation Workflow

### **Real-World Process:**

```
1. Query Database (SQL)
   ↓
2. Load into Pandas
   ↓
3. Transform/Calculate
   ↓
4. Export to Excel (openpyxl)
   ↓
5. Apply Formatting
   ↓
6. Add Charts
   ↓
7. Save & Share
```

### **Code Example:**

```python
import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill

# 1. Query database
query = "SELECT * FROM sales WHERE date >= '2024-01-01'"
df = pd.read_sql_query(query, conn)

# 2. Export to Excel
df.to_excel('report.xlsx', index=False)

# 3. Format Excel
wb = load_workbook('report.xlsx')
ws = wb.active

# Format headers
header_font = Font(bold=True, color="FFFFFF")
header_fill = PatternFill(start_color="4472C4", fill_type="solid")

for cell in ws[1]:
    cell.font = header_font
    cell.fill = header_fill

wb.save('report.xlsx')
```

---

## 🎯 Time Complexity Analysis

| Operation | Time Complexity | Notes |
|-----------|----------------|-------|
| Window Function | O(n log n) | Sorting required |
| ROW_NUMBER() | O(n log n) | Per partition |
| RANK() | O(n log n) | Same as ROW_NUMBER |
| LAG/LEAD | O(n) | Sequential access |
| Running Total | O(n²) worst | O(n) with optimization |
| CTEs | Same as query | Just syntactic sugar |
| CASE | O(1) per row | Simple evaluation |

**Optimization Tips:**
- Add indexes on PARTITION BY columns
- Add indexes on ORDER BY columns
- Limit partitions when possible
- Use appropriate window frames

---

## 💡 Common Interview Questions

### **Question 1: "Find top 3 employees by salary in each department"**

```sql
WITH ranked_employees AS (
    SELECT 
        department,
        employee_name,
        salary,
        ROW_NUMBER() OVER (
            PARTITION BY department 
            ORDER BY salary DESC
        ) as rank
    FROM employees
)
SELECT department, employee_name, salary
FROM ranked_employees
WHERE rank <= 3;
```

---

### **Question 2: "Calculate 30-day moving average of sales"**

```sql
SELECT 
    date,
    sales,
    AVG(sales) OVER (
        ORDER BY date 
        ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
    ) as moving_avg_30d
FROM daily_sales;
```

---

### **Question 3: "Show year-over-year growth by product"**

```sql
WITH yearly_sales AS (
    SELECT 
        product,
        YEAR(date) as year,
        SUM(sales) as total_sales,
        LAG(SUM(sales)) OVER (
            PARTITION BY product 
            ORDER BY YEAR(date)
        ) as prev_year_sales
    FROM sales
    GROUP BY product, YEAR(date)
)
SELECT 
    product,
    year,
    total_sales,
    (total_sales - prev_year_sales) / prev_year_sales * 100 as yoy_growth
FROM yearly_sales;
```

---

## 📈 Skills Progression

### **Before Day 16:**
- ❌ Only basic SQL (SELECT, WHERE, JOIN, GROUP BY)
- ❌ No window functions knowledge
- ❌ Nested subqueries (hard to read)
- ❌ Manual Excel work
- ❌ Limited to simple aggregations

### **After Day 16:**
- ✅ Advanced SQL patterns mastered
- ✅ Window functions expert
- ✅ Clean queries with CTEs
- ✅ Automated Excel reports
- ✅ Professional-grade analytics
- ✅ Senior-level SQL skills

---

## ✅ Completion Checklist

### **Core Knowledge:**
- ✅ Understand window functions vs GROUP BY
- ✅ Use ROW_NUMBER, RANK, DENSE_RANK correctly
- ✅ Write CTEs for complex queries
- ✅ Apply CASE for business logic
- ✅ Use LAG/LEAD for comparisons
- ✅ Master "top N per group" pattern

### **Practical Skills:**
- ✅ Built advanced SQL analyzer
- ✅ Solved 10+ advanced SQL problems
- ✅ Automated Excel report generation
- ✅ Combined SQL + Python + Excel
- ✅ Created professional formatted reports

### **Interview Ready:**
- ✅ Explain window functions clearly
- ✅ Solve "top N per group" in < 5 minutes
- ✅ Write growth calculations
- ✅ Perform cohort analysis
- ✅ Demonstrate automation skills

---

## 📁 Files in This Module

```
Day 16 - Advanced SQL/
├── advanced_sql_analyzer.py           # Main project
├── Day16_practice_NO_SOLUTIONS.py     # Practice exercises
├── Day16_practice_WITH_SOLUTIONS.py   # Solutions & explanations
├── excel_automation.py                # Report automation
├── sales_analysis.db                  # Database (from Day 15)
└── (generated files):
    ├── Sales_Summary_Report.xlsx
    ├── Advanced_Sales_Report.xlsx
    └── exported_data/
        ├── complete_orders.csv
        ├── customer_summary.csv
        └── product_performance.csv
```

---

## 💪 Key Takeaways

### **Why Advanced SQL Matters:**

**Career Impact:**
- 80% of senior analyst roles require window functions
- Average 15-20% salary increase for advanced SQL skills
- Differentiates you from junior candidates
- Opens doors to lead/senior positions

**Professional Benefits:**
- Write cleaner, more maintainable queries
- Solve complex business problems efficiently
- Impress technical interviewers
- Deliver insights faster

---

### **The Power of Automation:**

```
Before Automation:
- Manual Excel work: 2-3 hours/week
- Prone to human errors
- Hard to reproduce
- Doesn't scale

After Automation:
- One-click reports: < 5 minutes
- Consistent, error-free
- Easily reproducible
- Scales to any data size
```

---

## 🎉 Achievement Unlocked

**🏆 Advanced SQL Expert**
- Master of window functions
- CTE wizard
- Automation specialist
- Senior-level skills

**You can now:**
- Solve complex analytical problems
- Write production-quality SQL
- Automate reporting workflows
- Interview for senior analyst roles
- Teach others SQL

---

## 🚀 Real-World Applications

### **Where These Skills Are Used:**

**1. Business Intelligence**
- Executive dashboards
- KPI tracking
- Trend analysis
- Forecasting

**2. Data Analytics**
- Customer segmentation
- Cohort analysis
- Retention studies
- A/B test analysis

**3. Reporting Automation**
- Weekly sales reports
- Monthly performance reviews
- Quarterly board presentations
- Daily operational metrics

**4. Financial Analysis**
- Revenue forecasting
- Budget tracking
- Variance analysis
- Performance attribution

---

## 📚 Advanced Concepts Learned

### **1. Window Frame Specifications**

```sql
-- Different window frames
ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW  -- From start to current
ROWS BETWEEN 3 PRECEDING AND 3 FOLLOWING           -- 7-row window
RANGE BETWEEN INTERVAL '1' MONTH PRECEDING AND CURRENT ROW
```

### **2. LAG and LEAD Functions**

```sql
-- Access previous row
LAG(column, 1) OVER (ORDER BY date) as previous_value

-- Access next row
LEAD(column, 1) OVER (ORDER BY date) as next_value

-- With default value
LAG(column, 1, 0) OVER (ORDER BY date)
```

### **3. Advanced CASE Usage**

```sql
-- Nested CASE
CASE 
    WHEN category = 'Premium' THEN
        CASE 
            WHEN amount > 1000 THEN 'High Premium'
            ELSE 'Regular Premium'
        END
    ELSE 'Standard'
END

-- CASE in aggregations
SUM(CASE WHEN status = 'Completed' THEN amount ELSE 0 END) as completed_revenue
```

---

## 🎓 Interview Preparation

### **What Interviewers Test:**

**Technical Depth:**
1. Do you understand PARTITION BY vs GROUP BY?
2. Can you choose right window function?
3. Do you know when to use CTEs?
4. Can you optimize slow queries?

**Problem-Solving:**
1. Can you break down complex requirements?
2. Do you build queries incrementally?
3. Can you debug efficiently?
4. Do you validate results?

**Communication:**
1. Can you explain window functions simply?
2. Do you discuss trade-offs?
3. Can you justify your approach?
4. Do you think about performance?

---

### **Practice Recommendations:**

**Daily Practice (Next 2 weeks):**
- Solve 2-3 window function problems
- Practice "top N per group" variations
- Write growth calculations from memory
- Explain queries out loud

**Interview Simulation:**
- Time yourself on each problem
- Aim for < 10 minutes per query
- Practice whiteboarding SQL
- Record yourself explaining solutions

---

## 📊 Portfolio Highlight

**For Resume/LinkedIn:**

```
✅ Advanced SQL Analytics
   - Window functions (ROW_NUMBER, RANK, LAG/LEAD)
   - Complex CTEs for readable queries
   - Cohort analysis and customer segmentation
   - Query optimization and performance tuning

✅ Automation & Reporting
   - Automated Excel report generation (Python + openpyxl)
   - Multi-sheet formatted reports with charts
   - SQL-to-Excel data pipelines
   - Reduced manual reporting time by 90%

✅ Projects
   - Advanced SQL Analyzer: 10 production-ready analytical patterns
   - Excel Automation System: Automated weekly reporting
   - Data Export Pipeline: Organized CSV exports for analysis
```

---

## 🎯 Next Steps

### **Immediate Practice:**
1. Complete all 10 exercises independently
2. Solve 5 LeetCode SQL Medium problems
3. Practice explaining window functions
4. Build your own automated report

### **Day 17: Portfolio Projects**
Combining all skills to build complete analytics applications

### **Long-term Goals:**
- Master advanced window functions (NTILE, FIRST_VALUE, LAST_VALUE)
- Learn query optimization techniques
- Build real-time dashboards
- Contribute to open-source analytics tools

---

*Created: February 2026*  
*Part of: 30-Day Python Data Analytics Learning Journey*  
*Repository: [GitHub - Python Learning Journey](https://github.com/Purvaja11/python-learning-journey)*

**Next:** Day 17 - Building Complete Analytics Applications
