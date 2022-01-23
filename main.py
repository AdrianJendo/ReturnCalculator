import sys
import requests


def get_price_df(ticker, start_date, end_date):
    print("Hello World")

    return True


if __name__ == "__main__":
    ticker = sys.argv[1]
    start_date = sys.argv[2]
    end_date = sys.argv[3]

    # /SPY?serietype=line&apikey=455df261819241f4292b36bf952efbe9

    get_price_df(ticker, start_date, end_date)
