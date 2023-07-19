import pandas as pd
import yfinance as yf
from tqdm import tqdm




stock = yf.Ticker("aapl")
print(stock.info['sector'])

nasdaq = pd.read_csv(r'C:\Users\colea\Downloads\nyse-listed-symbols.csv')
tickers = nasdaq['ACT Symbol'].to_list()
sectors = []
noSector=[]

for stock in tqdm(tickers):
    company = yf.Ticker(stock)
    try:
         sectors.append(company.info['sector'])

    except:
         noSector.append(stock)

i = 0
while i < len(noSector):
    try:
        if noSector[i] in tickers:
            tickers.pop(tickers.index(noSector[i]))
        else:
            i += 1
    except:
        break

data = {
    "Stocks" : tickers,
    "Sectors" : sectors,
}

'''print(f"Bad Stocks {len(noSector)}")
pd.set_option("display.max_rows", None)
print(pd.DataFrame(data))'''

final = pd.DataFrame(data)
final.to_csv(r'C:\Users\colea\Downloads\nyse_sectors.csv')