import sys
import requests
import os
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta

API_URL = os.environ.get("API_URL")
API_KEY = os.environ.get("API_KEY")


def get_price_df(ticker, start_date, end_date):
    price_data = requests.get(
        "{}/{}".format(API_URL, ticker), params={"serietype": "line", "apikey": API_KEY}
    )
    dividend_data = requests.get(
        "{}/stock_dividend/{}".format(API_URL, ticker), params={"apikey": API_KEY}
    )

    price_data = price_data.json()["historical"]
    dividend_data = dividend_data.json()["historical"]
    historical_data_df = pd.DataFrame(price_data)
    historical_data_df = historical_data_df.set_index("date").sort_index()
    dividend_df = pd.DataFrame(
        [{"date": x["date"], "dividend": x["adjDividend"]} for x in dividend_data]
    )
    dividend_df = dividend_df.set_index("date").sort_index()

    return historical_data_df.loc[start_date:end_date].join(dividend_df)


def plot_df(df, ticker):
    plot = df.plot(figsize=(20, 10))
    plot.set_ylabel("Value of investment")
    plot.set_title("Investment Return")
    plot.legend(loc="upper left")
    plot.figure.savefig("graphs/{}.jpg".format(ticker))


def get_time_delta(frequency):
    if frequency == "weekly":
        return relativedelta(days=7)
    elif frequency == "quarterly":
        return relativedelta(months=3)
    elif frequency == "biannually":
        return relativedelta(months=6)
    elif frequency == "annually":
        return relativedelta(years=1)
    else:  # default do monthly
        return relativedelta(months=1)


if __name__ == "__main__":
    sys_args = sys.argv
    ticker = sys_args[1]
    start_date = sys_args[2]
    end_date = sys_args[3]
    contribution = int(sys.argv[4]) if len(sys_args) > 4 else 100
    frequency = sys.argv[5] if len(sys_args) > 5 else "monthly"

    timedelta = get_time_delta(frequency)
    cur_datetime = datetime.strptime(start_date, "%Y-%m-%d")
    last_datetime = cur_datetime
    end_datetime = datetime.strptime(end_date, "%Y-%m-%d")
    start_date = (cur_datetime - relativedelta(days=5)).strftime(
        "%Y-%m-%d"
    )  # avoid weekends

    total_investment = 0
    num_shares = 0  # assuming we can't do fractional
    remainder = 0

    price_df = get_price_df(ticker, start_date, end_date)

    if end_datetime < cur_datetime:
        print("ERROR: End date before start date")
        sys.exit(0)

    return_summary_df = pd.DataFrame(
        columns=["date", "total_investment", "portfolio_value"]
    )

    while end_datetime > cur_datetime:
        cur_date = cur_datetime.strftime("%Y-%m-%d")
        last_date = last_datetime.strftime("%Y-%m-%d")
        stock_price = price_df.loc[start_date:cur_date].iloc[-1]["close"]
        dividend = price_df.loc[last_date:cur_date]["dividend"].sum()

        investible_dollars = contribution + remainder + dividend * num_shares
        num_shares += investible_dollars // stock_price
        total_investment += investible_dollars // stock_price * stock_price
        remainder = investible_dollars % stock_price

        return_summary_df = pd.concat(
            [
                return_summary_df,
                pd.DataFrame(
                    [
                        [
                            cur_date,
                            round(total_investment, 2),
                            round(num_shares * stock_price, 2),
                        ]
                    ],
                    columns=["date", "total_investment", "portfolio_value"],
                ),
            ]
        )

        last_datetime = cur_datetime
        cur_datetime += timedelta

    return_summary_df = return_summary_df.set_index("date").sort_index()
    print("Start of df: ")
    print(return_summary_df.head(5))
    print("End of df: ")
    print(return_summary_df.tail(5))

    plot_df(return_summary_df, ticker)
