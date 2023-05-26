from PyPDF2 import PdfReader
from datetime import date
from string import printable
import os

def find_document_end_date(document_path):

    MONTHS = ("January","February","March","April","May","June","July","August","September","October","November", "December")
    reader = PdfReader(document_path)

    for index, page in enumerate(reader.pages):
        if index == 0:
            text = page.extract_text()
            break

    # clean up
    text = text.title()
    text = text.replace("  "," ")
    text = text.replace(",", " ")
    text = text.split()

    error_list = [("Decembe","December")]

    print(text)

    output_text = text.copy()[:200]

    for error in error_list:
        if error[0] in text:
            output_text[text.index(error[0])] = error[1]
            output_text.pop(text.index(error[0]) + 1)

    for index, word in enumerate(output_text):

        if word in MONTHS:
            month_found = index

    for char in printable.replace("0123456789",""): # removes all characters that are not numbers
        output_text[month_found+2] = output_text[month_found+2].lower().replace(char,"")
    
    day = int(output_text[month_found+1])
    month = MONTHS.index(output_text[month_found]) + 1
    year = int(output_text[month_found+2])

    return date(int(year),month,day) # Returns a datetime object 

class document:
    def __init__(self,name, path=os.getcwd()):
        self.name = name

        # print(self.name)
        self.directory = path
        
        # Path location
        
        for root, dirs, files in os.walk(path):
            if name in files:
                self.path = os.path.join(root, name)
            else:
                self.path = os.path.join(path, name)

        self.date_ended = find_document_end_date(name)

    def set_name(self,name):
        os.rename(self.path, os.path.join(self.directory, name))

    def __repr__(self) -> str:
        return f"document(name={repr(self.name)}, date_ended={repr(self.date_ended)})"
    
    def __str__(self) -> str:
        return self.name