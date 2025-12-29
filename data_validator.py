"""
Data Input Validator & Cleaner - Day 2 Project
Demonstrates: Control Flow, String Methods, Data Cleaning

This is EXACTLY what you'll do in data analytics jobs!
Time Complexity: O(n) where n = input length
Space Complexity: O(n) for storing cleaned data
"""

print("="*60)
print("DATA INPUT VALIDATOR & CLEANER")
print("="*60)
print("This tool validates and cleans user input data")
print("="*60)

# Get user input
print("\nEnter your information:")
name = input("Full Name: ")
email = input("Email: ")
phone = input("Phone (digits only): ")
age = input("Age: ")
country = input("Country: ")

print("\n" + "="*60)
print("PROCESSING & VALIDATION")
print("="*60)

# VALIDATE & CLEAN NAME
print("\n1. NAME VALIDATION:")
print(f"   Original: '{name}'")

# Clean name: strip whitespace, title case
name_cleaned = name.strip().title()

# Validate: only letters and spaces
if name_cleaned.replace(" ", "").isalpha():
    print(f"   Cleaned:  '{name_cleaned}' ✓")
    name_valid = True
else:
    print(f"   ERROR: Name should contain only letters! ✗")
    name_valid = False

# VALIDATE & CLEAN EMAIL
print("\n2. EMAIL VALIDATION:")
print(f"   Original: '{email}'")

# Clean email: strip whitespace, lowercase
email_cleaned = email.strip().lower()

# Validate: must contain @ and end with common domains
if "@" in email_cleaned and (
    email_cleaned.endswith(".com") or 
    email_cleaned.endswith(".org") or 
    email_cleaned.endswith(".net") or
    email_cleaned.endswith(".edu")
):
    # Check if @ is not at start or end
    at_position = email_cleaned.find("@")
    if at_position > 0 and at_position < len(email_cleaned) - 1:
        print(f"   Cleaned:  '{email_cleaned}' ✓")
        email_valid = True
    else:
        print(f"   ERROR: Invalid email format! ✗")
        email_valid = False
else:
    print(f"   ERROR: Email must contain @ and valid domain (.com, .org, .net, .edu)! ✗")
    email_valid = False

# VALIDATE & CLEAN PHONE
print("\n3. PHONE VALIDATION:")
print(f"   Original: '{phone}'")

# Clean phone: remove spaces and dashes
phone_cleaned = phone.replace(" ", "").replace("-", "").strip()

# Validate: only digits, 10 digits
if phone_cleaned.isdigit():
    if len(phone_cleaned) == 10:
        # Format phone number: (XXX) XXX-XXXX
        phone_formatted = f"({phone_cleaned[:3]}) {phone_cleaned[3:6]}-{phone_cleaned[6:]}"
        print(f"   Cleaned:  '{phone_formatted}' ✓")
        phone_valid = True
    else:
        print(f"   ERROR: Phone must be exactly 10 digits! (Got {len(phone_cleaned)}) ✗")
        phone_valid = False
else:
    print(f"   ERROR: Phone should contain only digits! ✗")
    phone_valid = False

# VALIDATE & CLEAN AGE
print("\n4. AGE VALIDATION:")
print(f"   Original: '{age}'")

# Clean age: strip whitespace
age_cleaned = age.strip()

# Validate: must be digits, between 1-120
if age_cleaned.isdigit():
    age_num = int(age_cleaned)
    if 1 <= age_num <= 120:
        print(f"   Cleaned:  {age_num} ✓")
        age_valid = True
        
        # Categorize age
        if age_num < 18:
            age_category = "Minor"
        elif 18 <= age_num < 65:
            age_category = "Adult"
        else:
            age_category = "Senior"
        print(f"   Category: {age_category}")
    else:
        print(f"   ERROR: Age must be between 1 and 120! ✗")
        age_valid = False
else:
    print(f"   ERROR: Age must be a number! ✗")
    age_valid = False

# VALIDATE & CLEAN COUNTRY
print("\n5. COUNTRY VALIDATION:")
print(f"   Original: '{country}'")

# Clean country: strip whitespace, title case
country_cleaned = country.strip().title()

# Validate: only letters and spaces
if country_cleaned.replace(" ", "").isalpha():
    print(f"   Cleaned:  '{country_cleaned}' ✓")
    country_valid = True
else:
    print(f"   ERROR: Country should contain only letters! ✗")
    country_valid = False

# FINAL SUMMARY
print("\n" + "="*60)
print("VALIDATION SUMMARY")
print("="*60)

# Count valid fields
valid_count = sum([name_valid, email_valid, phone_valid, age_valid, country_valid])
total_fields = 5

print(f"\nValid Fields: {valid_count}/{total_fields}")

# Show results with color indicators
print("\nField Status:")
print(f"  Name:    {'✓' if name_valid else '✗'}")
print(f"  Email:   {'✓' if email_valid else '✗'}")
print(f"  Phone:   {'✓' if phone_valid else '✗'}")
print(f"  Age:     {'✓' if age_valid else '✗'}")
print(f"  Country: {'✓' if country_valid else '✗'}")

# Overall status using nested conditionals
print("\n" + "="*60)
if valid_count == total_fields:
    print("STATUS: ✓ ALL FIELDS VALID - Data ready for processing!")
    print("="*60)
    
    # Display cleaned data
    print("\nCLEANED DATA:")
    print(f"  Name:    {name_cleaned}")
    print(f"  Email:   {email_cleaned}")
    print(f"  Phone:   {phone_formatted}")
    print(f"  Age:     {age_num} ({age_category})")
    print(f"  Country: {country_cleaned}")
    
elif valid_count >= 3:
    print(f"STATUS: ⚠ PARTIAL SUCCESS - {valid_count} out of {total_fields} fields valid")
    print("Please fix the errors above and try again.")
else:
    print(f"STATUS: ✗ FAILED - Only {valid_count} out of {total_fields} fields valid")
    print("Too many errors. Please check all fields.")

print("="*60)

# BONUS: String method demonstration
print("\n" + "="*60)
print("STRING METHOD DEMONSTRATION")
print("="*60)

demo_text = "  DATA analytics WITH Python  "
print(f"\nOriginal: '{demo_text}'")
print(f"lower():  '{demo_text.lower()}'")
print(f"upper():  '{demo_text.upper()}'")
print(f"title():  '{demo_text.title()}'")
print(f"strip():  '{demo_text.strip()}'")
print(f"replace(): '{demo_text.replace('DATA', 'Big Data')}'")

words = demo_text.strip().split()
print(f"split():  {words}")
print(f"join():   '{'-'.join(words)}'")

print(f"\ncount('a'): {demo_text.count('a')}")
print(f"startswith('  DA'): {demo_text.startswith('  DA')}")
print(f"endswith('  '): {demo_text.endswith('  ')}")
print("="*60)