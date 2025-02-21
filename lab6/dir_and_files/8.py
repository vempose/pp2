import os


path = input("Which file do you want to delete? Enter it's absolute path: ")

if os.path.exists(path):
    print("This file existst. Moving on...")

    if os.access(path, os.W_OK):
        print("Good, I can delete this file, so... I'M DELETING IT!")
        os.remove(path)
        print("Done :>")
    else:
        print("I can't delete this file... sorry :<")
else:
    print("There're no such file. Aborting...")