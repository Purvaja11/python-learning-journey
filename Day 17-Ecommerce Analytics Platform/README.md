# 🛒 E-Commerce Analytics Platform

**Day 17 of 30-Day Learning Journey**  
**Type:** End-to-End Portfolio Project  
**Difficulty:** Advanced  
**Skills Used:** Python, Pandas, NumPy, SQLite, SQL, Matplotlib, Seaborn, openpyxl

---

## 📌 Project Overview

A complete, production-ready analytics platform that simulates real-world e-commerce data analysis. This project combines every skill learned in the first 16 days into a single, professional application — the kind of project that gets you hired.

The platform handles the **full analytics lifecycle**:

```
Raw Data → Cleaning → Database → Analytics → Visualizations → Reports
```

---

## 🎯 What This Project Demonstrates

| Skill | Implementation |
|-------|---------------|
| Python OOP | Full class-based architecture |
| Data Generation | Realistic synthetic data (200 customers, 50 products, 1000 orders) |
| Data Cleaning | Validation, deduplication, integrity checks |
| SQL (Advanced) | CTEs, Window Functions, JOINs, Aggregations |
| RFM Analysis | Professional customer segmentation |
| Cohort Analysis | Customer behavior by acquisition month |
| Visualization | Matplotlib + Seaborn professional charts |
| Excel Automation | Multi-sheet reports via openpyxl |
| File Management | Automated folder creation and exports |

---

## 🏗️ System Architecture

```
EcommerceAnalyticsPlatform
│
├── PART 1: Data Generation
│   └── Realistic customers, products, orders
│
├── PART 2: Data Cleaning & Validation
│   ├── Duplicate detection
│   ├── Missing value handling
│   ├── Price/margin validation
│   └── Referential integrity checks
│
├── PART 3: Database Schema Creation
│   ├── Normalized tables (3NF)
│   ├── Constraints & foreign keys
│   └── Performance indexes
│
├── PART 4: Data Loading
│   └── Validated data → SQLite database
│
├── PART 5: Advanced Analytics
│   ├── RFM Customer Segmentation
│   ├── Cohort Analysis
│   ├── Product Performance + Profitability
│   └── Executive KPI Summary
│
├── PART 6: Visualizations
│   ├── Revenue by Category (Bar chart)
│   └── Monthly Revenue Trend (Dual-axis line+bar)
│
└── PART 7: Excel Reporting
    ├── Executive Summary sheet
    └── Top Customers sheet
```

---

## 📊 Analytics Features

### 1. RFM Customer Segmentation

RFM stands for **Recency, Frequency, Monetary** — an industry-standard technique for understanding customer behavior.

| Segment | Definition |
|---------|-----------|
| **Champions** | Bought recently, buy often, spend the most |
| **Loyal** | Regular buyers with solid spending |
| **Potential** | Recent buyers with growth potential |
| **At Risk** | Haven't bought recently, but historically valuable |
| **Lost** | No purchases in 180+ days |
| **New/Low Value** | Few purchases, low spend |

**Business Value:** Enables targeted marketing campaigns — e.g., send re-engagement offers to "At Risk", reward "Champions" with VIP perks.

---

### 2. Cohort Analysis

Groups customers by their **first purchase month** and tracks their collective behavior over time.

**Output Metrics Per Cohort:**
- Number of customers acquired
- Total orders generated
- Total revenue contributed
- Average order value
- Revenue per customer (LTV proxy)

**Business Value:** Identifies which acquisition periods brought the most valuable customers, helping optimize marketing spend.

---

### 3. Product Performance Analysis

Tracks every product's contribution to the business:
- Units sold
- Gross revenue
- Discounts given
- Net revenue
- **Profit** (revenue minus cost)
- Profit margin %

**Business Value:** Identifies which products to promote, discount, or discontinue.

---

### 4. Executive KPI Dashboard

Single-query summary of the entire business:
- Total vs. active customers
- Total vs. completed orders
- Gross revenue, discounts, net revenue
- Average order value
- Revenue per customer

---

## 💻 Database Schema

```sql
customers
├── customer_id  INTEGER  PRIMARY KEY
├── name         TEXT     NOT NULL
├── email        TEXT     UNIQUE
├── city         TEXT
├── customer_type TEXT    (Regular / Premium / VIP)
└── join_date    DATE

products
├── product_id    INTEGER  PRIMARY KEY
├── product_name  TEXT     NOT NULL
├── category      TEXT
├── price         DECIMAL  CHECK >= 0
├── cost          DECIMAL  CHECK >= 0
└── stock_quantity INTEGER

orders
├── order_id         INTEGER  PRIMARY KEY
├── customer_id      INTEGER  FOREIGN KEY → customers
├── product_id       INTEGER  FOREIGN KEY → products
├── quantity         INTEGER  CHECK > 0
├── order_date       DATE
├── subtotal         DECIMAL
├── discount_percent DECIMAL
├── discount_amount  DECIMAL
├── total_amount     DECIMAL
└── status           TEXT     (Completed / Pending / Cancelled / Returned)
```

