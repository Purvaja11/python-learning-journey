# Username Generator - String Practice
print("="*50)
print("USERNAME GENERATOR")
print("="*50)

# Step 1: Get input
full_name = input("Enter full name: ")
birth_year = input("Enter birth year (YYYY): ")

# Step 2: Process the name
# Split name into parts
# Extract first name, middle name (if exists), last name
# YOUR CODE HERE
words = full_name.split()
first_name = words[0]
middle_name = words[1] if len(words) > 1 else ""



# Step 3: Generate username
# First 3 letters of first name (lowercase)
# First letter of middle name (uppercase) - if exists
# Last 2 digits of birth year
# YOUR CODE HERE
letters = first_name.lower()[0:3]
digits = birth_year[-2:]

if middle_name:
    username = letters + middle_name.upper()[0] + digits
else:
    username = letters + digits

# Step 4: Validate username
# Check length (5-10 characters)
# Check for spaces
# YOUR CODE HERE
if " " in username:
    validate = "✗ Invalid"
    reason = "contains spaces"
elif not (5 <= len(username) <= 10):
    validate = "✗ Invalid"
    reason = f"length must be 5-10 characters(Got {len(username)})"
else:
    validate = "✓ Valid"
    reason = "all checks passed"

# Step 5: Display result
print("\n" + "="*50)
print("RESULT")
print("="*50)
# YOUR CODE HERE
print(f"{username} {validate} ({len(username)} characters, {reason}) ")