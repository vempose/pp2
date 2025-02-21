# Copy content from file A.txt to B.txt

with open("A.txt", "r") as file_from:
    text = file_from.readlines()

with open("B.txt", "w") as file_where:
    file_where.writelines(text)