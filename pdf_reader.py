import os
from datetime import date
from string import printable, digits

from pypdf import PdfReader


def document_text_processor(document_path):
    """Returns the text on the first page of a pdf file

    append to errors list in document manually if words are spelt incorrectly, use form (error, correction)
    """

    reader = PdfReader(document_path)

    # extract first page of the generator function
    for page in reader.pages:

        text = page.extract_text()

        if text:
            break

    # clean up
    text = text.title()
    text = text.replace("  ", " ")
    text = text.replace(",", " ")
    text = text.split()

    # we copy text for the error loop as we cannot edit strings as we use them
    output_text = text.copy()[:300]

    # add errors to this list
    # use form (error, correction)
    error_list = [("Decembe", "December")]
    for error in error_list:
        if error[0] in text:
            output_text[text.index(error[0])] = error[1]
            output_text.pop(text.index(error[0]) + 1)

    return output_text


def find_quater_report(text):

    """Returns the Datetime object of the report. Returns None if nothing is found

    This works becuase of form "MM DD YYYY", finding the month first means we have also found the day and year by adding an offset
    """

    MONTHS = ("January", "February", "March", "April", "May", "June",
              "July", "August", "September", "October", "November", "December")

    month_found = None
    for index, word in enumerate(text):
        if word in MONTHS:
            
            month_found = index
            break

    if not month_found:
        return None

    # Year or Day can contain other substrings when they should be only numbers
    for char in printable.replace(digits, ""):
        text[month_found+1] = text[month_found+1].lower().replace(char, "")
        text[month_found+2] = text[month_found+2].lower().replace(char, "")

    # month found could contain digits when only letters should be present
    for digit in digits:
        text[month_found] = text[month_found].replace(digit, "")

    year = int(text[month_found+2])
    # Adding one to month as lists begin at zero but months begin at one
    month = MONTHS.index(text[month_found]) + 1
    day = int(text[month_found+1])

    return date(int(year), month, day)


def find_company_name(text):
    """Attempts to find company name on form.

    This is likely to not be accurate. Jpmorgan for example is one it has trouble with

    Becuase of this it is best to run a cleanup script after to fix the errors by replacing them with the actual name

    If you already know the documents have the same company name this step can be skipped and the company name can be set manually
    """

    company_name_location_start, company_name_location_end = 0, 0

    for index, word in enumerate(text):

        for substring in ("Number", "No"):
            if substring in word:
                company_name_location_start = index
                break

        if "Exact" in word:
            company_name_location_end = index
            break

    if not (company_name_location_start and company_name_location_end):
        return None

    # array of company name
    company_name = text[company_name_location_start +
                        2: company_name_location_end]

    # add a space between the words
    output_name = []
    for word in company_name:
        output_name.append(word)
        output_name.append(" ")



    # remove any white space and underscores
    output_name = "".join(output_name).strip()
    output_name = output_name.replace("_", "")


    return " ".join(str(output_name).split()).strip()


class document:
    def __init__(self, name, directory=os.getcwd(), company=None, report_type=None, date=None):
        """Initialise the document object

        Variables:
        name        : Current filename of the document
        directory   : The current folder the pdf is in.
        company     : Can be set manually otherwise will be automatically found.
        report_type : Optional for manually setting the form type.
        date        : Optional for manually setting date of the object
        """

        self.name = name
        self.directory = directory

        # Exact File location
        for root, dirs, files in os.walk(directory):
            if name in files:
                self.path = os.path.join(root, name)
                break

        document_text = document_text_processor(name)

        # data
        if company:
            self.company = company
        else:
            self.company = find_company_name(document_text)

        if report_type:
            self.report_type = report_type
        else:
            self.report_type = document.find_report_type(document_text)

        if date:
            self.date_ended = date
        else:
            self.date_ended = find_quater_report(document_text)

    def find_report_type(text):
        """Retuns report type"""

        report_type = ("10-K", "10-Q")
        for word in text:
            if word in report_type:
                return word
        return None

    def set_name(self, name, log=False):
        """Renames the object"""

        # Safety net
        if name[:-4] != ".pdf":
            if self.name[:-4] != ".pdf":
                name += ".pdf"


        os.rename(self.path, os.path.join(self.directory, name))
        self.name = name

        if log:
            print(f"{self.name} -> {name}")

        return True
