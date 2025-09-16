import os
import win32print

# Get the default printer name
printer_name = win32print.GetDefaultPrinter()
print(f"Printing to default printer: {printer_name}")

# Specify the path to your document
file_to_print = "D:\\Code\\python\\searcher\\notes.txt"

# Tell Windows to print the file
# This is a non-blocking call, and a print dialog may appear depending on the file type
os.startfile(file_to_print, "print")

print("Print job sent.")
