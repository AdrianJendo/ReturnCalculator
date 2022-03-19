# Need to get an API key from financialmodellingprep.com

API_URL used for this project: https://financialmodelingprep.com/api/v3/historical-price-full

# Command to run:

`pipenv run python main.py -t` \<ticker\> `-s` \<start date (YY-mm-dd)\> `-e` \<end date (YY-mm-dd)\> `-c` \<contribution\> `-f` \<frequency (weekly, monthly, quarterly, biannually, annually)\> `-i` \<initial investment\>

ex: `pipenv run python main.py -t AAPL -s 2010-01-01 -e 2022-03-16 -c 300 -f quarterly -i 4000`

**OR**

`pipenv run python main.py --ticker` \<ticker\> `--start_date` \<start date (YY-mm-dd)\> `--end_date` \<end date (YY-mm-dd)\> `--contribution` \<contribution\> `--frequency` \<frequency (weekly, monthly, quarterly, biannually, annually)\> `--initial_investment` \<initial investment\>

ex: `pipenv run python main.py --ticker AAPL --start_date 2010-01-01 --end_date 2022-03-16 --contribution 300 --frequency quarterly --initial_investment 4000`

_Note: All parameters are optional and defaults are available_
