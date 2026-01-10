import pandas as pd
import numpy as np

# Create sample employee data
df = pd.DataFrame({
    'Name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve', 'Frank'],
    'Department': ['Sales', 'IT', 'Sales', 'IT', 'HR', 'Sales'],
    'Salary': [50000, 60000, 55000, 65000, 52000, 58000],
    'Age': [25, 30, 28, 35, 32, 29],
    'Experience': [2, 5, 3, 8, 6, 4]
})

# EXERCISE 1: Basic Operations
# 1. Display first 3 rows
# 2. Get column names
# 3. Get shape
# YOUR CODE HERE
print("\n"+ "="*50)
print("EXERCISE 1: Basic Operations")
print("="*50)
print("\nFirst 3 rows:")
print(df.head(3))
print("Column names:")
print(df.columns)
print("Shape of the matrix:")
print(df.shape)

# EXERCISE 2: Filtering
# 1. Find all employees in Sales department
# 2. Find employees with salary > 55000
# 3. Find IT employees with experience > 5 years
# YOUR CODE HERE
print("\n"+ "="*50)
print("EXERCISE 2: Filtering")
print("="*50)
employee_sales = df[(df['Department'] == 'Sales')]
print("All employees in Sales Dept.:")
print(employee_sales)
employee_salary = df[df['Salary'] > 55000]
print("Employees having salary above 55,000:")
print(employee_salary)
it_employee = df[(df['Department'] == 'IT') & (df['Experience'] > 5)]
print("IT employees with experience above 5 years:")
print(it_employee)

# EXERCISE 3: Calculations
# 1. Add a column 'Salary_per_year_exp' = Salary / Experience
# 2. Calculate average salary by department
# 3. Find highest paid employee
# YOUR CODE HERE
print("\n"+ "="*50)
print("EXERCISE 3: Calculations")
print("="*50)
df['Salary_per_year_exp'] = df['Salary'] / df['Experience']
print("\nData after adding Salary per year exp: ")
print(df.head())
avg_by_dept = df.groupby('Department')['Salary'].mean()
print("\nAverage Salary by department ")
print(avg_by_dept)
high_paid_employee = df[df['Salary'] == df['Salary'].max()]
print("\nHighest paid employee:")
print(high_paid_employee)

# EXERCISE 4: Grouping
# 1. Group by department and calculate mean salary
# 2. Count employees per department
# 3. Find max salary per department
# YOUR CODE HERE
print("\n"+ "="*50)
print("EXERCISE 4: Grouping")
print("="*50)
print("\nSalary by Dept.:")

department_salary = df.groupby('Department').agg({
    'Salary': 'sum'
})
department_salary.columns = ['Total']
department_salary = department_salary.sort_values('Total', ascending=False)

print(department_salary)

print("\nCount of Employees by Dept.:")
count_employee = df.groupby('Department').size()
print(count_employee)

print("\nMax salary per Dept.:")
max_salary_per_dept = df.groupby('Department')['Salary'].max()
print(max_salary_per_dept)