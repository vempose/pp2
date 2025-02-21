import os


path = "C://Program Files//Git"

if os.path.exists(path):
    print(f"'{os.path.normpath(path)}' exists!")
    print(f"Files in {os.path.basename(path)}:", [x for x in os.listdir(path) if os.path.isfile(os.path.join(path, x))])
    print(f"Dirs in {os.path.basename(path)}:", [x for x in os.listdir(path) if os.path.isdir(os.path.join(path, x))])
else:
    print(f"There's no '{os.path.normpath(path)}'...")