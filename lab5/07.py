import re


# Write a python program to convert snake case string to camel case string.
text = "some-example-of-snake-case you can check it by-how-to-do-it. See you later-allegator"

print(re.sub(
    "(?<=[a-zA-Zа-яА-Я])-([a-zA-Zа-яА-Я])",
    lambda pat: pat.group(1).upper(),
    text
))