import os
from itertools import cycle

from dateutil.relativedelta import *

from pdf_reader import document


def expected_seqeunce(start, end):
    """Returns a sequence of datetime objects that increments by 3 months based on the start and end period."""

    expected = [start]

    while expected[-1] < end:

        # you have to specify "months" not "month" otherwise the initial month will become January
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


def truncate_day_generator(input_list):
    """This is a helper function, see truncate_day()."""

    for x in input_list:
        yield truncate_day(x)


def remove_duplicates(input_list):
    """Removes objects with the same end date, discarding one and keeping the other."""

    output = [input_list[0]]
    duplicates = []

    for report in input_list:
        if truncate_day(report.date_ended) == truncate_day(output[-1].date_ended):
            duplicates.append(report)
        else:
            output.append(report)

    return output, duplicates[1:]


def fill_missing_gaps(input_list, expected_list, fill_value=None):
    """Returns a list based on the expected list where any missing dates are filled."""

    # we only care about comparing years and months so remove days
    input_dates = list(truncate_day(x.date_ended) for x in report_list)

    # By comparing the expected vs actual
    # we know when to insert a new value into the original list by looping over it
    for index, expected_date in enumerate(expected_list):
        if not expected_date in input_dates:
            input_list.insert(index, fill_value)

    return input_list


def rename_report_files(input_files, generator):
    """Renames the input files in a sequence based on the generator.

    generator has to be a generator function or list, I reccomend itertools.cycle().
    If the function has a differnt length than 4 then modify:

    for _ in range(4 - first_k_10):

    Change the value of 4 to the length of the generator or removing the loop if you want a sequence that increments infinitely.
    """

    for index, report in enumerate(input_files):
        if report:
            if report.report_type == "10-K":
                first_k_10 = index

    # prep the generator for the sequence
    # if you altered the length of the generator you need to change this as well
    for _ in range(4*len(input_files) - first_k_10):
        next(generator)

    for report in input_files:
        # Thanks to the fill_missing_gaps() generating the correct sequence is incredibly easy
        if report:

            # print(f"{report.name} {report.report_type} ")
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

    # The list has to be sorted by date
    report_list.sort(key=lambda document: document.date_ended)

    # Remove duplicates
    report_list, duplicates = remove_duplicates(report_list)

    # Handle duplicate reports
    for dup in duplicates:
        dup.set_name(f"Duplicate - {dup.name}")

    # we generate a list of the expected dates then remove the day from each using list comprehension
    expected_report_dates = list(truncate_day_generator(
        expected_seqeunce(report_list[0].date_ended, report_list[-1].date_ended)))

    # using the previously created variables we can fill in the gaps of the reports
    report_list = fill_missing_gaps(report_list, expected_report_dates)

    # generator has to be able to cycle through a sequence
    generator = cycle(("Annual Report", "Q1", "Q2", "Q3"))

    # sort the files with the names
    rename_report_files(report_list, generator)