---

## 🚀 How to Run

### 1. Install Dependencies

```bash
pip install pandas numpy matplotlib seaborn openpyxl
```

### 2. Run the Platform

```bash
python ecommerce_analytics_platform.py
```

### 3. Follow the prompts

Press **Enter** to step through each section:
- Data generation
- Cleaning & validation
- Database creation
- RFM Analysis
- Cohort Analysis
- Product Performance
- Executive Summary
- Visualizations
- Excel Report

---

## 📁 Output Files

All outputs are automatically created when the script runs:

```
Day 17-Ecommerce Analytics Platform/
│
├── ecommerce_analytics.db          ← SQLite database
│
├── analytics_charts/
│   ├── revenue_by_category.png     ← Bar chart
│   └── monthly_trends.png          ← Dual-axis trend chart
│
├── analytics_reports/
│   └── Analytics_Report_YYYYMMDD.xlsx  ← Multi-sheet Excel report
│
└── exported_data/
    ├── rfm_analysis.csv            ← Customer segments
    ├── cohort_analysis.csv         ← Cohort metrics
    └── product_performance.csv     ← Product profitability
```

---

## 🧠 Key Concepts Applied

### Data Validation Pattern
```python
# Check → Report → Fix
duplicates = df['email'].duplicated().sum()
if duplicates > 0:
    issues_found.append(f"Found {duplicates} duplicates")
    df = df.drop_duplicates(subset=['email'])
```

### RFM SQL Pattern (CTE + CASE)
```sql
WITH customer_metrics AS (
    SELECT customer_id,
           MAX(order_date) as last_order,
           COUNT(*) as frequency,
           SUM(total_amount) as monetary
    FROM orders
    GROUP BY customer_id
)
SELECT *,
    CASE
        WHEN recency <= 30 AND frequency >= 5 THEN 'Champions'
        WHEN recency <= 60 AND frequency >= 3 THEN 'Loyal'
        ELSE 'Others'
    END as segment
FROM customer_metrics;
```

### Professional Visualization Pattern
```python
# Seaborn v0.13+ requires hue for palette
sns.barplot(data=df, x='category', y='revenue',
            hue='category', palette='viridis', legend=False)
```

---

## 📈 Skills Progression

### Before This Project:
- ❌ Skills existed in isolation
- ❌ Only small, single-purpose scripts
- ❌ No end-to-end thinking

### After This Project:
- ✅ All skills integrated into one system
- ✅ Production-ready code architecture
- ✅ Full analytics lifecycle understanding
- ✅ Professional output deliverables
- ✅ Portfolio-ready project

---

## 💼 Resume / Portfolio Value

**What this project proves to an employer:**

- Can build complete data pipelines (not just pieces)
- Writes clean, maintainable, documented code
- Understands database design and SQL
- Applies real analytical frameworks (RFM, Cohort)
- Delivers professional outputs (Excel, charts, CSV)
- Self-directed learner who builds real things

---

## 🔧 Possible Extensions

Want to take this further? Here are ideas:

- **Add a dashboard** using Streamlit or Dash
- **Schedule automation** using Windows Task Scheduler or cron
- **Add email delivery** of reports using smtplib
- **Connect to real data** from Kaggle e-commerce datasets
- **Add ML** for churn prediction or sales forecasting
- **Add more charts** — heatmaps, scatter plots, funnel charts

---

## ✅ Completion Checklist

- ✅ Data generation with realistic distributions
- ✅ Production-ready data validation
- ✅ Normalized database with constraints
- ✅ RFM customer segmentation
- ✅ Cohort analysis
- ✅ Product profitability analysis
- ✅ Executive KPI dashboard
- ✅ Professional visualizations
- ✅ Automated Excel reporting
- ✅ Clean OOP architecture
- ✅ Documented code

---

## 🎉 Achievement Unlocked

**🏆 Full-Stack Data Analyst**

This project demonstrates the complete skill set of a junior-to-mid data analyst:
- Data engineering (ingestion, cleaning, storage)
- Data analysis (SQL, Python, statistics)
- Data presentation (charts, Excel, dashboards)

---

*Created: February 2026*  
*Part of: 30-Day Python Data Analytics Learning Journey*  
*Repository: [GitHub - Python Learning Journey](https://github.com/Purvaja11/python-learning-journey)*