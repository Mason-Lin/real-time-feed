import pprint
import logging
from collections import defaultdict

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
print(input)


def quiz_a(data_format_1, data_format_2):
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
    for each_trading_day in sorted(set(data_format_1["date"])):
        logging.debug(each_trading_day)


def quiz_b(data_format_1, data_format_2):
    """Calculate and print the following data for each Symbol as a comma-delimiter string.
    Rows should be printed in alphabetical order based on Symbol

        i. Time: Most recent timestamp for that Symbol in YYYY-mm-dd HH:MM:SS format
        ii. Symbol
        iii. High: Maximum Price that occurred for that Symbol during the trading day.
        iv. Low: Minimum Price that occurred for that Symbol during the trading day
    """
    symbols = sorted(set(data_format_1["symbol"]))
    for each_symbol in symbols:
        logging.debug(each_symbol)


def read_input(input):
    input_lines = input.splitlines()
    count = input_lines[0]
    data_format_1 = defaultdict(list)
    data_format_2 = list()
    for line in input_lines[1:]:
        splited = line.split(",")
        logging.debug(splited)
        data_format_1["date"].append(splited[0])
        data_format_1["time"].append(splited[1])
        data_format_1["symbol"].append(splited[2])
        data_format_1["price"].append(splited[3])
        data_format_2.append(
            {
                "date": splited[0],
                "time": splited[1],
                "symbol": splited[2],
                "price": splited[3],
            }
        )
    pprint.pprint(data_format_1)
    # logging.debug(data1)
    logging.debug("=========================")
    # logging.debug(data2)
    pprint.pprint(data_format_2)
    return data_format_1, data_format_2


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.DEBUG)
    data_format_1, data_format_2 = read_input(input)
    assert data_format_1["price"][3] == "845.61"
    assert data_format_2[2]["date"] == "2017-01-03"
    assert data_format_2[2]["time"] == "16:25:25"
    assert data_format_2[2]["symbol"] == "AAPL"
    assert data_format_2[2]["price"] == "141.64"
    quiz_a(data_format_1, data_format_2)
    quiz_b(data_format_1, data_format_2)
