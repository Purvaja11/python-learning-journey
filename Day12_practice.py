"""
Day 12 Practice: Data Visualization Exercises
Complete these tasks to master matplotlib and seaborn!
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

print("=" * 60)
print("DAY 12 PRACTICE: DATA VISUALIZATION")
print("=" * 60)

# ============================================================================
# EXERCISE 1: Temperature Analysis (Line Charts)
# ============================================================================
print("\n📈 EXERCISE 1: Temperature Line Charts")
print("-" * 60)

# Data: Daily temperatures for a week
days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
temp_morning = [18, 19, 17, 20, 21, 22, 20]
temp_afternoon = [28, 30, 27, 31, 32, 33, 31]
temp_evening = [22, 23, 21, 24, 25, 26, 24]

# YOUR TASK:
# 1. Create a line chart showing all three temperatures
# 2. Add markers to each line (different shapes: 'o', 's', '^')
# 3. Add title: "Weekly Temperature Variation"
# 4. Add legend with labels: "Morning", "Afternoon", "Evening"
# 5. Add grid with transparency (alpha=0.3)
# 6. Save as 'exercise1_temperature.png'

# YOUR CODE HERE:
plt.figure(figsize=(12, 6))

# Plot the lines (complete this)
plt.plot(days, temp_morning, marker='o', label = 'Morning Temp', linewidth=2, markersize=8)
plt.plot(days, temp_afternoon, marker='s', label='Afternoon Temp', linewidth=2, markersize=8)
plt.plot(days, temp_evening, marker='^', label='Evening Temp', linewidth=2, markersize=8)

# Add labels and formatting (complete this)
plt.title('Weekly Temperature Variation', fontsize=16,fontweight='bold')
plt.xlabel('Days',fontsize=12)
plt.ylabel('Temperature (°C)',fontsize=12)
plt.legend(loc='upper left', fontsize=11)
plt.grid(True, alpha=0.3, linestyle='--')

plt.tight_layout()
plt.savefig('exercise1_temperature.png', dpi=300, bbox_inches='tight')
plt.show()

print("TODO: Complete Exercise 1")


# ============================================================================
# EXERCISE 2: Sales Comparison (Bar Charts)
# ============================================================================
print("\n📊 EXERCISE 2: Sales Bar Charts")
print("-" * 60)

# Data: Quarterly sales for two years
quarters = ['Q1', 'Q2', 'Q3', 'Q4']
sales_2023 = [45000, 52000, 48000, 61000]
sales_2024 = [50000, 58000, 55000, 68000]

# YOUR TASK:
# 1. Create a GROUPED bar chart comparing 2023 vs 2024
# 2. Use different colors for each year
# 3. Add value labels on top of each bar
# 4. Title: "Quarterly Sales Comparison: 2023 vs 2024"
# 5. Add legend
# 6. Save as 'exercise2_sales.png'

# HINT: Use np.arange() for x positions and width for bar spacing

# YOUR CODE HERE:
x = np.arange(len(quarters))
width = 0.35

fig, ax =plt.subplots(figsize=(10,6))

#Create bars
bars1 = ax.bar(x - width/2, sales_2023, width, label='2023', color='skyblue', edgecolor='black')
bars2 = ax.bar(x + width/2, sales_2024, width, label='2024', color='cyan', edgecolor='black')

#Add labels to first set of bars
for bar in bars1:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, height,
            f'${height/1000:.0f}K',
            ha='center', va='bottom', fontsize=10, fontweight='bold')
    
#Add labels to second set of bars
for bar in bars2:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, height,
            f'${height/1000:.0f}K',
            ha='center', va='bottom', fontsize=10, fontweight='bold')

#Labels
ax.set_title('Quarterly Sales Comparison: 2023 vs 2024', fontsize=16, fontweight='bold')
ax.set_xlabel('Quater', fontsize=12)
ax.set_ylabel('Sales ($)',fontsize=12)
ax.set_xticks(x)
ax.set_xticklabels(quarters)
ax.legend(fontsize=11)
ax.grid(axis='y', alpha=0.3, linestyle='--')

plt.tight_layout()
plt.savefig('exercise2_sales.png', dpi=300, bbox_inches='tight')
plt.show()

print("TODO: Complete Exercise 2")


# ============================================================================
# EXERCISE 3: Customer Segmentation (Pie Chart)
# ============================================================================
print("\n🥧 EXERCISE 3: Customer Pie Chart")
print("-" * 60)

# Data: Customer segments
segments = ['New Customers', 'Returning', 'VIP', 'Inactive']
percentages = [25, 45, 20, 10]

# YOUR TASK:
# 1. Create a pie chart showing customer distribution
# 2. Explode the 'VIP' slice (0.1)
# 3. Show percentages with 1 decimal place
# 4. Use colors: ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99']
# 5. Add shadow
# 6. Title: "Customer Segmentation"
# 7. Save as 'exercise3_customers.png'

# YOUR CODE HERE:
colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99']
explode = (0,0,0.1,0)

plt.figure(figsize=(8,8))
plt.pie(percentages, explode=explode, labels=segments, colors=colors, 
        autopct='%1.1f%%', shadow=True, startangle=90)
plt.title('Customer Segmantation', fontsize=16, fontweight='bold')
plt.axis('equal') #Equal aspect ratio = circular pie

plt.tight_layout()
plt.savefig('exercise3_customers.png', dpi=300, bbox_inches='tight')
plt.show()

print("TODO: Complete Exercise 3")


# ============================================================================
# EXERCISE 4: Student Performance (Histogram)
# ============================================================================
print("\n📊 EXERCISE 4: Score Distribution Histogram")
print("-" * 60)

# Data: Test scores of 50 students
np.random.seed(42)
scores = np.random.normal(75, 12, 50).astype(int)  # Mean=75, SD=12

# YOUR TASK:
# 1. Create a histogram with 10 bins
# 2. Color: 'skyblue', edge color: 'black'
# 3. Add vertical line at mean (red, dashed, label='Mean')
# 4. Title: "Student Test Score Distribution"
# 5. X-axis: "Score", Y-axis: "Number of Students"
# 6. Add legend and grid
# 7. Save as 'exercise4_scores.png'

# HINT: Use plt.axvline() for the mean line

# YOUR CODE HERE:
plt.figure(figsize=(10,6))
plt.hist(scores, bins=10, color='skyblue', edgecolor='black', alpha=0.7)

mean_score = scores.mean()
plt.axvline(mean_score, color='red', linestyle='--', linewidth=2, label=f'Mean: {mean_score:.1f}')

plt.title('Student Test Score Distribution', fontsize=16, fontweight='bold')
plt.xlabel('Score', fontsize=12)
plt.ylabel('Number of Students', fontsize=12)
plt.legend(fontsize=11)
plt.grid(axis='y',alpha=0.3, linestyle='--')

plt.tight_layout()
plt.savefig('exercise4_scores.png', dpi=300, bbox_inches='tight')
plt.show()

print("TODO: Complete Exercise 4")


# ============================================================================
# EXERCISE 5: Price vs Demand (Scatter Plot)
# ============================================================================
print("\n🔵 EXERCISE 5: Price-Demand Scatter Plot")
print("-" * 60)

# Data: Product pricing and demand
prices = [10, 15, 20, 25, 30, 35, 40, 45, 50]
demand = [150, 135, 118, 100, 85, 70, 55, 42, 30]

# YOUR TASK:
# 1. Create a scatter plot
# 2. Points: size=150, color='red', alpha=0.6
# 3. Add a trend line (use numpy polyfit)
# 4. Title: "Price vs Demand Analysis"
# 5. X-axis: "Price ($)", Y-axis: "Demand (units)"
# 6. Add grid
# 7. Save as 'exercise5_price_demand.png'

# HINT: 
z = np.polyfit(prices, demand, 1)
p = np.poly1d(z)
plt.plot(prices, p(prices), "r--", label='Trend')

# YOUR CODE HERE:
plt.figure(figsize=(10,6))
plt.scatter(prices, demand, color='red', alpha=0.6, s=150, edgecolors='black',linewidth=1.5)

#Add trend line
z = np.polyfit(prices, demand, 1)
p = np.poly1d(z)
plt.plot(prices, p(prices), "b--", linewidth=2, label='Trend Line')

#Labels and formatting
plt.title('Price vs Demand Analysis',fontsize=16, fontweight='bold')
plt.xlabel('Price ($)', fontsize=12)
plt.ylabel('Demand (units)', fontsize=12)
plt.legend(fontsize=11)
plt.grid(True, alpha=0.3, linestyle='--')

plt.tight_layout()
plt.savefig('exercise5_price_demand.png', dpi=300, bbox_inches='tight')
plt.show()

print("TODO: Complete Exercise 5")


# ============================================================================
# EXERCISE 6: Product Performance (Multiple Subplots)
# ============================================================================
print("\n📊 EXERCISE 6: Multi-Chart Dashboard")
print("-" * 60)

# Sample product data
products_df = pd.DataFrame({
    'Product': ['A', 'B', 'C', 'D', 'E'],
    'Revenue': [45000, 38000, 52000, 31000, 47000],
    'Units_Sold': [450, 380, 520, 310, 470],
    'Avg_Price': [100, 100, 100, 100, 100]
})

# YOUR TASK:
# Create a 2x2 subplot dashboard with:
# 1. Top-left: Bar chart of Revenue by Product
# 2. Top-right: Bar chart of Units Sold by Product
# 3. Bottom-left: Pie chart of Revenue distribution
# 4. Bottom-right: Scatter plot of Revenue vs Units (color by product)
# 
# Overall title: "Product Performance Dashboard"
# Save as 'exercise6_dashboard.png'

# YOUR CODE HERE:
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# 1. Revenue by product
axes[0,0].bar(products_df['Product'], products_df['Revenue'], color='skyblue', edgecolor='black')
axes[0,0].set_title('Revenue by Product', fontsize=14, fontweight='bold')
axes[0,0].set_ylabel('Revenue ($)')
axes[0,0].grid(axis='y', alpha=0.3)

# 2. Units sold by product
axes[0,1].bar(products_df['Product'], products_df['Units_Sold'], color='lightcoral', edgecolor='black')
axes[0,1].set_title('Units Sold by Product', fontsize=14, fontweight='bold')
axes[0,1].set_ylabel('Units Sold')
axes[0,1].grid(axis='y', alpha=0.3)

# 3. Pie chart of Revenue distribution
colours_pie = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#ff99cc']
axes[1,0].pie(products_df['Revenue'], labels=products_df['Product'],
              autopct='%1.1f%%', colors=colours_pie, startangle=90)
axes[1,0].set_title('Revenue Distribution', fontsize=14, fontweight='bold')

# 4. Revenue vs units
axes[1,1].scatter(products_df['Revenue'], products_df['Units_Sold'],
                  s=200, alpha=0.6, c=range(len(products_df)), cmap='viridis',
                  edgecolors='black', linewidth=2)
for idx, row in products_df.iterrows():
    axes[1,1].annotate(row['Product'],
                       (row['Revenue'], row['Units_Sold']),
                       fontsize=11, fontweight='bold',
                       ha='center', va='center')
axes[1,1].set_title('Revenue vs Units Sold', fontsize=14, fontweight='bold')
axes[1,1].set_xlabel('Revenue ($)')
axes[1,1].set_ylabel('Units Sold')
axes[1,1].grid(True, alpha=0.3)

#Overall title
fig.suptitle('Product Performance Dashboard', fontsize=18, fontweight='bold', y=0.98)

plt.tight_layout(rect=[0,0,1,0.94])
plt.savefig('exercise6_dashboard.png', dpi=300)
plt.show()

print("TODO: Complete, Exercise 6")


# ============================================================================
# EXERCISE 7: Seaborn Heatmap (Advanced)
# ============================================================================
print("\n🔥 EXERCISE 7: Correlation Heatmap with Seaborn")
print("-" * 60)

# Sample sales data
sales_data = pd.DataFrame({
    'TV_Ads': [50, 45, 60, 55, 70, 65, 80, 75, 90],
    'Radio_Ads': [20, 25, 18, 30, 28, 35, 32, 40, 38],
    'Social_Media': [100, 110, 95, 120, 115, 130, 125, 140, 135],
    'Sales': [150, 160, 145, 175, 170, 190, 185, 205, 200]
})

# YOUR TASK:
# 1. Calculate correlation matrix: sales_data.corr()
# 2. Create seaborn heatmap with annotations (annot=True)
# 3. Use 'coolwarm' colormap
# 4. Set center=0 for better contrast
# 5. Title: "Marketing Channels Correlation"
# 6. Save as 'exercise7_heatmap.png'

# YOUR CODE HERE:
correlation = sales_data.corr()

plt.figure(figsize=(10, 8))

sns.heatmap(correlation, annot=True, cmap='coolwarm', center=0,
            fmt='.2f', linewidths=1, cbar_kws={'label': 'Correlation'},
            square=True)

plt.title('Marketing Channels Correlation', fontsize=16, fontweight='bold', pad=20)

plt.tight_layout()
plt.savefig('exercise7_heatmap.png', dpi=300, bbox_inches='tight')
plt.show()

print("TODO: Complete Exercise 7")
