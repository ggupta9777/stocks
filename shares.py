from nsetools import Nse
from pprint import pprint

import datetime
from nsepy import get_history

now = datetime.datetime.now()
nse = Nse()
start_date = datetime.date(now.year, now.month-3, now.day)
end_date = datetime.date(now.year, now.month, now.day)
if __name__ == "__main__":
	infy_quote = nse.get_quote("infy")
	infy_history = get_history(symbol = 'INFY', start=start_date, end=end_date)
	pprint (infy_quote)
	print(infy_history)
