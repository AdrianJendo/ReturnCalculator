# Command to run:

pipenv run python main.py {ticker} {start_date (YY-mm-dd)} {end_date (YY-mm-dd)} {contribution (int) -- default 100} {frequency (weekly, monthly, quarterly, biannually, annually) -- default monthly} {contribution (int) -- default 0}

ex: pipenv run python main.py SPY 1995-01-01 2022-01-24 200 monthly 0
