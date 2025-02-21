import re


with open("row.txt", "r") as file:
    text = file.read()

task_number = 1
def perform(p: str):
    global task_number
    print(f"--- Task {task_number} ---")
    print(f"Pattern: {p!r}")
    print(f"Matched strings: {re.findall(p, text)}\n")
    task_number += 1


# 1. Write a Python program that matches a string that has an 'a' followed by zero or more 'b's.
perform("ab*")

# 2. Write a Python program that matches a string that has an 'a' followed by two to three 'b'.
perform("ab{2,3}")

# 3. Write a Python program to find sequences of lowercase letters joined with a underscore.
perform("[a-zа-я]+_[a-zа-я]+")

# 4. Write a Python program to find the sequences of one upper case letter followed by lower case letters.
perform("[A-ZА-Я][a-zа-я]+")

# 5. Write a Python program that matches a string that has an 'a' followed by anything, ending in 'b'.
perform("a.+b")