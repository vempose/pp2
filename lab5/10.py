import re


# Write a Python program to convert a given camel case string to snake case.
text = "someGoodCamelCase string which canBeModified and ViewedAsSomethingElse"

print(re.sub(
    r"(?<=[a-zа-я0-9])([A-ZА-Я])",
    lambda pat: "-" + pat.group(1).lower(),
    text
))