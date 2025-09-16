import os
import pathlib

file = pathlib.Path('sample.pdf')
try:
    os.startfile(file, "print")
except FileNotFoundError:
    print(f"Error: file not found '{file}'.")

