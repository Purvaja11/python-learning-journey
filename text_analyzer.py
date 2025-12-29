sentence = input("Enter a sentence:")

length = len(sentence)
length_without_spaces = len(sentence.replace(" ",""))
words = sentence.split()
total_words = len(words)

vowels = 0
consonants = 0
for char in sentence.lower():
    if char in "aeiou":
        vowels += 1
    elif char.isalpha():
        consonants += 1

longest_word = max(words, key=len)
shortest_word = min(words, key=len)

print("\nAnalysis:")
print(f"Total characters: {length}")
print(f"Characters (no spaces): {length_without_spaces}")
print(f"Words: {total_words}")
print(f"Vowels: {vowels}")
print(f"Consonants: {consonants}")
print(f"Longest word:{longest_word} ({len(longest_word)} letters)")
print(f"Shortest word: {shortest_word} ({len(shortest_word)} letters)")
