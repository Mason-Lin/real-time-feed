# TODO create test folder, pytest.ini, conftest.py if needed.
import unittest
import feed_parser


class TestParser(unittest.TestCase):
    def test_get_most_active_symbol_only_one(self):
        data_format_row = [
            {"date": "2017-01-03", "symbol": "AAPL"},
            {"date": "2017-01-03", "symbol": "AMD"},
            {"date": "2017-01-03", "symbol": "AAPL"},
            {"date": "2017-01-03", "symbol": "AMZN"},
            {"date": "2017-01-03", "symbol": "AAPL"},
            {"date": "2017-01-03", "symbol": "FB"},
        ]
        trading_day = "2017-01-03"
        actual = feed_parser.get_most_active_symbol(data_format_row, trading_day)
        expected = "AAPL"
        assert actual == expected

    def test_get_most_active_symbol_more_than_one(self):
        data_format_row = [
            {"date": "2017-01-03", "symbol": "FB"},
            {"date": "2017-01-03", "symbol": "FB"},
            {"date": "2017-01-03", "symbol": "AAPL"},
            {"date": "2017-01-03", "symbol": "FB"},
            {"date": "2017-01-03", "symbol": "AAPL"},
            {"date": "2017-01-03", "symbol": "AAPL"},
        ]
        trading_day = "2017-01-03"
        actual = feed_parser.get_most_active_symbol(data_format_row, trading_day)
        expected = "AAPL"
        assert actual == expected

    def test_get_most_active_hour_only_one(self):
        data_format_row = [
            {"date": "2017-01-03", "time": "16:18:50"},
            {"date": "2017-01-03", "time": "16:25:22"},
            {"date": "2017-01-03", "time": "16:25:25"},
            {"date": "2017-01-03", "time": "16:25:28"},
            {"date": "2017-01-03", "time": "16:28:50"},
            {"date": "2017-01-03", "time": "16:29:59"},
        ]
        trading_day = "2017-01-03"
        actual = feed_parser.get_most_active_hour(data_format_row, trading_day)
        expected = "16"
        assert actual == expected

    def test_get_most_active_hour_more_than_one(self):
        data_format_row = [
            {"date": "2017-01-03", "time": "12:18:50"},
            {"date": "2017-01-03", "time": "12:25:22"},
            {"date": "2017-01-03", "time": "14:25:25"},
            {"date": "2017-01-03", "time": "14:25:28"},
            {"date": "2017-01-03", "time": "16:28:50"},
            {"date": "2017-01-03", "time": "16:29:59"},
        ]
        trading_day = "2017-01-03"
        actual = feed_parser.get_most_active_hour(data_format_row, trading_day)
        expected = "12"
        assert actual == expected


if __name__ == "__main__":
    unittest.main(verbosity=2)