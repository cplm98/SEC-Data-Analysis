import pandas as pd
import numpy as np
from sec_edgar_downloader import Downloader

dl = Downloader('./')

# all_comps = pd.DataFrame(pd.read_csv('./cik_ticker.csv', sep='|'))
sp = pd.DataFrame(pd.read_csv('./constituents_csv.csv'))

# all_comps.set_index('Ticker')
# sp.rename('Symbol': 'Ticker')
# sp.set_index('Ticker')

print(sp.head(10))

for symbol in sp['Symbol'][50:100]:
    dl.get('10-K', symbol, amount=5)