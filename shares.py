from nsetools import Nse
from pprint import pprint
import datetime
from nsepy import get_history
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


now = datetime.datetime.now()
nse = Nse()
max_start_date = datetime.date(now.year-5, now.month, now.day)
long_start_date = datetime.date(now.year-1, now.month, now.day)
start_date = datetime.date(now.year, now.month-3, now.day)
end_date = datetime.date(now.year, now.month, now.day)

def show_trend(stock_name):
	quote = nse.get_quote(stock_name)

        max_history = get_history(symbol = stock_name, start=max_start_date, end=end_date)
	long_history = get_history(symbol = stock_name, start=long_start_date, end=end_date)
	history = get_history(symbol = stock_name, start=start_date, end=end_date)
	
	max_year_mean = max_history['Close'].rolling(window = 365, center=False).mean()
	max_quarter_mean = max_history['Close'].rolling(window = 90, center=False).mean()
	max_month_mean = max_history['Close'].rolling(window = 30, center=False).mean()
	long_close = long_history['Close'][0]
        mm = history['Close'].mean()
	one_mm = history['Close'][-30:].mean()
	 
        mean_history =  history['Close'].rolling(window=5, center=False).mean()
        max_year_mean.plot()
	max_quarter_mean.plot()
	max_month_mean.plot()
	# history[['Close']].plot()
        # mean_history.plot()
        plt.xlabel("date")
        plt.ylabel("price (R)")
        plt.title("prices over time "+stock_name)
        plt.savefig(stock_name + ".png")
	plt.clf()

if __name__ == "__main__":
	f = open("nifty50.txt", 'r');
	company_list = f.readlines()
	company_list = [x.strip() for x in company_list] 
	for company in company_list:
		show_trend(company)
	# show_trend("INFY")
	# show_trend("SBIN")
	# show_trend("SUNPHARMA")
