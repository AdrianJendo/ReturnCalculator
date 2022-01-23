import sys
import requests
import os
import json
import pandas as pd

API_URL = os.environ.get("API_URL")
API_KEY = os.environ.get("API_KEY")


def get_price_df(ticker):
    resp = requests.get(
        "{}/{}".format(API_URL, ticker), params={"serietype": "line", "apikey": API_KEY}
    )

    historical_data = resp.json()["historical"]
    historical_data_df = pd.DataFrame(historical_data)
    historical_data_df = historical_data_df.set_index("date").sort_index()

    print(historical_data_df.head())

    plot = historical_data_df.plot(figsize=(20, 10))
    plot.set_ylabel("Value of investment")
    plot.set_title("Investment Return")
    plot.get_legend().remove()
    plot.figure.savefig("graphs/test.jpg")

    return True


if __name__ == "__main__":
    ticker = sys.argv[1]
    start_date = sys.argv[2]
    end_date = sys.argv[3]

    # /SPY?serietype=line&apikey=455df261819241f4292b36bf952efbe9

    get_price_df(ticker)
