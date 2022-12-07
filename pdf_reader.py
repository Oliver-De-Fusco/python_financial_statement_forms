from PyPDF2 import PdfReader
import os

def find_document_end_date(document_name,find_string="Quarterly Period Ended"):
    
    #Code copied from stack overflow, tried using pdfminer but lack of documentation made it more difficult 
    reader = PdfReader(document_name)
    for index, page in enumerate(reader.pages):
        if index == 0:
            text = page.extract_text()
            break
    #end

    #clean up
    text = text.title()
    text = text.replace("\n","")#"Quarterly  Period Ended"
    text = text.replace("  "," ")
    
    #find
    try:
        location = text.index(find_string)
        K_10 = False
    except ValueError:
        find_string = "Fiscal Year Ended"
        K_10 = True
        location = text.index(find_string)

    #find range of data then trim by removing new lines and spaces
    estimated_end_date_location = text[location+len(find_string): location + 60].strip()


    #Year should always be last so finding the last digit included
    #Figure out if this covers edge cases
    last_Digit_Found_Index = 0

    for index, character in enumerate(estimated_end_date_location):

        if character.isdigit():
            last_Digit_Found_Index = index

    
    end_date_location_processed = estimated_end_date_location[:1+last_Digit_Found_Index].replace(",","").split()
    #Month, day , year

    end_date_iso_format = (int(end_date_location_processed[2]), (end_date_location_processed[0]), int(end_date_location_processed[1]))
    #year month day

    return end_date_iso_format[0:2], K_10



def get_document_period(extracted_end_month, end_year):

    print(extracted_end_month)

    MONTHS = ("January","February","March","April","May","June","July","August","September","October","November","December")

    start_month = MONTHS[MONTHS.index(extracted_end_month) - 2] #Because report includes current month

    if MONTHS.index(extracted_end_month) - 2 < 0: # should the start period be January to March the period started the prevoius year 
        start_year = end_year - 1
    else:
        start_year = end_year

    #Returns 2 dimensional tuple
    #getdocumentperiod(extracted_end_month, end_year)[0][1] will result in start year
    return ((start_month, start_year), (extracted_end_month, end_year))

# create document objects

class document:
    def __init__(self,name ,date_end=None,date_period=None, path=os.getcwd(), K_10=False):
        self.name = name

        #print(self.name)
        self.directory = path
        
        # Path location
        for root, dirs, files in os.walk(path):
            if name in files:
                self.path = os.path.join(root, name)
            else:
                self.path = os.path.join(path, name)

        if date_end is None:
            self.date_end, self.K_10 = find_document_end_date(name)
        else:
            self.date_end, self.K_10 = date_end, K_10
        
        #("start", "end")
        if date_period is None:
            
            self.date_period = get_document_period(self.date_end[1].capitalize(),self.date_end[0])
        else:
            self.date_period = date_period

        #print(self.date_period)
        self.start_date = self.date_period[0]

    def set_name(self,name):
        os.rename(self.path, os.path.join(self.directory, name))

    def __repr__(self) -> str:
        return f"document(name={repr(self.name)}, date_end={repr(self.date_end)}, date_period={repr(self.date_period)}, path={repr(self.path)}, K_10={repr(self.K_10)})"
    
    def __str__(self) -> str:
        return self.name