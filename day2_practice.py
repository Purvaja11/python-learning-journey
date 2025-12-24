#Exercise 1
#Email domain extractor
email = "user@example.com"
at_position = email.find("@")
domain = email[at_position + 1:]
print(domain)

#Exercise 2
#CSV parser
data = "John,25,Engineer,New York"
make_list = data.split(",")
print(make_list)
print(type(make_list))
name = make_list[0]
age = int(make_list[1])
position = make_list[2]
country = make_list[3]
print(f"Name: {name}")
print(f"Age: {age}")
print(f"Job: {position}")
print(f"City: {country}")

#Exercise 3
#Password validator
password = input("Enter a password:")
length = len(password)
has_upper = False
has_lower = False
has_digit = False

for char in password:
    if char.isupper():
        has_upper = True
    elif char.islower():
        has_lower = True
    elif char.isdigit():
        has_digit = True

if length >= 8:
    print("Password contains more than 8 characters")
else:
    print("Please enter more than 8 characters")

print("Password validation")
print(f"Length: {length} characters")
print(f"Has Uppercase: {'✓' if has_upper else '✗'}")
print(f"Has Lowercase: {'✓' if has_lower else '✗'}")
print(f"Has Digits: {'✓' if has_digit else '✗'}")

#Exercise 4
#name formatter
names = ["  JOHN doe  ", "alice SMITH", "  bob  "]
print(f"Original names: {names}")

cleaned_names = []
for name in names:
    cleaned = name.strip().title()
    cleaned_names.append(cleaned)

print(f"Cleaned: {cleaned_names}")

#Exercise 5
#Word counter

sentence = "Python is amazing and Python is powerful"
print(f"Sentence: {sentence}")

#Using count()
words = sentence.lower().split()
python_count = words.count("python")
total_words = len(words)

print(f"\n'Python'appears: {python_count} times")
print(f"Total words: {total_words}")

#using loop
count_manual = 0
for word in words:
    if word == "python":
        count_manual += 1

print(f'\nManual count: {count_manual} times (same result!)')
