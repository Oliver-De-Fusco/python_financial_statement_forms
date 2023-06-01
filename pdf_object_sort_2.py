import os
from itertools import cycle

from dateutil.relativedelta import *

from pdf_reader import document


def expected_seqeunce(start, end):

    expected = [start]

    while expected[-1] < end:

        # you have to specify "months" not "month" otherwise the initial month will become January
        next_month = expected[-1] + relativedelta(months=3)
        expected.append(next_month)

    return expected


def truncate_day(input):
    return str(input)[:-3]


def truncate_day_generator(input_list):

    for x in input_list:
        yield truncate_day(x)


def remove_duplicates(input_list):

    output = [input_list[0]]
    duplicates = []

    for report in input_list:
        if truncate_day(report.date_ended) == truncate_day(output[-1].date_ended):
            duplicates.append(report)
        else:
            output.append(report)

    return output, duplicates[1:]


def fill_missing_gaps(input_list, expected_list, fill_value=None):

    # we only care about comparing years and months so remove days
    input_dates = list(truncate_day(x.date_ended) for x in report_list)

    # By comparing the expected vs actual 
    # we know when to insert a new value into the original list by looping over it
    for index, expected_date in enumerate(expected_list):
        if not expected_date in input_dates:
            input_list.insert(index, fill_value)

    return input_list


def find_first_10K(input_list):

    for index, report in enumerate(input_list):
        if report:
            if report.report_type == "10-K":
                return index


def sort_files(input_files, generator):
    first_k_10 = find_first_10K(input_files)

    # prep the generator for the sequence
    # if you altered the length of the generator you need to change this as well
    for _ in range(4 - first_k_10):
        next(generator)
    for report in input_files:
        # Thanks to the fill_missing_gaps() generating the correct sequence is incredibly easy
        if report:
            report.set_name(
                f"{report.company} - {report.date_ended.year} {next(generator)}")
        else:
            next(generator)


# Code starts here
if __name__ == "__main__":

    # get the pdf files in current directory
    report_list = [document(filename) for filename in os.listdir(".")
                   if os.path.isfile(filename) if filename[-4:] == ".pdf"]

    # remove files from list that data was not able to be found for
    report_list = [report for report in report_list if (
        report.company or report.date_ended or report.report_type)]

    # The list has to be sorted by date and have no duplicates
    report_list.sort(key=lambda document: document.date_ended)
    report_list, duplicates = remove_duplicates(report_list)

    # Handle duplicate reports
    for dup in duplicates:
        dup.set_name(f"Duplicate - {dup.name}")

    # generator has to be able to cycle through the sequence
    generator = cycle(("Annual Report", "Q1", "Q2", "Q3"))

    # we generate a list of the expected dates then remove the day from each
    expected_report_dates = list(truncate_day_generator(
        expected_seqeunce(report_list[0].date_ended, report_list[-1].date_ended)))

    # using the previously created variables we can fill in the gaps of the reports
    report_list = fill_missing_gaps(
        report_list, expected_report_dates)

    # sort the files with the names
    sort_files(report_list, generator)
