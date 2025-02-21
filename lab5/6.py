import re


with open("row.txt", "r") as file:
    text = file.read()

# Write a Python program to replace all occurrences of space, comma, or dot with a colon.
print(re.sub("[ .,]", ":", text))