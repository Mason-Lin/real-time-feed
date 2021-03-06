import unittest

import feed_parser
from feed_parser import Feed


class TestParser(unittest.TestCase):
    def test_get_most_active_symbol_only_one(self):
        trading_day_feed = [
            Feed(date="2017-01-03", symbol="AAPL"),
            Feed(date="2017-01-03", symbol="AMD"),
            Feed(date="2017-01-03", symbol="AAPL"),
            Feed(date="2017-01-03", symbol="AMZN"),
            Feed(date="2017-01-03", symbol="AAPL"),
            Feed(date="2017-01-03", symbol="FB"),
        ]
        actual = feed_parser._get_most_active_symbol(trading_day_feed)
        expected = "AAPL"
        assert actual == expected

    def test_get_most_active_symbol_more_than_one(self):
        trading_day_feed = [
            Feed(date="2017-01-03", symbol="FB"),
            Feed(date="2017-01-03", symbol="FB"),
            Feed(date="2017-01-03", symbol="AAPL"),
            Feed(date="2017-01-03", symbol="FB"),
            Feed(date="2017-01-03", symbol="AAPL"),
            Feed(date="2017-01-03", symbol="AAPL"),
        ]
        actual = feed_parser._get_most_active_symbol(trading_day_feed)
        expected = "AAPL"
        assert actual == expected

    def test_get_most_active_hour_only_one(self):
        trading_day_feed = [
            Feed(date="2017-01-03", time="16:18:50"),
            Feed(date="2017-01-03", time="16:25:22"),
            Feed(date="2017-01-03", time="16:25:25"),
            Feed(date="2017-01-03", time="16:25:28"),
            Feed(date="2017-01-03", time="16:28:50"),
            Feed(date="2017-01-03", time="16:29:59"),
        ]
        actual = feed_parser._get_most_active_hour(trading_day_feed)
        expected = "16"
        assert actual == expected

    def test_get_most_active_hour_more_than_one(self):
        trading_day_feed = [
            Feed(date="2017-01-03", time="12:18:50"),
            Feed(date="2017-01-03", time="12:25:22"),
            Feed(date="2017-01-03", time="14:25:25"),
            Feed(date="2017-01-03", time="14:25:28"),
            Feed(date="2017-01-03", time="16:28:50"),
            Feed(date="2017-01-03", time="16:29:59"),
        ]
        actual = feed_parser._get_most_active_hour(trading_day_feed)
        expected = "12"
        assert actual == expected

    def test_get_price_statistics(self):
        trading_day_feed = [
            Feed(
                date="2017-01-03",
                time="16:18:50",
                symbol="AAPL",
                price="142.64",
            ),
            Feed(
                date="2017-01-03", time="16:25:22", symbol="AMD", price="13.86"
            ),
            Feed(
                date="2017-01-03",
                time="16:25:25",
                symbol="AAPL",
                price="141.64",
            ),
            Feed(
                date="2017-01-03",
                time="16:25:28",
                symbol="AMZN",
                price="845.61",
            ),
            Feed(
                date="2017-01-03",
                time="16:28:50",
                symbol="AAPL",
                price="140.64",
            ),
            Feed(
                date="2017-01-03", time="16:29:59", symbol="FB", price="140.34"
            ),
        ]
        actual_price_statistics = feed_parser._get_price_statistics(
            trading_day_feed
        )
        expected = {
            "AAPL": {
                "date": "2017-01-03",
                "time": "16:28:50",
                "high": "142.64",
                "low": "140.64",
            },
            "AMD": {
                "date": "2017-01-03",
                "time": "16:25:22",
                "high": "13.86",
                "low": "13.86",
            },
            "AMZN": {
                "date": "2017-01-03",
                "time": "16:25:28",
                "high": "845.61",
                "low": "845.61",
            },
            "FB": {
                "date": "2017-01-03",
                "time": "16:29:59",
                "high": "140.34",
                "low": "140.34",
            },
        }
        assert expected == actual_price_statistics


if __name__ == "__main__":
    unittest.main(verbosity=2)
