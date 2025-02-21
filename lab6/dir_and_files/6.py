import os
from time import sleep


os.chdir("files")
if os.listdir():
    print("Deleting all files in the 'files' dir! Watch out!")
    for file in os.listdir():
        os.remove(file)
    sleep(3)
    
for file in "abcdefghijklmnopqrstuvwxyz":
    with open(file + ".txt", "w") as file_txt:
        pass
else:
    print("New txt files are created!")