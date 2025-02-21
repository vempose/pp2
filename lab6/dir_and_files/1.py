import  os


path = "C://Windows"

# List only directories
print(f"{' Dirs ':-^50}\n", [x for x in os.listdir(path) if os.path.isdir(os.path.join(path, x))], "\n", sep="")

# List only files
print(f"{' Files ':-^50}\n", [x for x in os.listdir(path) if os.path.isfile(os.path.join(path, x))], "\n", sep="")

# Dirs and files
print(f"{' Dirs and files ':-^50}\n", os.listdir(path), "\n", sep="")