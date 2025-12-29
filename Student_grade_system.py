"""
Student Grade Management System - Day 3 Project
Demonstrates: Loops, Lists, List Methods, List Comprehensions

Time Complexity: O(n) for most operations, O(n log n) for sorting
Space Complexity: O(n) where n = number of students
"""

print("="*60)
print("STUDENT GRADE MANAGEMENT SYSTEM")
print("="*60)

# Store student data
students = []
grades = []

# Get number of students
while True:
    num_students = input("\nHow many students? ")
    if num_students.isdigit() and int(num_students) > 0:
        num_students = int(num_students)
        break
    else:
        print("Please enter a valid positive number!")

# Collect student data using for loop
print(f"\nEnter data for {num_students} students:")
for i in range(num_students):
    print(f"\n--- Student {i + 1} ---")
    
    # Get name
    while True:
        name = input("Name: ").strip().title()
        if name and name.replace(" ", "").isalpha():
            break
        else:
            print("Invalid name! Use letters only.")
    
    # Get grade
    while True:
        grade = input("Grade (0-100): ")
        if grade.isdigit() and 0 <= int(grade) <= 100:
            grade = int(grade)
            break
        else:
            print("Invalid grade! Enter 0-100.")
    
    # Store data
    students.append(name)
    grades.append(grade)

# Display all students
print("\n" + "="*60)
print("ALL STUDENTS")
print("="*60)
for i in range(len(students)):
    print(f"{i + 1}. {students[i]}: {grades[i]}")

# Calculate statistics
print("\n" + "="*60)
print("STATISTICS")
print("="*60)

# Total and average
total_grade = sum(grades)
average_grade = total_grade / len(grades)
print(f"Total Students: {len(students)}")
print(f"Average Grade: {average_grade:.2f}")

# Highest and lowest
highest_grade = max(grades)
lowest_grade = min(grades)
highest_index = grades.index(highest_grade)
lowest_index = grades.index(lowest_grade)

print(f"Highest: {highest_grade} ({students[highest_index]})")
print(f"Lowest: {lowest_grade} ({students[lowest_index]})")

# Pass/Fail analysis (passing = 50+)
passing_grades = [g for g in grades if g >= 50]
failing_grades = [g for g in grades if g < 50]

pass_count = len(passing_grades)
fail_count = len(failing_grades)
pass_rate = (pass_count / len(grades)) * 100

print(f"\nPassing (≥50): {pass_count} students ({pass_rate:.1f}%)")
print(f"Failing (<50): {fail_count} students ({100-pass_rate:.1f}%)")

# Grade distribution
a_count = len([g for g in grades if g >= 90])
b_count = len([g for g in grades if 80 <= g < 90])
c_count = len([g for g in grades if 70 <= g < 80])
d_count = len([g for g in grades if 60 <= g < 70])
f_count = len([g for g in grades if g < 60])

print("\n" + "="*60)
print("GRADE DISTRIBUTION")
print("="*60)
print(f"A (90-100): {a_count} students")
print(f"B (80-89):  {b_count} students")
print(f"C (70-79):  {c_count} students")
print(f"D (60-69):  {d_count} students")
print(f"F (0-59):   {f_count} students")

# Sort students by grade (highest to lowest)
print("\n" + "="*60)
print("STUDENTS RANKED BY GRADE")
print("="*60)

# Create list of tuples (grade, name) for sorting
student_data = list(zip(grades, students))
student_data.sort(reverse=True)  # Sort by grade (first element of tuple)

for rank, (grade, name) in enumerate(student_data, 1):
    # Assign letter grade
    if grade >= 90:
        letter = "A"
    elif grade >= 80:
        letter = "B"
    elif grade >= 70:
        letter = "C"
    elif grade >= 60:
        letter = "D"
    else:
        letter = "F"
    
    print(f"{rank}. {name}: {grade} ({letter})")

# Search for a specific student
print("\n" + "="*60)
print("STUDENT SEARCH")
print("="*60)

search_name = input("Enter student name to search: ").strip().title()

if search_name in students:
    index = students.index(search_name)
    grade = grades[index]
    
    # Calculate letter grade
    if grade >= 90:
        letter = "A"
    elif grade >= 80:
        letter = "B"
    elif grade >= 70:
        letter = "C"
    elif grade >= 60:
        letter = "D"
    else:
        letter = "F"
    
    # Find rank
    rank = sorted(grades, reverse=True).index(grade) + 1
    
    print(f"\nStudent Found:")
    print(f"  Name: {search_name}")
    print(f"  Grade: {grade}/100")
    print(f"  Letter: {letter}")
    print(f"  Rank: {rank} out of {len(students)}")
    print(f"  Status: {'Pass ✓' if grade >= 50 else 'Fail ✗'}")
    
    # Compare to average
    diff = grade - average_grade
    if diff > 0:
        print(f"  Performance: {diff:.1f} points above average")
    elif diff < 0:
        print(f"  Performance: {abs(diff):.1f} points below average")
    else:
        print(f"  Performance: Exactly at average")
else:
    print(f"\n✗ Student '{search_name}' not found!")

# Students above/below average
print("\n" + "="*60)
print("PERFORMANCE ANALYSIS")
print("="*60)

above_avg = [students[i] for i in range(len(students)) if grades[i] > average_grade]
below_avg = [students[i] for i in range(len(students)) if grades[i] < average_grade]
at_avg = [students[i] for i in range(len(students)) if grades[i] == average_grade]

print(f"Above Average ({len(above_avg)} students):")
if above_avg:
    print(f"  {', '.join(above_avg)}")
else:
    print("  None")

print(f"\nBelow Average ({len(below_avg)} students):")
if below_avg:
    print(f"  {', '.join(below_avg)}")
else:
    print("  None")

if at_avg:
    print(f"\nAt Average ({len(at_avg)} students):")
    print(f"  {', '.join(at_avg)}")

print("\n" + "="*60)
print("END OF REPORT")
print("="*60)