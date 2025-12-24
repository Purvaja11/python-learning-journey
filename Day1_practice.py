print("="*50)
print("EXERCISE 1: Using  += Operator")
print("="*50)

score = 10
print(f"Initial score: {score}")


#Add 5 to score using shorthand
score += 5

print(f"After adding 5: {score}")
print()

#Exercise 2: Check Data Types
print("="*50)
print("EXERCISE 2: Check Data Types")
print("="*50)

age = 25
price = 19.99
name = "Alice"
is_student = True

print(f"age = {age}, type: {type(age)}")
print(f"price = {price}, type: {type(price)}")
print(f"name = {name}, type: {type(name)}")
print(f"is_student = {is_student}, type: {type(is_student)}")

#Exercise 3: Use Comparison Operators
print("="*50)
print("EXERCISE 3: Comparison Operators")
print("="*50)

x = 15
y = 20

result1 = x < y
print(f"Is {x} less than {y}? {result1}")

result2 = x != y
print(f"Is {x} not equal to {y}? {result2}")

# All 6 Comparison Operators
print(f"\n{x} == {y}: {x == y}")  # Equal to
print(f"{x} != {y}: {x != y}")    # Not equal to
print(f"{x} > {y}: {x > y}")      # Greater than
print(f"{x} < {y}: {x < y}")      # Less than
print(f"{x} >= {y}: {x >= y}")    # Greater than or equal to
print(f"{x} <= {y}: {x <= y}")    # Less than or equal to

# Exercise 4: Ternary Operators
print("="*50)
print("EXERCISE 4: Ternary Operator")
print("="*50)

temperature = 30

# Using ternary operator (one line if-else)
weather = "Hot" if temperature > 25 else "Cold"
print(f"\nTemperature is {temperature}°C")
print(f"Weather: {weather}")

temp1 = 20
weather1 = "Hot" if temp1 > 25 else "Cold"
print(f"\nTemperature is {temp1}°C")
print(f"Weather: {weather1}")

# The same logis using regular if-else
print("\nSame Logic with regular if-else:")
if temperature >25:
    weather_normal = "Hot"
else:
    weather_normal = "Cold"
print(f"Weather: {weather_normal}")

# Exercise 5: String Manipulation
print("="*50)
print("EXERCISE 5: String Manipulation")
print("="*50)

name = "Purvaja"

print(name * 5)          # Print name 5 times on same line

print((name + " ") * 5)  # Print name 5 times with spaces

print("-" * 50)          # Print a line of 50 dashes

print("=" * 20 + "HEADER" + "=" * 20) # Combine different string operations

greeting = "Hello, " + name + "!"  # String concatenation with +
print(greeting)

greeting_pythonic = f"Hello, {name}"  # Using f-strings (Pythonic way)
print(greeting_pythonic)

# Escape sequences
print("\nNew line example:")
print("Line 1\nLine 2\nLine 3")

print("\nTab example:")
print("Name:\tPurvaja")
print("Age:\t25")

# Combing All Concepts
print("="*50)
print("BONUS: Mini Calculator")
print("="*50)

num1 = 10
num2 = 3

print(f"Number 1: {num1}")
print(f"Number 2: {num2}")
print(f"Type of num1: {type(num1)}")

#Arithemetic Operators:
print("Arithemetic Operations:")
print(f"{num1} + {num2} = {num1 + num2}")
print(f"{num1} - {num2} = {num1 - num2}")
print(f"{num1} * {num2} = {num1 * num2}")
print(f"{num1} / {num2} = {num1 / num2}")
print(f"{num1} // {num2} = {num1 // num2}")   #Floor division
print(f"{num1} % {num2} = {num1 % num2}")     #Modulus (remainder)
print(f"{num1} ** {num2} = {num1 ** num2}")   #Exponentiation

# Comparison operators
print("Comparison Operations:")
print(f"{num1} > {num2} = {num1 > num2}")
print(f"{num1} < {num2} = {num1 < num2}")
print(f"{num1} == {num2} = {num1 == num2}")

# Logical operators
print("Logical Operations:")
is_positive1 = num1 > 0
is_positive2 = num2 > 0
print(f"Both numbers positive? {is_positive1 and is_positive2}")
print(f"At least one positive? {is_positive1 or is_positive2}")
print(f"{num1} is NOT positive? {not is_positive1}")

# Ternary operator
result = "Even" if num1 % 2 == 0 else "Odd"
print(f"{num1} is {result}")
print("="*50)
