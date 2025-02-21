import re


# Write a Python program to insert spaces between words starting with capital letters.
text = "BioWorldWithHelp of myMother and SISTER :D goodBYE!"

print(re.sub(
    r"(?<=\S)(?=[A-ZА-Я][a-z]+)",
    " ",
    text
))