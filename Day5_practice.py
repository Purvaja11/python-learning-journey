#Exercise 1
#Temperature Converter Functions
def celsius_to_fahrenheit(celsius):
    """Convert celsius to Fahrenheit"""
    return (celsius * 9/5) + 32
    
    

def fahrenheit_to_celsius(fahrenheit):
    """Convert Fahrenheit to Celsius"""
    return (fahrenheit - 32) * 5/9
    

#test
print(celsius_to_fahrenheit(0))
print(fahrenheit_to_celsius(32))

#Excercise 2
#Grade Calculator with functions
def calculate_letter_grade(score):
    """Return letter grade for numeric score"""
    if score >= 90 :
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    elif score < 60:
        return "F"
    else:
        return "Not Valid!"
    

def calculate_gpa(grades):
    """Calculate GPA from list of letter grades
    A=4.0, B=3.0, C=2.0, D=1.0, F=0.0"""
    
    grade_points = {
        'A': 4.0,
        'B': 3.0,
        'C': 2.0,
        'D': 1.0,
        'F': 0.0
    }

    # Calculate total points
    total_points = 0
    for grade in grades:
        total_points += grade_points[grade]

    #Calculate average
    gpa = total_points / len(grades)
    return gpa

# Test
print(calculate_letter_grade(85))  # B
print(calculate_gpa(['A', 'B', 'A', 'C']))  

# Additional tests
print("\n" + "="*40)
print("ADDITIONAL TESTS")
print("="*40)

# Test letter grades
print(f"Score 95: {calculate_letter_grade(95)}")  
print(f"Score 75: {calculate_letter_grade(75)}") 
print(f"Score 55: {calculate_letter_grade(55)}")  
# Test GPA
print(f"\nGPA [A, A, A, A]: {calculate_gpa(['A', 'A', 'A', 'A'])}")  
print(f"GPA [B, B, B, B]: {calculate_gpa(['B', 'B', 'B', 'B'])}")    
print(f"GPA [A, B, C, D]: {calculate_gpa(['A', 'B', 'C', 'D'])}")    