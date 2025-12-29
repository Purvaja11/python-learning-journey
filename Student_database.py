"""
Student Database Management System - Day 4 Project
Demonstrates: Dictionaries, Sets, Nested Data Structures

Time Complexity: O(1) for lookups, O(n) for iterations
Space Complexity: O(n) where n = number of students
"""

print("="*60)
print("STUDENT DATABASE MANAGEMENT SYSTEM")
print("="*60)

# Database: Dictionary of students (ID: student info)
database = {}
all_courses = set()  # Track all unique courses

def add_student():
    """Add a new student to database"""
    print("\n--- ADD NEW STUDENT ---")
    
    # Generate student ID
    if database:
        student_id = max(database.keys()) + 1
    else:
        student_id = 1
    
    # Get student info
    name = input("Name: ").strip().title()
    
    while True:
        age = input("Age: ")
        if age.isdigit() and 15 <= int(age) <= 100:
            age = int(age)
            break
        print("Invalid age! Enter 15-100.")
    
    # Get courses
    print("Enter courses (comma-separated): ")
    courses_input = input("Courses: ").strip()
    courses = [c.strip().title() for c in courses_input.split(",")]
    
    # Get grades for each course
    grades = {}
    for course in courses:
        while True:
            grade = input(f"Grade for {course} (0-100): ")
            if grade.isdigit() and 0 <= int(grade) <= 100:
                grades[course] = int(grade)
                all_courses.add(course)  # Add to global course set
                break
            print("Invalid grade! Enter 0-100.")
    
    # Calculate average
    avg_grade = sum(grades.values()) / len(grades) if grades else 0
    
    # Store in database
    database[student_id] = {
        "name": name,
        "age": age,
        "courses": courses,
        "grades": grades,
        "average": avg_grade
    }
    
    print(f"\n✓ Student added successfully! ID: {student_id}")

def display_all_students():
    """Display all students in database"""
    if not database:
        print("\n✗ No students in database!")
        return
    
    print("\n" + "="*60)
    print("ALL STUDENTS")
    print("="*60)
    
    for student_id, info in database.items():
        print(f"\nID: {student_id}")
        print(f"  Name: {info['name']}")
        print(f"  Age: {info['age']}")
        print(f"  Courses: {', '.join(info['courses'])}")
        print(f"  Average Grade: {info['average']:.2f}")

def search_student():
    """Search for a student by ID or name"""
    print("\n--- SEARCH STUDENT ---")
    print("1. Search by ID")
    print("2. Search by Name")
    
    choice = input("Choose (1/2): ")
    
    if choice == "1":
        student_id = input("Enter Student ID: ")
        if student_id.isdigit() and int(student_id) in database:
            student_id = int(student_id)
            display_student_details(student_id)
        else:
            print("✗ Student not found!")
    
    elif choice == "2":
        search_name = input("Enter Name: ").strip().title()
        found = False
        for student_id, info in database.items():
            if info["name"] == search_name:
                display_student_details(student_id)
                found = True
                break
        if not found:
            print("✗ Student not found!")
    
    else:
        print("Invalid choice!")

def display_student_details(student_id):
    """Display detailed information for a student"""
    info = database[student_id]
    
    print("\n" + "="*60)
    print("STUDENT DETAILS")
    print("="*60)
    print(f"ID: {student_id}")
    print(f"Name: {info['name']}")
    print(f"Age: {info['age']}")
    print(f"\nCourses and Grades:")
    for course, grade in info['grades'].items():
        letter = get_letter_grade(grade)
        print(f"  {course}: {grade} ({letter})")
    print(f"\nAverage Grade: {info['average']:.2f} ({get_letter_grade(info['average'])})")
    
    # Compare to class average
    if len(database) > 1:
        class_avg = sum(s['average'] for s in database.values()) / len(database)
        diff = info['average'] - class_avg
        if diff > 0:
            print(f"Performance: {diff:.2f} points above class average")
        elif diff < 0:
            print(f"Performance: {abs(diff):.2f} points below class average")
        else:
            print("Performance: At class average")

def get_letter_grade(grade):
    """Convert numeric grade to letter grade"""
    if grade >= 90:
        return "A"
    elif grade >= 80:
        return "B"
    elif grade >= 70:
        return "C"
    elif grade >= 60:
        return "D"
    else:
        return "F"

def class_statistics():
    """Display statistics for entire class"""
    if not database:
        print("\n✗ No students in database!")
        return
    
    print("\n" + "="*60)
    print("CLASS STATISTICS")
    print("="*60)
    
    # Calculate averages
    all_averages = [info['average'] for info in database.values()]
    class_avg = sum(all_averages) / len(all_averages)
    
    print(f"Total Students: {len(database)}")
    print(f"Class Average: {class_avg:.2f}")
    print(f"Highest Average: {max(all_averages):.2f}")
    print(f"Lowest Average: {min(all_averages):.2f}")
    
    # Find top performer
    top_id = max(database.keys(), key=lambda x: database[x]['average'])
    print(f"\nTop Performer: {database[top_id]['name']} ({database[top_id]['average']:.2f})")
    
    # All courses offered
    print(f"\nAll Courses Offered: {', '.join(sorted(all_courses))}")
    
    # Grade distribution
    grade_counts = {"A": 0, "B": 0, "C": 0, "D": 0, "F": 0}
    for info in database.values():
        letter = get_letter_grade(info['average'])
        grade_counts[letter] += 1
    
    print("\nGrade Distribution:")
    for letter, count in grade_counts.items():
        percentage = (count / len(database)) * 100
        print(f"  {letter}: {count} students ({percentage:.1f}%)")

def students_by_course():
    """Show which students are enrolled in each course"""
    if not all_courses:
        print("\n✗ No courses in database!")
        return
    
    print("\n" + "="*60)
    print("STUDENTS BY COURSE")
    print("="*60)
    
    for course in sorted(all_courses):
        enrolled = [info['name'] for info in database.values() if course in info['courses']]
        print(f"\n{course} ({len(enrolled)} students):")
        if enrolled:
            print(f"  {', '.join(enrolled)}")

# Main menu
while True:
    print("\n" + "="*60)
    print("MENU")
    print("="*60)
    print("1. Add Student")
    print("2. Display All Students")
    print("3. Search Student")
    print("4. Class Statistics")
    print("5. Students by Course")
    print("6. Exit")
    
    choice = input("\nChoose an option (1-6): ")
    
    if choice == "1":
        add_student()
    elif choice == "2":
        display_all_students()
    elif choice == "3":
        search_student()
    elif choice == "4":
        class_statistics()
    elif choice == "5":
        students_by_course()
    elif choice == "6":
        print("\n👋 Goodbye!")
        break
    else:
        print("Invalid choice! Please choose 1-6.")
        