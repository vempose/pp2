import os


file_path = "C://Windows//explorer.exe"

if os.path.exists(file_path):
    print(f"File {os.path.basename(file_path)!r} exists!")

    if os.access(file_path, os.R_OK):
        print(f"Read permission is granted for file: {file_path}")
    else:
        print(f"Read permission is not granted for file: {file_path}")
        
    if os.access(file_path, os.W_OK):
        print(f"Write permission is granted for file: {file_path}")
    else:
        print(f"Write permission is not granted for file: {file_path}")
        
    if os.access(file_path, os.X_OK):
        print(f"Execute permission is granted for file: {file_path}")
    else:
        print(f"Execute permission is not granted for file: {file_path}")
else:
    print(f"There is no {file_path}...")