import pdf_object_sort_2
from datetime import date


class mock_report:
    def __init__(self) -> None:
        self.date_ended = date(2000,1,1)

    def __repr__(self) -> str:
        return "report"


class TestExpected_sequence:
    def test_normal(self):
        assert pdf_object_sort_2.expected_seqeunce(date(2000,1,1),date(2001,1,1)) == [date(2000, 1, 1), date(2000, 4, 1), date(2000, 7, 1), date(2000, 10, 1), date(2001, 1, 1)]
    def test_new_millennium(self):
        assert pdf_object_sort_2.expected_seqeunce(date(2999,1,1),date(3000,1,1)) == [date(2999, 1, 1), date(2999, 4, 1), date(2999, 7, 1), date(2999, 10, 1), date(3000, 1, 1)]
    def test_new_digit(self):
        assert pdf_object_sort_2.expected_seqeunce(date(999,1,1),date(1000,1,1)) == [date(999,1,1), date(999,4,1), date(999,7,1), date(999,10,1), date(1000,1,1)]
    def test_end_less_than(self):
        assert pdf_object_sort_2.expected_seqeunce(date(2001,1,1),date(2000,1,1)) == [date(2001, 1, 1)]


class TestTruncate_day:
    def test_normal(self):
        assert pdf_object_sort_2.truncate_day(date(2000,1,1)) == "1999-12"
        assert pdf_object_sort_2.truncate_day(date(2000,1,5)) == "2000-01"


class TestRemove_duplicates:
    input_list = [mock_report(),mock_report(),mock_report()]

    def test_normal(self):
        assert pdf_object_sort_2.remove_duplicates(TestRemove_duplicates.input_list) == ([TestRemove_duplicates.input_list[0]], TestRemove_duplicates.input_list[1:])