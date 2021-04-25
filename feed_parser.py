import logging
from collections import Counter, OrderedDict, defaultdict
from dataclasses import dataclass
from io import StringIO
from operator import itemgetter

input = """8
2017-01-03,16:18:50,AAPL,142.64
2017-01-03,16:25:22,AMD,13.86
2017-01-03,16:25:25,AAPL,141.64
2017-01-03,16:25:28,AMZN,845.61
2017-01-03,16:28:50,AAPL,140.64
2017-01-03,16:29:59,FB,140.34
2017-01-04,16:29:32,AAPL,143.64
2017-01-04,16:30:50,AAPL,141.64
"""


@dataclass
class Feed:
    date: str = None
    time: str = None
    symbol: str = None
    price: str = None


class DailyFeed:
    """The exchange starts trading daily at 09:30:00 hrsand closes at 16:30:00 hrsevery day
    Any quotes outside this time window are invalid and will be ignored.
    Input:
        StringIO
    """

    def __init__(self, input):
        self._input_data = input
        self._feeds = defaultdict(list)
        self.input_total_rows = next(self._input_data).strip()

    @staticmethod
    def _is_valid_trading(time):
        return "09:30:00" < time < "16:30:00"

    @staticmethod
    def _extract_feed_from_line(line):
        splited = line.strip().split(",")
        date = splited[0]
        time = splited[1]
        symbol = splited[2].upper()
        price = splited[3]
        return Feed(date, time, symbol, price)

    def get_trading_day_feeds(self):
        trading_day_feeds = None
        for _ in range(int(self.input_total_rows)):
            feed = self._extract_feed_from_line(self._input_data.readline())

            if not self._is_valid_trading(feed.time):
                continue

            self._feeds[feed.date].append(feed)

            if trading_day_feeds and trading_day_feeds[0].date != feed.date:
                yield trading_day_feeds

            trading_day_feeds = self._feeds[feed.date]
        else:
            # last trading day
            yield trading_day_feeds


def _get_most_active_hour(trading_day_feed):
    cnt = Counter(feed.time.split(":")[0] for feed in trading_day_feed)  # HH:MM:SS
    sorted_most_common = sorted(cnt.most_common(), key=itemgetter(0))
    # [0][0] means get hour from [('12', 3), ('16', 3)]
    return sorted_most_common[0][0]


def _get_most_active_symbol(trading_day_feed):
    cnt = Counter(feed.symbol for feed in trading_day_feed)
    sorted_most_common = sorted(cnt.most_common(), key=itemgetter(0))
    return sorted_most_common[0][0]


def _get_last_quote_time(trading_day_feed):
    return trading_day_feed[-1].time


def _get_valid_quote_count(trading_day_feed):
    return len(trading_day_feed)


def _get_price_statistics(trading_day_feed):
    """Calculate and print the following data for each Symbol as a comma-delimiter string.
    Rows should be printed in alphabetical order based on Symbol

        i. Time: Most recent timestamp for that Symbol in YYYY-mm-dd HH:MM:SS format
        ii. Symbol
        iii. High: Maximum Price that occurred for that Symbol during the trading day.
        iv. Low: Minimum Price that occurred for that Symbol during the trading day
    """
    stat = dict()
    for feed in trading_day_feed:
        symbol = feed.symbol
        if stat.get(symbol):
            prev_feed = stat[symbol]
            prev_feed["time"] = max(prev_feed["time"], feed.time)
            prev_feed["high"] = max(prev_feed["high"], feed.price)
            prev_feed["low"] = min(prev_feed["low"], feed.price)
        else:
            stat[symbol] = {
                "date": feed.date,
                "time": feed.time,
                "high": feed.price,
                "low": feed.price,
            }

    # alphabetical order based on Symbol
    price_statistics = OrderedDict.fromkeys(sorted(stat.keys()))
    for symbol, symbol_info in stat.items():
        price_statistics[symbol] = symbol_info
    return price_statistics


#
# Public API
#


def print_trading_summary(feed):
    """After exchange closes at 16:30:00 for each trading day, print

    1. Trading Day = <Date>
    2. Last Quote Time = <Time of the last quote received before 16:30:00>
    3. Number of valid quotes received for the day
    4. Most active hour (maximum valid quotes per hour received during the
    trading day). If the maximum number of valid quotes per hour occurs for
    more than one hour, pick the earliest hour of the day.
    5. Most active symbol (maximum valid quotes per symbol received during
    the trading day).If the maximum number of valid quotes per symbol
    occurs for more than one symbol, pick the first symbol (sorted
    alphabetically).
    """
    for trading_day_feed in feed.get_trading_day_feeds():
        print(
            f"\n===Trading Day: {trading_day_feed[0].date}===\n"
            f"Last Quote Time: {_get_last_quote_time(trading_day_feed)}\n"
            f"Number of valid quotes: {_get_valid_quote_count(trading_day_feed)}\n"
            f"Most active hour: {_get_most_active_hour(trading_day_feed)}\n"
            f"Most active symbol: {_get_most_active_symbol(trading_day_feed)}\n"
        )

        print("Price Statistics:")
        for symbol, price_statistics in _get_price_statistics(trading_day_feed).items():
            print(
                f"{price_statistics['date']} {price_statistics['time']},{symbol},{price_statistics['high']},{price_statistics['low']}"
            )


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.DEBUG)
    print_trading_summary(DailyFeed(StringIO(input)))
