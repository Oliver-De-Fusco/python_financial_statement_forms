import os
from itertools import cycle
from dateutil.relativedelta import *
from pdf_reader import document


def expected_seqeunce(start, end):
    """Returns a sequence of datetime objects that increments by 3 months based on the start and end period.
    """

    expected = [start]

    while expected[-1] < end:

        next_month = expected[-1] + relativedelta(months=3)
        expected.append(next_month)

    return expected


def truncate_day(date_input):
    """Returns just month and year of a datetime object.

    There are scenarios where a company may have the period end on the 1st instead of the 30th/31st
    to account for this we have to subtract a month to account for this decision.

    Check date ended on the documents and modify this function accordingly.
    """

    if (date_input.day == 1) or (date_input.day == 2) or (date_input.day == 3):
        date_input = date_input + relativedelta(months=-1)

    return str(date_input)[:-3]


def remove_duplicates(input_list):
    """Removes objects with the same end date, discarding one and keeping the other.
    """

    output = [input_list[0]]
    duplicates = []

    for report in input_list:
        if truncate_day(report.date_ended) == truncate_day(output[-1].date_ended):
            duplicates.append(report)
        else:
            output.append(report)

    return output, duplicates[1:]


def fill_missing_gaps(input_list, expected_list):
    """Returns a list based on the expected list where any missing dates are filled.
    """

    # we only care about comparing years and months so remove days
    input_dates = list(map(lambda x: truncate_day(x.date_ended), input_list))
    expected_dates = list(map(truncate_day, expected_list))
    output = []

    # By checking if the current date is in the input list, insert none if it does not exist
    index = 0
    for expected_date in expected_dates:
        if expected_date in input_dates:
            output.append(input_list[index])
            index += 1
        else:
            output.append(None)
    
    return output


def rename_report_files(input_files, generator):
    """Renames the input files in a sequence based on the generator.

    Generator needs to be a generator function, use itertools.cycle().
    """

    for x in input_files:
        next(generator)
        if x:
            if x.report_type == "10-K":
                break

    for report in input_files:
        report_type = next(generator)
        if report:
            report.set_name(f"{report.company} - {report.date_ended.year} {report_type}")
        

def main():
    # get the pdf files
    report_list = [document(filename) for filename in os.listdir(".")
                   if os.path.isfile(filename) if filename[-4:] == ".pdf"]

    # remove files from list when no data was able to be found
    report_list = [report for report in report_list if (report.company or report.date_ended or report.report_type)]

    # The list has to be sorted by date
    report_list.sort(key=lambda document: document.date_ended)

    # seperate duplicates
    report_list, duplicates = remove_duplicates(report_list)

    # Handle duplicates
    if not os.path.exists("duplicates"):
        os.mkdir("duplicates")

    for dup in duplicates:
        dup.set_name(os.path.join("duplicates", dup.path))

    # generate a list of the expected dates
    expected_report_dates = expected_seqeunce(report_list[0].date_ended, report_list[-1].date_ended)
    
    # fill in the date gaps in the reports
    report_list = fill_missing_gaps(report_list, expected_report_dates)

    # generator has to be able to cycle through a sequence
    generator = cycle(("Q1", "Q2", "Q3", "Q4"))

    # rename the files with the names
    rename_report_files(report_list, generator)

if __name__ == "__main__":
    main()
    
