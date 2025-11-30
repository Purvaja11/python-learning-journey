"""
Password Strength Checker - Day 1 Project
Demonstrates: Variables, Data Types, Operators, Type Conversion

Time Complexity: O(n) where n = password length
Space Complexity: O(1) - only storing counters
"""

# Get password from user
password = input("Enter a password to check its strength: ")

# Initialize counters (using integers)
length = len(password)
has_upper = False
has_lower = False
has_digit = False
has_special = False
strength_score = 0

# Check each character (O(n) loop)
for char in password:
    if char.isupper():  # Check uppercase
        has_upper = True
    elif char.islower():  # Check lowercase
        has_lower = True
    elif char.isdigit():  # Check digit
        has_digit = True
    elif char in "!@#$%^&*()_+-=[]{}|;:,.<>?":  # Check special chars
        has_special = True

# Calculate strength score (O(1) operations)
if length >= 8:
    strength_score += 1
if length >= 12:
    strength_score += 1
if has_upper:
    strength_score += 1
if has_lower:
    strength_score += 1
if has_digit:
    strength_score += 1
if has_special:
    strength_score += 1

# Determine strength level using comparison operators
if strength_score <= 2:
    strength = "Weak"
    color = "🔴"
elif strength_score <= 4:
    strength = "Medium"
    color = "🟡"
else:
    strength = "Strong"
    color = "🟢"

# Display results (f-strings are Pythonic for formatting)
print("\n" + "="*40)
print(f"{color} Password Strength: {strength}")
print("="*40)
print(f"Length: {length} characters")
print(f"Has uppercase: {'✓' if has_upper else '✗'}")
print(f"Has lowercase: {'✓' if has_lower else '✗'}")
print(f"Has digits: {'✓' if has_digit else '✗'}")
print(f"Has special chars: {'✓' if has_special else '✗'}")
print(f"Strength Score: {strength_score}/6")
print("="*40)

# Bonus: Calculate crack time estimate (demonstrates arithmetic operators)
possible_chars = 0
if has_lower:
    possible_chars += 26
if has_upper:
    possible_chars += 26
if has_digit:
    possible_chars += 10
if has_special:
    possible_chars += 20

if possible_chars > 0:
    combinations = possible_chars ** length
    seconds = combinations / 1_000_000_000
    
    if seconds < 60:
        time_str = f"{seconds:.2f} seconds"
    elif seconds < 3600:
        time_str = f"{seconds/60:.2f} minutes"
    elif seconds < 86400:
        time_str = f"{seconds/3600:.2f} hours"
    elif seconds < 31536000:
        time_str = f"{seconds/86400:.2f} days"
    else:
        time_str = f"{seconds/31536000:.2f} years"
    
    print(f"Estimated crack time: {time_str}")
    print("="*40)