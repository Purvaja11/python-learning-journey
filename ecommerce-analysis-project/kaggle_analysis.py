"""
E-COMMERCE DATA ANALYSIS - PORTFOLIO PROJECT
Day 13: Real Dataset Analysis

Business Objective:
Analyze customer behavior and sales patterns to provide actionable insights
for improving revenue, customer satisfaction, and operational efficiency.

Author: Purvaja Kalbande
Date: January 2026
Dataset: E-commerce Customer & Orders Data
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Set visualization style
sns.set_style('whitegrid')
sns.set_palette('husl')

print("=" * 80)
print("🎯 E-COMMERCE DATA ANALYSIS PROJECT")
print("=" * 80)


# ============================================================================
# PART 1: DATA LOADING & INITIAL EXPLORATION
# ============================================================================
print("\n📂 PART 1: LOADING DATA")
print("-" * 80)

# Load datasets
try:
    customers = pd.read_csv('ecommerce_customers.csv')
    orders = pd.read_csv('ecommerce_orders.csv')
    print("✅ Data loaded successfully!")
except FileNotFoundError:
    print("❌ Error: CSV files not found!")
    print("   Please run the dataset generator first!")
    exit()

print(f"\n📊 Dataset Shapes:")
print(f"   Customers: {customers.shape[0]} rows × {customers.shape[1]} columns")
print(f"   Orders: {orders.shape[0]} rows × {orders.shape[1]} columns")


# ============================================================================
# PART 2: EXPLORATORY DATA ANALYSIS (EDA)
# ============================================================================
print("\n" + "=" * 80)
print("🔍 PART 2: EXPLORATORY DATA ANALYSIS (EDA)")
print("=" * 80)

# 2.1: Customer Data Overview
print("\n📋 2.1: CUSTOMER DATA OVERVIEW")
print("-" * 80)
print("\nFirst 5 customers:")
print(customers.head())

print("\nData Types:")
print(customers.dtypes)

print("\nBasic Statistics:")
print(customers.describe())

print("\nMissing Values:")
print(customers.isnull().sum())

# 2.2: Orders Data Overview
print("\n" + "-" * 80)
print("📋 2.2: ORDERS DATA OVERVIEW")
print("-" * 80)
print("\nFirst 5 orders:")
print(orders.head())

print("\nData Types:")
print(orders.dtypes)

print("\nBasic Statistics:")
print(orders.describe())

print("\nMissing Values:")
print(orders.isnull().sum())


# ============================================================================
# PART 3: DATA CLEANING
# ============================================================================
print("\n" + "=" * 80)
print("🧹 PART 3: DATA CLEANING")
print("=" * 80)

# Create copies to preserve original data
customers_clean = customers.copy()
orders_clean = orders.copy()

# 3.1: Clean Customer Data
print("\n🔧 3.1: Cleaning Customer Data")
print("-" * 80)

# Handle missing ages - fill with median
median_age = customers_clean['Age'].median()
customers_clean['Age'].fillna(median_age, inplace=True)
print(f"✅ Filled {customers['Age'].isnull().sum()} missing ages with median: {median_age:.0f}")

# Handle missing cities - fill with mode (most common)
mode_city = customers_clean['City'].mode()[0]
customers_clean['City'].fillna(mode_city, inplace=True)
print(f"✅ Filled {customers['City'].isnull().sum()} missing cities with mode: {mode_city}")

# Convert date column
customers_clean['Registration_Date'] = pd.to_datetime(customers_clean['Registration_Date'])
print("✅ Converted Registration_Date to datetime")

# 3.2: Clean Orders Data
print("\n🔧 3.2: Cleaning Orders Data")
print("-" * 80)

# Convert date column
orders_clean['Order_Date'] = pd.to_datetime(orders_clean['Order_Date'])
print("✅ Converted Order_Date to datetime")

# Fix Order_Status inconsistencies (lowercase issues)
orders_clean['Order_Status'] = orders_clean['Order_Status'].str.title()
orders_clean['Order_Status'] = orders_clean['Order_Status'].replace({
    'Deliverd': 'Delivered'
})
print("✅ Standardized Order_Status values")

# Handle missing discounts - assume 0%
orders_clean['Discount_Percent'].fillna(0, inplace=True)
print(f"✅ Filled missing discounts with 0%")

# Handle missing ratings - keep as NaN (only delivered orders have ratings)
print(f"ℹ️  Keeping {orders_clean['Rating'].isnull().sum()} missing ratings (non-delivered orders)")

# Verify cleaning
print("\n✅ DATA CLEANING COMPLETE!")
print(f"   Customers missing values: {customers_clean.isnull().sum().sum()}")
print(f"   Orders missing values: {orders_clean.isnull().sum().sum()} (excluding valid NaN ratings)")


# ============================================================================
# PART 4: DATA MERGING & ENRICHMENT
# ============================================================================
print("\n" + "=" * 80)
print("🔗 PART 4: MERGING DATASETS")
print("=" * 80)

# Merge orders with customer data
df = pd.merge(orders_clean, customers_clean, on='Customer_ID', how='left')
print(f"✅ Merged datasets: {df.shape[0]} rows × {df.shape[1]} columns")

# Add calculated columns
df['Order_Year'] = df['Order_Date'].dt.year
df['Order_Month'] = df['Order_Date'].dt.month
df['Order_Month_Name'] = df['Order_Date'].dt.month_name()
df['Order_Quarter'] = df['Order_Date'].dt.quarter
df['Order_Weekday'] = df['Order_Date'].dt.day_name()

print("✅ Added time-based columns: Year, Month, Quarter, Weekday")

# Customer lifetime metrics
customer_metrics = df.groupby('Customer_ID').agg({
    'Order_ID': 'count',
    'Final_Amount': 'sum'
}).rename(columns={
    'Order_ID': 'Total_Orders',
    'Final_Amount': 'Lifetime_Value'
})

df = df.merge(customer_metrics, on='Customer_ID', how='left')
print("✅ Added customer metrics: Total_Orders, Lifetime_Value")


# ============================================================================
# PART 5: DEEP ANALYSIS & INSIGHTS
# ============================================================================
print("\n" + "=" * 80)
print("📊 PART 5: ANALYSIS & INSIGHTS")
print("=" * 80)

# 5.1: Revenue Analysis
print("\n💰 5.1: REVENUE ANALYSIS")
print("-" * 80)

total_revenue = df['Final_Amount'].sum()
total_orders = len(df)
avg_order_value = df['Final_Amount'].mean()
unique_customers = df['Customer_ID'].nunique()

print(f"Total Revenue: ₹{total_revenue:,.2f}")
print(f"Total Orders: {total_orders:,}")
print(f"Average Order Value: ₹{avg_order_value:,.2f}")
print(f"Unique Customers: {unique_customers:,}")
print(f"Avg Orders per Customer: {total_orders/unique_customers:.2f}")

# 5.2: Category Performance
print("\n📦 5.2: CATEGORY PERFORMANCE")
print("-" * 80)

category_stats = df.groupby('Category').agg({
    'Final_Amount': ['sum', 'mean', 'count'],
    'Rating': 'mean'
}).round(2)

category_stats.columns = ['Total_Revenue', 'Avg_Order_Value', 'Order_Count', 'Avg_Rating']
category_stats = category_stats.sort_values('Total_Revenue', ascending=False)

print(category_stats)

# 5.3: Customer Segmentation Analysis
print("\n👥 5.3: CUSTOMER SEGMENTATION")
print("-" * 80)

membership_stats = df.groupby('Membership_Type').agg({
    'Final_Amount': ['sum', 'mean'],
    'Customer_ID': 'nunique'
}).round(2)

membership_stats.columns = ['Total_Revenue', 'Avg_Order_Value', 'Customer_Count']
membership_stats['Avg_Revenue_Per_Customer'] = (
    membership_stats['Total_Revenue'] / membership_stats['Customer_Count']
).round(2)

print(membership_stats)

# 5.4: Time-based Analysis
print("\n📅 5.4: TIME-BASED TRENDS")
print("-" * 80)

monthly_revenue = df.groupby(['Order_Year', 'Order_Month_Name'])['Final_Amount'].sum()
print("\nMonthly Revenue Trends:")
print(monthly_revenue.head(10))

weekday_orders = df.groupby('Order_Weekday')['Order_ID'].count().sort_values(ascending=False)
print("\nOrders by Weekday:")
print(weekday_orders)

# 5.5: Top Customers
print("\n🏆 5.5: TOP 10 CUSTOMERS")
print("-" * 80)

top_customers = df.groupby('Customer_ID').agg({
    'Final_Amount': 'sum',
    'Order_ID': 'count'
}).sort_values('Final_Amount', ascending=False).head(10)

top_customers.columns = ['Total_Spent', 'Order_Count']
print(top_customers)

# 5.6: Payment Method Analysis
print("\n💳 5.6: PAYMENT METHOD ANALYSIS")
print("-" * 80)

payment_stats = df.groupby('Payment_Method').agg({
    'Order_ID': 'count',
    'Final_Amount': 'sum'
}).sort_values('Final_Amount', ascending=False)

payment_stats.columns = ['Order_Count', 'Total_Revenue']
payment_stats['Percentage'] = (payment_stats['Order_Count'] / len(df) * 100).round(2)
print(payment_stats)


# ============================================================================
# PART 6: VISUALIZATIONS
# ============================================================================
print("\n" + "=" * 80)
print("📈 PART 6: CREATING VISUALIZATIONS")
print("=" * 80)

# 6.1: Revenue by Category
print("\n📊 Creating Chart 1: Revenue by Category...")
plt.figure(figsize=(12, 6))
category_revenue = df.groupby('Category')['Final_Amount'].sum().sort_values(ascending=False)
bars = plt.bar(category_revenue.index, category_revenue.values, 
               color='skyblue', edgecolor='navy', linewidth=2)

for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, height,
            f'₹{height/100000:.1f}L',
            ha='center', va='bottom', fontsize=11, fontweight='bold')

plt.title('Total Revenue by Product Category', fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Category', fontsize=12)
plt.ylabel('Revenue (₹)', fontsize=12)
plt.xticks(rotation=45)
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('chart1_category_revenue.png', dpi=300, bbox_inches='tight')
plt.show()
print("✅ Saved: chart1_category_revenue.png")

# 6.2: Monthly Revenue Trend
print("\n📊 Creating Chart 2: Monthly Revenue Trend...")
monthly_data = df.groupby(df['Order_Date'].dt.to_period('M'))['Final_Amount'].sum()
months = [str(m) for m in monthly_data.index]

plt.figure(figsize=(14, 6))
plt.plot(months, monthly_data.values, marker='o', linewidth=2.5, 
         color='#2E86AB', markersize=8)
plt.title('Monthly Revenue Trend', fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Month', fontsize=12)
plt.ylabel('Revenue (₹)', fontsize=12)
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('chart2_monthly_trend.png', dpi=300, bbox_inches='tight')
plt.show()
print("✅ Saved: chart2_monthly_trend.png")

# 6.3: Customer Membership Distribution
print("\n📊 Creating Chart 3: Membership Distribution...")
membership_counts = customers_clean['Membership_Type'].value_counts()

plt.figure(figsize=(8, 8))
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A']
explode = (0.05, 0.05, 0.05, 0.1)  # Explode Platinum

plt.pie(membership_counts.values, labels=membership_counts.index,
        autopct='%1.1f%%', colors=colors, explode=explode,
        shadow=True, startangle=90)
plt.title('Customer Distribution by Membership Type', 
          fontsize=16, fontweight='bold', pad=20)
plt.tight_layout()
plt.savefig('chart3_membership_distribution.png', dpi=300, bbox_inches='tight')
plt.show()
print("✅ Saved: chart3_membership_distribution.png")

# 6.4: Order Status Distribution
print("\n📊 Creating Chart 4: Order Status...")
status_counts = df['Order_Status'].value_counts()

plt.figure(figsize=(10, 6))
bars = plt.barh(status_counts.index, status_counts.values, 
                color='lightcoral', edgecolor='darkred', linewidth=2)

for bar in bars:
    width = bar.get_width()
    plt.text(width, bar.get_y() + bar.get_height()/2,
            f' {width:,}',
            ha='left', va='center', fontsize=11, fontweight='bold')

plt.title('Order Status Distribution', fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Number of Orders', fontsize=12)
plt.ylabel('Status', fontsize=12)
plt.grid(axis='x', alpha=0.3)
plt.tight_layout()
plt.savefig('chart4_order_status.png', dpi=300, bbox_inches='tight')
plt.show()
print("✅ Saved: chart4_order_status.png")

# 6.5: Top 10 Cities by Revenue
print("\n📊 Creating Chart 5: Top Cities...")
city_revenue = df.groupby('City')['Final_Amount'].sum().sort_values(ascending=False).head(10)

plt.figure(figsize=(12, 6))
bars = plt.barh(city_revenue.index, city_revenue.values,
                color='#66b3ff', edgecolor='navy', linewidth=2)

for bar in bars:
    width = bar.get_width()
    plt.text(width, bar.get_y() + bar.get_height()/2,
            f' ₹{width/100000:.1f}L',
            ha='left', va='center', fontsize=10, fontweight='bold')

plt.title('Top 10 Cities by Revenue', fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Revenue (₹)', fontsize=12)
plt.ylabel('City', fontsize=12)
plt.gca().invert_yaxis()
plt.grid(axis='x', alpha=0.3)
plt.tight_layout()
plt.savefig('chart5_top_cities.png', dpi=300, bbox_inches='tight')
plt.show()
print("✅ Saved: chart5_top_cities.png")

# 6.6: Find most ordered products
print("\n📊 Creating Chart 6: Most Ordered Products...")
product_popularity = df.groupby('Product_Name').agg({
    'Order_ID': 'count',
    'Rating': 'mean',
    'Final_Amount': 'sum'
}).sort_values('Order_ID', ascending=False).head(10)
   
# Create bar chart
# YOUR CODE HERE
plt.figure(figsize=(12,6))
bars = plt.barh(product_popularity.index, product_popularity['Order_ID'], 
               color= "#034858", edgecolor='skyblue', linewidth=2)

for bar in bars:
    width = bar.get_width()
    plt.text(width, bar.get_y() + bar.get_height()/2,
             f' {int(width)}',
             ha='left', va='center', 
             fontsize=10, fontweight='bold')
    
plt.title('Most Ordered Products', fontsize=16, fontweight='bold', pad=20)
plt.xlabel('No. of Orders', fontsize=12)
plt.ylabel('Product', fontsize=12)
plt.xticks(rotation=45)
plt.grid(axis='y', alpha=0.3, linestyle='--')
plt.tight_layout()
plt.savefig('chart6_most_ordered_products.png', dpi=300, bbox_inches='tight')
plt.show()
print("✅ Saved: most_orderd_products.png")

# 6.7: Analyze if discounts increase order value
print("\n📊 Creating Chart 7: Dicounts increase...")
discount_groups = df.groupby('Discount_Percent')['Final_Amount'].mean()

# Create line chart showing relationship
# YOUR CODE HERE
plt.figure(figsize=(14,6))
plt.plot(discount_groups.index, discount_groups.values, marker='o', linewidth=2.5,
         color='#4b8be0', markersize=8)
plt.title('Relationship between Discount% & Revenue', fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Discount %', fontsize=12)
plt.ylabel('Revenue', fontsize=12)
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('chart7_relationship_discount_revenue.png', dpi=300, bbox_inches='tight')
plt.show()
print("✅ Saved: chart7_discount_vs_revenue.png")

# Create age groups
print("\n📊 Creating Chart 8: Spending by age group...")
df['Age_Group'] = pd.cut(df['Age'], bins=[0, 25, 35, 45, 60, 100],
                         labels=['18-25', '26-35', '36-45', '46-60', '60+'])
   
# 6.8: Analyze spending by age group
age_analysis = df.groupby('Age_Group')['Final_Amount'].agg(['sum', 'mean', 'count'])
colors1= ['#EAF077', '#8AF38A','#79BDED','#FF6B6B', '#A8E6CF']
# Create visualization
# YOUR CODE HERE
plt.figure(figsize=(12,6))
bars = plt.bar(age_analysis.index, age_analysis['sum'], color=colors1, edgecolor='black',
               linewidth=2, alpha=0.7)

for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2,
             height,
             f'₹{height/100000:.1f}L',
             fontsize=11, fontweight='bold')

plt.title('Total Spending by Age Group', fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Age group', fontsize=12)
plt.ylabel('Total Amount Spent', fontsize=12)
plt.grid(axis='y', alpha=0.3, linestyle='--')
plt.savefig('chart8_Spending_by_age.png', dpi=300, bbox_inches='tight')
plt.show()
print("✅ Saved: chart8_spending_by_age.png")

# 6.9: Comprehensive Dashboard
print("\n📊 Creating Chart 9: Complete Dashboard...")
fig = plt.figure(figsize=(16, 10))
gs = fig.add_gridspec(2, 3, hspace=0.3, wspace=0.3)

# Revenue by category
ax1 = fig.add_subplot(gs[0, :2])
cat_rev = df.groupby('Category')['Final_Amount'].sum().sort_values(ascending=False)
ax1.bar(cat_rev.index, cat_rev.values, color='skyblue', edgecolor='black')
ax1.set_title('Revenue by Category', fontweight='bold')
ax1.set_ylabel('Revenue (₹)')
ax1.tick_params(axis='x', rotation=45)
ax1.grid(axis='y', alpha=0.3)

# Order status pie
ax2 = fig.add_subplot(gs[0, 2])
status_counts = df['Order_Status'].value_counts().head(5)
ax2.pie(status_counts.values, labels=status_counts.index, autopct='%1.0f%%')
ax2.set_title('Order Status', fontweight='bold')

# Monthly trend
ax3 = fig.add_subplot(gs[1, :2])
monthly = df.groupby(df['Order_Date'].dt.to_period('M'))['Final_Amount'].sum()
months_short = [str(m)[:7] for m in monthly.index]
ax3.plot(months_short, monthly.values, marker='o', linewidth=2, color='#2E86AB')
ax3.set_title('Monthly Revenue Trend', fontweight='bold')
ax3.tick_params(axis='x', rotation=45)
ax3.grid(True, alpha=0.3)

# Top customers table
ax4 = fig.add_subplot(gs[1, 2])
ax4.axis('off')
top_5 = df.groupby('Customer_ID')['Final_Amount'].sum().sort_values(ascending=False).head(5)
table_data = [[f"₹{v/1000:.0f}K"] for v in top_5.values]
table = ax4.table(cellText=table_data,
                 rowLabels=[f"Cust {i+1}" for i in range(5)],
                 colLabels=['Spent'],
                 cellLoc='center',
                 loc='center')
table.auto_set_font_size(False)
table.set_fontsize(9)
table.scale(1, 2)
ax4.set_title('Top 5 Customers', fontweight='bold', pad=20)

fig.suptitle('📊 E-COMMERCE ANALYTICS DASHBOARD', 
            fontsize=18, fontweight='bold', y=0.98)

plt.savefig('chart9_complete_dashboard.png', dpi=300, bbox_inches='tight')
plt.show()
print("✅ Saved: chart9_complete_dashboard.png")


# ============================================================================
# PART 7: KEY INSIGHTS & RECOMMENDATIONS
# ============================================================================
print("\n" + "=" * 80)
print("💡 PART 7: KEY INSIGHTS & BUSINESS RECOMMENDATIONS")
print("=" * 80)

print("""
🎯 KEY FINDINGS:

