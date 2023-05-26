from pdf_reader import document
import os

reports = [document(filename) for filename in os.listdir(".") if os.path.isfile(filename) if filename[-3:] == "pdf"]

reports.sort(key=lambda document:document.date_ended)

def q_generator():
    while True:
        for i in range(4):
            yield i + 1

for report, quater in zip(reports, q_generator()):
    if report.name == f"{report.date_ended.year}Q{quater} - {report.date_ended}.pdf":
        continue
    else:
        print(f"{report} --> {report.date_ended.year}Q{quater} - {report.date_ended}.pdf")
        report.set_name(f"{report.date_ended.year}Q{quater} - {report.date_ended}.pdf")