import logging
import pprint
from collections import Counter, defaultdict
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


def get_most_active_hour(data_format_row, trading_day):
    cnt = Counter()
    # FIXME create trading day slice from earlier step, like trading_day_data (include all tradings of the date only)
    # it's very hard to test this function now.
    for i in range(len(data_format_row)):
        if data_format_row[i]["date"] == trading_day:
            hh, mm, ss = data_format_row[i]["time"].split(":")
            cnt[hh] += 1

    # [0][0] means get hour from [('12', 3)]
    sorted_most_common = sorted(cnt.most_common(), key=itemgetter(0))
    return sorted_most_common[0][0]


def get_most_active_symbol(data_format_row, trading_day):
    # TODO didn't handle two active symbol case
    # AAPL 3 times, FB 3 times, should return AAPL
    cnt = Counter()
    for i in range(len(data_format_row)):
        if data_format_row[i]["date"] == trading_day:
            # TODO Should I consider case? will it be AAPL and aapl?
            cnt[data_format_row[i]["symbol"]] += 1
    sorted_most_common = sorted(cnt.most_common(), key=itemgetter(0))
    return sorted_most_common[0][0]


def get_last_quote_time(data_format_row, trading_day):
    for i in range(len(data_format_row) - 1, 0, -1):
        if data_format_row[i]["date"] == trading_day:
            last_quote_time = data_format_row[i]["time"]
            break
    return last_quote_time


def get_valid_quote_count(data_format_row, trading_day):
    valid_quote_count = 0
    for i in range(len(data_format_row)):
        if data_format_row[i]["date"] == trading_day:
            valid_quote_count += 1
    return valid_quote_count


def quiz_a(data_format_col, data_format_row):
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
    for trading_day in sorted(set(data_format_col["date"])):
        logging.info("Trading Day: %s", trading_day)
        logging.info(
            "Last Quote Time: %s", get_last_quote_time(data_format_row, trading_day)
        )
        logging.info(
            "Number of valid quotes: %s",
            get_valid_quote_count(data_format_row, trading_day),
        )
        logging.info(
            "Most active hour: %s", get_most_active_hour(data_format_row, trading_day)
        )
        logging.info(
            "Most active symbol: %s",
            get_most_active_symbol(data_format_row, trading_day),
        )


def quiz_b(data_format_col, data_format_row):
    """Calculate and print the following data for each Symbol as a comma-delimiter string.
    Rows should be printed in alphabetical order based on Symbol

        i. Time: Most recent timestamp for that Symbol in YYYY-mm-dd HH:MM:SS format
        ii. Symbol
        iii. High: Maximum Price that occurred for that Symbol during the trading day.
        iv. Low: Minimum Price that occurred for that Symbol during the trading day
    """
    symbols = sorted(set(data_format_col["symbol"]))
    for each_symbol in symbols:
        logging.debug(each_symbol)


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
    count = input_lines[0]
    data_format_1 = defaultdict(list)
    data_format_2 = list()
    for line in input_lines[1:]:
        splited = line.split(",")
        time = splited[1]
        # TODO convert to datetime format?
        if "09:30:00" > time or time > "16:30:00":
            continue
        logging.debug(splited)
        data_format_1["date"].append(splited[0])
        data_format_1["time"].append(time)
        data_format_1["symbol"].append(splited[2])
        data_format_1["price"].append(splited[3])
        data_format_2.append(
            {
                "date": splited[0],
                "time": time,
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
    data_format_col, data_format_row = read_input(input)
    assert data_format_col["price"][3] == "845.61"
    assert data_format_row[2]["date"] == "2017-01-03"
    # assert data_format_row[2]["time"] == "16:25:25"
    assert data_format_row[2]["symbol"] == "AAPL"
    assert data_format_row[2]["price"] == "141.64"
    quiz_a(data_format_col, data_format_row)
    quiz_b(data_format_col, data_format_row)
