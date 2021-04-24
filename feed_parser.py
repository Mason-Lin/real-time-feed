import logging
import pprint
from collections import Counter
from dataclasses import dataclass
from operator import itemgetter

# FIXME think about really big inputs, using iterator
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
class ParsedFeedData:
    data_format_row: list = None
    data_format_start_end: dict = None


def get_most_active_hour(trading_day_data):
    cnt = Counter()
    for data in trading_day_data:
        hour = data["time"].split(":")[0]  # HH:MM:SS
        cnt[hour] += 1

    # [0][0] means get hour from [('12', 3), ('16', 3)]
    sorted_most_common = sorted(cnt.most_common(), key=itemgetter(0))
    return sorted_most_common[0][0]


def get_most_active_symbol(trading_day_data):
    cnt = Counter()
    for data in trading_day_data:
        cnt[data["symbol"]] += 1
    sorted_most_common = sorted(cnt.most_common(), key=itemgetter(0))
    return sorted_most_common[0][0]


def get_last_quote_time(trading_day_data):
    return trading_day_data[-1]["time"]


def get_valid_quote_count(trading_day_data):
    return len(trading_day_data)


def trading_summary(parsed_feed_data):
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
    for trading_day in sorted(parsed_feed_data.data_format_start_end.keys()):
        start = parsed_feed_data.data_format_start_end[trading_day]["start"]
        end = parsed_feed_data.data_format_start_end[trading_day]["end"]
        trading_day_data = parsed_feed_data.data_format_row[start:end]
        print(
            f"\n===Trading Day: {trading_day}===\n"
            f"Last Quote Time: {get_last_quote_time(trading_day_data)}\n"
            f"Number of valid quotes: {get_valid_quote_count(trading_day_data)}\n"
            f"Most active hour: {get_most_active_hour(trading_day_data)}\n"
            f"Most active symbol: {get_most_active_symbol(trading_day_data)}\n"
            "Price Statistics:\n"
            f"{get_price_statistics(trading_day_data)}"
        )


def get_price_statistics(trading_day_data):
    """Calculate and print the following data for each Symbol as a comma-delimiter string.
    Rows should be printed in alphabetical order based on Symbol

        i. Time: Most recent timestamp for that Symbol in YYYY-mm-dd HH:MM:SS format
        ii. Symbol
        iii. High: Maximum Price that occurred for that Symbol during the trading day.
        iv. Low: Minimum Price that occurred for that Symbol during the trading day
    """
    symbol_hist = dict()
    for data in trading_day_data:
        if symbol_hist.get(data["symbol"]):
            prev_time = symbol_hist[data["symbol"]]["time"]
            symbol_hist[data["symbol"]]["time"] = (
                data["time"] if data["time"] > prev_time else prev_time
            )
            symbol_hist[data["symbol"]]["high"] = max(
                symbol_hist[data["symbol"]]["high"], data["price"]
            )
            symbol_hist[data["symbol"]]["low"] = min(
                symbol_hist[data["symbol"]]["low"], data["price"]
            )
        else:
            symbol_hist[data["symbol"]] = {
                "date": data["date"],
                "time": data["time"],
                "high": data["price"],
                "low": data["price"],
            }
    # TODO refactoring
    price_statistics = []
    for symbol in sorted(symbol_hist.keys()):
        price_statistics.append(
            f"{symbol_hist[symbol]['date']} {symbol_hist[symbol]['time']},{symbol},{symbol_hist[symbol]['high']},{symbol_hist[symbol]['low']}"
        )
    return price_statistics


def read_input(input):
    """The exchange starts trading daily at 09:30:00 hrsand closes at 16:30:00 hrsevery day
    Any quotes outside this time window are invalid and will be ignored.
        Input:
            string like
            8
            2017-01-03,16:18:50,AAPL,142.64
            2017-01-03,16:25:22,AMD,13.86
        Return:
            some kind of data sturuct
    """
    input_lines = input.splitlines()
    data_format_row = list()
    # TODO temp ignored first line, it's number of quotes like 8
    for line in input_lines[1:]:
        splited = line.split(",")
        # TODO convert to datetime format? no need for now.
        date = splited[0]
        time = splited[1]
        symbol = splited[2].upper()
        price = splited[3]

        if "09:30:00" > time or time > "16:30:00":
            continue

        data_format_row.append(
            {
                "date": date,
                "time": time,
                "symbol": symbol,
                "price": price,
            }
        )

    # helper
    data_format_start_end = dict()
    for i in range(len(data_format_row)):
        trading_day = data_format_row[i]["date"]
        if data_format_start_end.get(trading_day):
            data_format_start_end[trading_day]["end"] = i + 1
        else:
            data_format_start_end[trading_day] = {"start": i, "end": i + 1}

    logging.debug(pprint.pformat(data_format_start_end))
    logging.debug(pprint.pformat(data_format_row))
    parsed_feed_data = ParsedFeedData(data_format_row, data_format_start_end)
    return parsed_feed_data


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.DEBUG)
    parsed_feed_data = read_input(input)
    trading_summary(parsed_feed_data)
