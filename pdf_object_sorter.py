
# From 10k work backwards
# IE 10k released end of december so Q4 is december to september, Q3 is september to june etc, sort by start date
# go back to document and rename each file to {quarter period}Q{year}
# sort files

from pdf_reader import document
import os

#yearly_reports = ("0000070858-17-000037.pdf", "0000070858-17-000046.pdf","0000070858-17-000025.pdf","0000070858-18-000009.pdf","0000070858-18-000042.pdf")

yearly_reports = []

for root, dirs, files in os.walk(os.getcwd()):
    for filename in files:
        #print(filenames[:])
        if filename[-3:] == "pdf":
            yearly_reports.append(filename)


yearly_reports_documents = [document(i) for i in yearly_reports]

MONTHS = ("January","February","March","April","May","June","July","August","September","October","November","December")

def sort_key_year(e):
    return e.date_period[0][1]

def sort_key_month(e):
    return MONTHS.index(e.date_period[0][0])

yearly_reports_documents.sort(key=sort_key_year)
yearly_reports_documents.sort(key=sort_key_month)



def fiscal_year_documents(documents_list):

    return_list = [] 

    for documents in documents_list:
        if documents.K_10:
            #If the document is a 10k then create a list with the document as the head
            connected_documents = [documents]

            def find_previous_document(document, list):

                # Loop through the list given until you find a quarterly report with the end date before the start date of the prevoius document
                for quarterly_report in list:
                    if quarterly_report.date_end[:2] == (document.start_date[1], MONTHS[MONTHS.index(document.start_date[0])-1]):
                        #return that report
                        return quarterly_report

            # do this 3 times to get the full list for the financial quarter
            while len(connected_documents) <= 3:
                connected_documents.append(find_previous_document(connected_documents[-1], documents_list))

            #add the fiscal year documents onto the return list, this will be in order starting with the 10k
            return_list.append(connected_documents)
    
    return return_list
        

def rename_connected_documents(documents_list):

    for i in documents_list:
        print(repr(i))
        i.name = f"{4-documents_list.index(i)}Q{i.start_date[1]-2000}.pdf"

        # Different name for Q4's 
        if i.name[:2] == "4Q":
            i.name = f"4Q{i.start_date[1]-2000} Annual report.pdf"


for i in fiscal_year_documents(yearly_reports_documents):
    rename_connected_documents(i)
    for o in i:
        o.set_name(o.name)