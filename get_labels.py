from alpha_vantage.timeseries import TimeSeries
import pandas as pd
import numpy as np
import time

sp = pd.DataFrame(pd.read_csv('./constituents_csv.csv'))

key = '9AD6SV02MT4Z7G8W'

ts = TimeSeries(key, output_format='pandas')


# aapl, meta = ts.get_monthly_adjusted(symbol='AAPL')
# print(aapl[aapl.index >= '2015'])
results=[]
for ticker in sp['Symbol'][:100]:
    print(ticker)
    try:
        res, meta = ts.get_monthly_adjusted(symbol=ticker)
        res['ticker'] = ticker
        for i in range(2015, 2021): # up to 2021
            try:
                year = res[res.index.year == i]
                open_ = year[year.index.month == 1]['1. open'].values
                close = year[year.index.month == 12]['5. adjusted close'].values
                yearly_adj_close = close - open_
                yearly_change = yearly_adj_close/open_
                results.append({'year': i, 'ticker': ticker, 'yearly adjsuted close': yearly_adj_close[0], 'yearly percent change': yearly_change[0], 'year open': open_[0], 'year adjusted close': close[0]})
            except:
                print(res)
                print('No valid data for year', i, ' with Ticker ', ticker)
                results.append({'year': i, 'ticker': ticker, 'yearly adjsuted close': None, 'yearly percent change': None, 'year open': None, 'year adjusted close': None})
    except:
        print('Problem retrieiving stock information: ', ticker)
    time.sleep(15) # necessary to not overwhelm API
    print(results)

df = pd.DataFrame(results)
df.to_csv('labels.csv')