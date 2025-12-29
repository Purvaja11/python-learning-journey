# Grade Calculator - Practice Project
print("="*50)
print("GRADE CALCULATOR")
print("="*50)

# Step 1: Get 5 scores
print("\nEnter scores for 5 subjects (0-100):")
score1 = int(input("Subject 1: "))
score2 = int(input("Subject 2: "))
score3 = int(input("Subject 3: "))
score4 = int(input("Subject 4: "))
score5 = int(input("Subject 5: "))

# Step 2: Calculate average
# YOUR CODE HERE
total_score = score1+score2+score3+score4+score5
average = total_score/5

# Step 3: Determine letter grade
# YOUR CODE HERE
if average >= 90:
    grade = "A"
elif average >= 80:
    grade = "B"
elif average >= 70:
    grade = "C"
elif average >= 60:
    grade = "D"
else:
    grade = "F"

    
# Step 4: Check pass/fail (passing = average >= 50)
# YOUR CODE HERE
if average >= 50:
    result = "PASS!"
else:
    result = "FAIL!"

# Step 5: Check honor roll (average >= 85)
# YOUR CODE HERE
if average >= 85:
    honor = "YES"
else:
    honor = "NO"

# Step 6: Display results
print("\n" + "="*50)
print("RESULTS")
print("="*50)
# YOUR CODE HERE
print(f"Subject 1: {score1}")
print(f"Subject 2: {score2}")
print(f"Subject 3: {score3}")
print(f"Subject 4: {score4}")
print(f"Subject 5: {score5}")
print("\n")
print(f"Average score: {average}")
print(f"Grade: {grade}")
print(f"Status: {result}")
print(f"Honor Roll: {honor}")