import pandas as pd
from datetime import datetime
# Create sample data
students = pd.DataFrame({
    'Student_ID': [1, 2, 3, 4, 5],
    'Name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve'],
    'Class': ['10A', '10B', '10A', '10B', '10A']
})

grades = pd.DataFrame({
    'Student_ID': [1, 2, 3, 4, 6],  # Note: Student 6 doesn't exist!
    'Math': [85, 90, 78, 92, 88],
    'Science': [88, 85, 92, 89, 90]
})

# EXERCISE 1: Merging
# 1. Inner join - only matching students
# 2. Left join - all students, even without grades
# 3. Right join - all grades, even without student info
# YOUR CODE HERE
print("\n" + "="*70)
print("Exercise 1: Merging")
print("="*70)
merged_inner = pd.merge(students, grades, on='Student_ID', how='inner')
merged_left = pd.merge(students, grades, on='Student_ID', how='left')
merged_right = pd.merge(students, grades, on='Student_ID', how='right')
print("\n1. INNER JOIN (only matching students):")
print(merged_inner)
print("\n2. LEFT JOIN (all students, even without grades):")
print(merged_left)
print("\n3. RIGHT JOIN (All 5 students, Eve has NaN for grades):")
print(merged_right)
print(f"Rows: {len(merged_right)} (All 5 grade records, Student 6 has NaN for name/class)")

# EXERCISE 2: Date Analysis
print("\n" + "="*70)
print("Exercise 2: Date Analysis")
print("="*70)
orders = pd.DataFrame({
    'Order_ID': range(1, 11),
    'Date': pd.date_range('2024-01-01', periods=10, freq='D'),
    'Amount': [100, 150, 200, 180, 220, 190, 210, 170, 160, 230]
})
orders['Date'] = pd.to_datetime(orders['Date'])

# Extract: year, month, day, weekday
# Group by weekday and calculate average
# YOUR CODE HERE
orders['Year'] = orders['Date'].dt.year
orders['Month'] = orders['Date'].dt.month
orders['Day'] = orders['Date'].dt.day
orders['Weekday'] = orders['Date'].dt.day_name()
print("\nOrders with date components:")
print(orders)
print("\n"+"="*70)
print("Average Amount by Weekday:")
weekday_sales = orders.groupby('Weekday')['Amount'].mean()

#Reorder by actual weekday order
weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday',
                 'Friday', 'Saturday', 'Sunday']
weekday_sales = weekday_sales.reindex(weekday_order)

print(weekday_sales)

#Additional analysis
print("\n"+"="*70)
print("Additional Date Analysis:")
print(f"Total Revenue: ₹{orders['Amount'].sum():,}")
print(f"Average Daily: ₹{orders['Amount'].mean():.0f}")
print(f"Best Day: {orders.loc[orders['Amount'].idxmax(), 'Weekday']} (₹{orders['Amount'].max()})")

# EXERCISE 3: Pivot Table
# Create pivot showing average grades by Class
# YOUR CODE HERE
print("\n" + "="*70)
print("Exercise 3: Pivot Table")
print("="*70)
#Method 1: Simple pivot (average grades by class)
print("\nMethod 1: Average grades by class:")
pivot1 = merged_left.pivot_table(
    values=['Math','Science'],
    index='Class',
    aggfunc='mean'
)
print(pivot1)

# Method 2: Reshape and pivot (better for visualization)
print("\n" + "-"*70)
print("Method 2: Reshaped pivot table:")

# First, melt the data (wide to long format)
melted = merged_left.melt(
    id_vars=['Student_ID', 'Name', 'Class'],
    value_vars=['Math', 'Science'],
    var_name='Subject',
    value_name='Grade'
)

print("\nMelted data (first 5 rows):")
print(melted.head())


# Now create pivot
pivot_reshaped = melted.pivot_table(
    values='Grade',
    index='Class',
    columns='Subject',
    aggfunc='mean'
)

print("\nAverage grades by Class and Subject:")
print(pivot_reshaped)

#Method 3: Multiple aggregations
print("\n"+"="*70)
print("Method 3: Multiple Statistics:")

pivot_multi = merged_left.pivot_table(
    values=['Math','Science'],
    index='Class',
    aggfunc=['mean', 'min', 'max', 'count']
)

print(pivot_multi)

#BONUS COMPLEX PIVOT
print("\n" + "="*70)
print("BONUS: Student Performance Matrix")
print("="*70)

#Create pivot showing each student's grades
student_pivot = merged_left.pivot_table(
    values=['Math','Science'],
    index=['Class', 'Name'],
    aggfunc='first'  #Each student has one grade per subject
)

print(student_pivot)

# Calculate class rankings
print("\n" + "-"*70)
print("Class Rankings:")
merged_left['Average'] = merged_left[['Math', 'Science']].mean(axis=1)
class_rankings = merged_left[['Name', 'Class', 'Science', 'Average']].sort_values('Average', ascending=False)
print(class_rankings)

print("\n" + "="*70)
print("✓ ALL EXERCISES COMPLETE!")
print("="*70)