1. REVENUE INSIGHTS:
   • Total Revenue: ₹{:,.2f}
   • Average Order Value: ₹{:,.2f}
   • {} category generates highest revenue
   
2. CUSTOMER BEHAVIOR:
   • {} unique customers placed {} orders
   • Average {:.2f} orders per customer
   • {} membership tier has highest customer count
   
3. OPERATIONAL INSIGHTS:
   • {:.1f}% orders successfully delivered
   • Most popular payment method: {}
   • Peak ordering day: {}
   
4. GROWTH OPPORTUNITIES:
   • Focus on {} category (highest revenue)
   • Target {} customers (high spending potential)
   • Optimize {} operations (delivery/cancellations)

📈 RECOMMENDATIONS:

1. REVENUE GROWTH:
   ✓ Promote high-margin {} products
   ✓ Upsell to Basic members → Silver/Gold tier
   ✓ Focus marketing on top-performing cities
   
2. CUSTOMER RETENTION:
   ✓ Implement loyalty programs for repeat customers
   ✓ Personalized recommendations based on purchase history
   ✓ Address reasons for {} cancelled/returned orders
   
3. OPERATIONAL EFFICIENCY:
   ✓ Improve delivery success rate (currently {:.1f}%)
   ✓ Analyze and fix reasons for order cancellations
   ✓ Optimize inventory for peak ordering days
   
