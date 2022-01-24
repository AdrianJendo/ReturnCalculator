import sys
from turtle import end_fill
import requests
import os
import json
import pandas as pd

API_URL = os.environ.get("API_URL")
API_KEY = os.environ.get("API_KEY")


def get_price_df(ticker, start_date, end_date):
    resp = requests.get(
        "{}/{}".format(API_URL, ticker), params={"serietype": "line", "apikey": API_KEY}
    )

    historical_data = resp.json()["historical"]
    historical_data_df = pd.DataFrame(historical_data)
    historical_data_df = historical_data_df.set_index("date").sort_index()

    return historical_data_df.loc[start_date:end_date]


def plot_df(df, ticker):
    plot = df.plot(figsize=(20, 10))
    plot.set_ylabel("Value of investment")
    plot.set_title("Investment Return")
    plot.get_legend().remove()
    plot.figure.savefig("graphs/{}.jpg".format(ticker))


if __name__ == "__main__":
    sys_args = sys.argv
    ticker = sys_args[1]
    start_date = sys_args[2]
    end_date = sys_args[3]
    contribution = int(sys.argv[4]) if len(sys_args) > 4 else 100
    frequency = int(sys.argv[5]) if len(sys_args) > 5 else "monthly"

    # monthly, weekly, quarterly, yearly, biannually

    # price_df = get_price_df(ticker, start_date, end_date)

    # print(price_df)
