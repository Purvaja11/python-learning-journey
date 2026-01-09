import numpy as np

# Challenge 1: Sales Analysis
print("="*50)
print("CHALLENGE 1: Multi-Region Sales Analysis")
print("="*50)

# 3 regions, 4 quarters, 5 products
# Create random sales data
np.random.seed(42)
sales_data = np.random.randint(1000, 5000, size=(3, 4, 5))
regions = ['North', 'South', 'East']
quarters = ['Q1', 'Q2', 'Q3', 'Q4']
products = ['Product A', 'Product B', 'Product C', 'Product D', 'Product E']
print(f"\nData Shape: {sales_data.shape}")
# Calculate:
# 1. Total sales by region
# 2. Total sales by quarter (across all regions)
# 3. Best selling product overall
# 4. Which region had best Q4?

# YOUR CODE HERE
print("Total Sales by region")
region_totals = np.sum(sales_data, axis=(1,2))
for i, region in enumerate(regions):
    print(f"{region:8s}: ${region_totals[i]:,}")
print(f"🏆 Best:{regions[np.argmax(region_totals)]}")

print("\nTotal Sales by Quater")
quarter_totals = np.sum(sales_data, axis=(0, 2))
for i, quarter in enumerate(quarters):
    print(f"{quarter}: ${quarter_totals[i]:,}")
print(f"📈 Best: {quarters[np.argmax(quarter_totals)]}")

print("\nBest Selling Product")
product_totals = np.sum(sales_data, axis=(0,1))
for i, product in enumerate(products):
    print(f"{product}: ${product_totals[i]:,}")
print(f"⭐ Best: {products[np.argmax(product_totals)]}")

print("\nBest Region in Q4")
q4_totals = np.sum(sales_data[:, 3, :], axis=1)
for i, region in enumerate(regions):
    print(f"{region:8s}: ${q4_totals[i]:,}")
print(f"🎯 Best Q4: {regions[np.argmax(q4_totals)]}")


# Challenge 2: Grade Normalization
print("\n" + "="*50)
print("CHALLENGE 2: Grade Normalization")
print("="*50)

# Original grades (different scales)
math_grades = np.array([85, 90, 78, 92, 88])      # Out of 100
science_grades = np.array([42, 48, 39, 46, 44])   # Out of 50
english_grades = np.array([170, 190, 160, 185, 175])  # Out of 200

# Normalize all to 0-100 scale
# Formula: (score / max_score) * 100

# YOUR CODE HERE
print("\n📚 ORIGINAL GRADES:")
print("="*50)
print(f"Math (out of 100):    {math_grades}")
print(f"Science (out of 50):  {science_grades}")
print(f"English (out of 200): {english_grades}")

#normalize
math_norm = math_grades
science_norm = (science_grades/50)*100
english_norm = (english_grades/200)*100

print("\n✅ NORMALIZED (0-100 scale):")
print("="*50)
print(f"Math:    {math_norm}")
print(f"Science: {science_norm}")
print(f"English: {english_norm}")

#student averages
all_grades = np.vstack([math_norm, science_norm, english_norm])
student_avg = np.mean(all_grades, axis=0)

print("\n🎓 STUDENT AVERAGES:")
print("="*50)
for i in range(5):
    print(f"Student {i+1}: {student_avg[i]:.2f}")
print(f"🏆 Top: Student {np.argmax(student_avg)+1} ({student_avg[np.argmax(student_avg)]:.2f})")


# Challenge 3: Data Cleaning
print("\n" + "="*50)
print("CHALLENGE 3: Clean Messy Data")
print("="*50)

# Data with outliers and missing values (represented as -999)
data = np.array([23, 45, 67, -999, 89, 34, 300, 56, 78, -999, 12])

# Tasks:
# 1. Replace -999 with median of valid values
# 2. Remove outliers (values > 200)
# 3. Calculate mean and std of cleaned data

# YOUR CODE HERE
print(f"Original: {data}")
print(f"Count: {len(data)}")

#identify issues
print("\n🔍 Issues:")
print(f" Missing (-999): {np.sum(data == -999)}")
print(f" Outliers (>200): {np.sum(data > 200)}")


valid = data[data != -999]
median = np.median(valid)
data_clean = np.where(data == -999, median, data)
data_clean = data_clean[data_clean <= 200]

print(f"\n✅ Cleaned: {data_clean}")
print(f"Count: {len(data_clean)}")

print("\n STATISTICS")
print("="*50)
print(f"Mean:      {np.mean(data_clean):.2f}")
print(f"Median:    {np.median(data_clean):.2f}")
print(f"Std Dev:   {np.std(data_clean):.2f}")
print(f"Range:     {np.min(data_clean):.2f} - {np.max(data_clean):.2f}")