4. STRATEGIC FOCUS:
   ✓ Expand presence in high-revenue cities
   ✓ Partner with popular payment providers
   ✓ Launch targeted campaigns during peak months

""".format(
    total_revenue,
    avg_order_value,
    category_stats.index[0],
    unique_customers,
    total_orders,
    total_orders/unique_customers,
    membership_stats['Customer_Count'].idxmax(),
    (df['Order_Status'] == 'Delivered').sum() / len(df) * 100,
    payment_stats.index[0],
    weekday_orders.index[0],
    category_stats.index[0],
    membership_stats.index[-1],
    status_counts.index[0],
    category_stats.index[0],
    (df['Order_Status'].isin(['Cancelled', 'Returned'])).sum(),
    (df['Order_Status'] == 'Delivered').sum() / len(df) * 100
))

print("=" * 80)
print("✅ ANALYSIS COMPLETE!")
print("=" * 80)
print("\n📁 Generated Files:")
print("   ✅ chart1_category_revenue.png")
print("   ✅ chart2_monthly_trend.png")
print("   ✅ chart3_membership_distribution.png")
print("   ✅ chart4_order_status.png")
print("   ✅ chart5_top_cities.png")
print("   ✅ chart6_complete_dashboard.png")

print("\n🎯 NEXT STEPS:")
print("   1. Review all visualizations")
print("   2. Create professional README.md")
print("   3. Commit to GitHub with detailed message")
print("   4. Practice presenting this project!")

print("\n💪 THIS IS YOUR PORTFOLIO SHOWCASE PROJECT!")
print("=" * 80)