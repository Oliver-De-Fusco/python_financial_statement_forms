import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))

from datetime import date
import pof2


class mock_report:
    def __init__(self, date=None, company=None) -> None:
        self.date_ended = date
        self.company = company

    def __repr__(self) -> str:
        return f"mock_report(date_ended=date({self.date_ended}), company={self.company})"
    


class TestExpected_sequence:
    def test_normal(self):
        assert pof2.expected_seqeunce(date(2000,1,1),date(2001,1,1)) == [date(2000, 1, 1), date(2000, 4, 1), date(2000, 7, 1), date(2000, 10, 1), date(2001, 1, 1)]
    def test_new_millennium(self):
        assert pof2.expected_seqeunce(date(2999,1,1),date(3000,1,1)) == [date(2999, 1, 1), date(2999, 4, 1), date(2999, 7, 1), date(2999, 10, 1), date(3000, 1, 1)]
    def test_new_digit(self):
        assert pof2.expected_seqeunce(date(999,1,1),date(1000,1,1)) == [date(999,1,1), date(999,4,1), date(999,7,1), date(999,10,1), date(1000,1,1)]
    def test_end_less_than(self):
        assert pof2.expected_seqeunce(date(2001,1,1),date(2000,1,1)) == [date(2001, 1, 1)]


class TestTruncate_day:
    def test_normal(self):
        assert pof2.truncate_day(date(2000,1,1)) == "1999-12"
        assert pof2.truncate_day(date(2000,1,5)) == "2000-01"


class TestRemove_duplicates:
    input_list = [mock_report(date=date(2000,1,1)),mock_report(date=date(2000,1,1)),mock_report(date=date(2000,1,1))]

    def test_normal(self):
        assert pof2.remove_duplicates(TestRemove_duplicates.input_list) == ([TestRemove_duplicates.input_list[0]], TestRemove_duplicates.input_list[1:])


class Testfill_missing_gaps:
    input_list = [mock_report(date=date(2000,1,1)), mock_report(date=date(2000,7,1)), mock_report(date=date(2000,10,1)), mock_report(date=date(2001,4,1))]
    expected_report_dates = list((pof2.expected_seqeunce(input_list[0].date_ended, input_list[-1].date_ended)))

    def test_normal(self):
        assert pof2.fill_missing_gaps(Testfill_missing_gaps.input_list, Testfill_missing_gaps.expected_report_dates) == [Testfill_missing_gaps.input_list[0], None, Testfill_missing_gaps.input_list[1], Testfill_missing_gaps.input_list[2], None, Testfill_missing_gaps.input_list[3]]

if __name__ == "__main__":

    # print(Testfill_missing_gaps.test_normal(""))

    """
[Testfill_missing_gaps.input_list[0], None, Testfill_missing_gaps.input_list[1], Testfill_missing_gaps.input_list[2], None]
[mock_report(date=date(2000-01-01), company=None), None, mock_report(date=date(2000-07-01), company=None), mock_report(date=date(2000-10-01), company=None), None]"""