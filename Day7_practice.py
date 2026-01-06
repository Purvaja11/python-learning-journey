import numpy as np

# Exercise 1: Array Creation
print("="*50)
print("EXERCISE 1: Array Creation")
print("="*50)

# Create these arrays:
# 1. Array of numbers 1-20
# 2. Array of 10 zeros
# 3. 5x5 identity matrix
# 4. Random integers between 1-100 (size 15)

# YOUR CODE HERE
print(f"Numbers 1 - 20: {np.arange(1, 21)}")
print(f"Array of 10 zeros: {np.zeros(10)}")
print(f"5x5 identity matrix: {np.eye(5)}")
print(f"Random integers between 1-100 (size = 15): {np.random.randint(1, 100, size=15)}")

# Exercise 2: Array Operations
print("\n" + "="*50)
print("EXERCISE 2: Array Operations")
print("="*50)

grades = np.array([85, 90, 78, 92, 88, 76, 95, 89, 84, 91])

# Calculate:
# 1. Average grade
# 2. Highest and lowest grade
# 3. Standard deviation
# 4. How many students scored above 85?
# 5. Add 5 bonus points to everyone's grade

# YOUR CODE HERE
print(f"Average: {np.mean(grades)}")
print(f"Highest grade: {np.max(grades)}")
print(f"Lowest grade: {np.min(grades)}")
print(f"Standard Deviation: {np.std(grades)}")
print(f"No. of students who scored above 85: {len(grades[grades > 85])}")
print(f"Grades after adding Bonus 5 points: {grades + 5}")

# Exercise 3: 2D Array Analysis
print("\n" + "="*50)
print("EXERCISE 3: 2D Array Analysis")
print("="*50)

# Test scores: 3 students, 4 subjects each
scores = np.array([[85, 90, 78, 92],
                   [88, 76, 95, 89],
                   [84, 91, 87, 93]])

# Calculate:
# 1. Average score for each student (by row)
# 2. Average score for each subject (by column)
# 3. Overall class average
# 4. Highest score in entire array

# YOUR CODE HERE
print(f"Average score for each student: {np.mean(scores, axis=1)}")
print(f"Average score for each subject: {np.mean(scores, axis=0)}")
print(f"Overall Class average: {np.mean(scores)}")
print(f"Highest Score of Class: {np.max(scores)}")
