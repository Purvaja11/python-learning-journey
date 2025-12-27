# Exercise A: Print with different format
names = ["Alice", "Bob", "Charlie"]
ages = [25, 30, 35]

names.append("Maire")
ages.append(29)


# Print: "Alice is 25 years old"
# YOUR CODE HERE
for name,age in zip(names,ages):
    print(f"{name} is {age} years old")

# Exercise B: Find who is oldest
# YOUR CODE HERE
oldest_age = max(ages)
oldest_index = ages.index(oldest_age)
print(f"\nOldest Person: {names[oldest_index]}, Age: {oldest_age}")

# Exercise C: Create list of people over 28
# YOUR CODE HERE
people = [person for person, age in zip(names, ages) if age > 28]
print(f"\nPeople Details (over age 28): {people}")
