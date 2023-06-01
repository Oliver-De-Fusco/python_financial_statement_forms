import os
from datetime import date
from string import printable, digits

from pypdf import PdfReader


def document_text_processor(document_path):

    reader = PdfReader(document_path)

    # extract first page of the generator function
    for index, page in enumerate(reader.pages):
        if index == 0:
            text = page.extract_text()
            break

    # clean up
    text = text.title()
    text = text.replace("  ", " ")
    text = text.replace(",", " ")
    text = text.split()

    # we copy text for the error loop as we cannot edit strings as we use them
    output_text = text.copy()[:200]

    # I gave up so just add error to this list
    # use form (error, correction)
    error_list = [("Decembe", "December")]
    for error in error_list:
        if error[0] in text:
            output_text[text.index(error[0])] = error[1]
            output_text.pop(text.index(error[0]) + 1)

    return output_text


def find_quater_report(text):

    # All the forms begin with a dated period in format -> MONTH DAY YEAR
    # By finding the index of the first mention of month we can find the rest of the date by offset values
    # Loop becuase index can only find a single value at any time
    MONTHS = ("January", "February", "March", "April", "May", "June",
              "July", "August", "September", "October", "November", "December")

    month_found = None
    for index, word in enumerate(text):
        if word in MONTHS:
            month_found = index

    if not month_found:
        return None

    # while this alternative code does work it is bad practice to have 11 errors for each input
    # for month in MONTHS:
    #     try:
    #         month_found = text.index(month)
    #     except ValueError:
    #         continue

    # post processing

    # Year date can contain other letters such as Or as a result of the previous processing

    for char in printable.replace(digits, ""):
        text[month_found+2] = text[month_found+2].lower().replace(char, "")

    year = int(text[month_found+2])
    month = MONTHS.index(text[month_found]) + 1
    day = int(text[month_found+1])

    # Returns a datetime object to manipulate easier
    return date(int(year), month, day)


def find_company_name(text):

    company_name_location_start, company_name_location_end = 0, 0

    for index, word in enumerate(text):
        if "Number" in word:
            company_name_location_start = index

        if "Exact" in word:
            company_name_location_end = index
            break

    if not (company_name_location_start and company_name_location_end):
        return None

    # array of company name
    company_name = text[company_name_location_start +
                        2: company_name_location_end]

    # add a space between the words
    output_name = [company_name[0]]

    for index, word in enumerate(company_name):
        if (index) % 2 == 0:
            # print(word)
            output_name.append(" ")
        else:
            output_name.append(word)

    # remove any white space
    output_name = "".join(output_name).strip()
    return " ".join(output_name.split())


class document:
    def __init__(self, name, path=os.getcwd()):

        self.name = name
        self.directory = path

        # File location
        for root, dirs, files in os.walk(path):
            if name in files:
                self.path = os.path.join(root, name)
            else:
                self.path = os.path.join(path, name)

        document_text = document_text_processor(name)

        # data
        self.company = find_company_name(document_text)
        self.report_type = document.find_report_type(document_text)
        self.date_ended = find_quater_report(document_text)

    def find_report_type(text):

        report_type = ("10-K", "10-Q")
        for word in text:
            if word in report_type:
                return word
        return None

    def set_name(self, name, log=False):

        # Safety net
        if name[:-4] != ".pdf":
            if self.name[:-4] != ".pdf":
                name += ".pdf"

        os.rename(self.path, os.path.join(self.directory, name))
        self.name = name

        if log:
            print(f"{self.name} -> {name}")

        return True

    def move_file(self, destination, log=False):
        os.rename(self.path, os.path.join(destination, self.name))
        self.directory = destination

        if log:
            print(f"{self.path} -> {os.path.join(destination, self.name)}")

    def __repr__(self) -> str:
        return f"document(name={repr(self.name)}, date_ended={repr(self.date_ended)})"

    def __str__(self) -> str:
        return self.name
