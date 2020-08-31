import os
import pathlib

count = 0
path = os.getcwd() + "//" + "input"
for path in pathlib.Path(path).iterdir():
    if path.is_file():
        count += 1

print(count)