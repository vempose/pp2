import re


# Write a Python program to split a string at uppercase letters.
text = "BioWorldWithHelp of my Mother and SISTER :D goodBYE!"

print(re.split(
    r"(?<=.)(?=[A-Z])",
    text
))