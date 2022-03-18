import requests
import os
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
from optparse import OptionParser
import os

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
    dividend_data = dividend_data.json().get(
        "historical",
        [
            {"date": end_date, "adjDividend": 0}
        ],  # Dummy data to avoid errors if company never paid a dividend
    )
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
    date_today = datetime.today().strftime("%Y-%m-%d")
    plot.figure.savefig("graphs/{}-{}.jpg".format(ticker, date_today))


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


def main(options):
    ticker = options.ticker
    start_date = options.start_date
    end_date = options.end_date
    contribution = options.contribution
    frequency = options.frequency
    initial_investment = options.initial_investment

    cur_datetime = datetime.strptime(start_date, "%Y-%m-%d")
    next_contribution = cur_datetime + get_time_delta(
        frequency
    )  # Next contribution to portfolio
    last_contribution = cur_datetime - relativedelta(
        days=7
    )  # prevents error when last_date and start_date are same day
    end_datetime = datetime.strptime(end_date, "%Y-%m-%d")
    start_date = (cur_datetime - relativedelta(days=5)).strftime(
        "%Y-%m-%d"
    )  # avoid weekends

    if end_datetime < cur_datetime:
        print("ERROR: End date before start date")
        return

    price_df = get_price_df(ticker, start_date, end_date)

    initial_price = price_df.iloc[0]["close"]
    num_shares = initial_investment // initial_price  # assuming we can't do fractional
    total_investment = initial_investment // initial_price * initial_price
    remainder = initial_investment % initial_price

    return_summary_df = pd.DataFrame(
        columns=["date", "total_investment", "portfolio_value"]
    )

    while end_datetime > cur_datetime:
        cur_date = cur_datetime.strftime("%Y-%m-%d")
        last_date = last_contribution.strftime("%Y-%m-%d")
        stock_price = price_df.loc[last_date:cur_date].iloc[-1]["close"]

        # Only update total investment at each contribution
        if next_contribution <= cur_datetime:
            next_contribution += get_time_delta(frequency)
            dividend = price_df.loc[last_date:cur_date]["dividend"].sum()
            investible_dollars = contribution + remainder + dividend * num_shares
            num_shares += investible_dollars // stock_price
            total_investment += investible_dollars // stock_price * stock_price
            remainder = investible_dollars % stock_price
            last_contribution = cur_datetime

        # Update graph every 7 days
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

        cur_datetime += relativedelta(days=7)

    return_summary_df = return_summary_df.set_index("date").sort_index()
    print("Start of df: ")
    print(return_summary_df.head(5))
    print("End of df: ")
    print(return_summary_df.tail(5))

    plot_df(return_summary_df, ticker)


if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option(
        "-t",
        "--ticker",
        default="SPY",
        dest="ticker",
        help="ticker to calculate return",
    )
    parser.add_option(
        "-s",
        "--start_date",
        default=(datetime.now() - relativedelta(years=10)).strftime("%Y-%m-%d"),
        dest="start_date",
        help="date to start calculate",
    )
    parser.add_option(
        "-e",
        "--end_date",
        default=(datetime.now()).strftime("%Y-%m-%d"),
        dest="end_date",
        help="date to end calculate",
    )
    parser.add_option(
        "-c",
        "--contribution",
        default=100,
        dest="contribution",
        help="recurring contribution",
        type="int",
    )
    parser.add_option(
        "-f",
        "--frequency",
        default="monthly",
        dest="frequency",
        help="frequency of recurring contribution",
    )
    parser.add_option(
        "-i",
        "--initial_investment",
        default=0,
        dest="initial_investment",
        help="initial contribution",
        type="int",
    )

    (options, args) = parser.parse_args()

    main(options)
