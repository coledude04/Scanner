import yfinance as yf
import pandas as pd
from tqdm import tqdm

companies = pd.read_csv(r"C:\Users\colea\Downloads\nasdaq-listed-symbols.csv")

tickers = companies['Symbol'].to_list()

pe_ratios = []
avg_pe_ratios = []
bad_pe = []
avg_div_current = []

def add_pe(company):
    try:
        stock = yf.Ticker(company)
        html = "https://www.macrotrends.net/stocks/charts/" + company + "//pe-ratio"
        data = pd.read_html(html)

        df = pd.DataFrame(data[0])
        df = df.columns.to_frame().T._append(df, ignore_index = True)
        df.columns = range(len(df.columns))
        df = df[1:]
        df = df.rename(columns = {0: 'Date', 1: 'Price', 2: 'EPS', 3: 'PE ratio'})
        df['EPS'][1] = ''
        df.set_index('Date', inplace = True)
        df = df.sort_index()
        df['trend'] = ""

        df['PE ratio'] = pd.to_numeric(df['PE ratio'], errors='coerce')
        pe_std = df['PE ratio'].std()
        for i in range(0, len(df)):
            df['PE ratio mean'] = df['PE ratio'].mean()

        try:
            pe_ratios.append(round(stock.info['trailingPE'], 2))
            avg_pe_ratios.append(round(df['PE ratio'].mean(),2))

        except:
            bad_pe.append(company)

    except:
        bad_pe.append(company)
       
for stock in tqdm(tickers):
    add_pe(stock)
    '''
    print(stock)
    print(f"{tickers.index(stock)} / {len(tickers)}")
    '''
    
i = 0
while i < len(bad_pe):
    try:
        if bad_pe[i] in tickers:
            tickers.pop(tickers.index(bad_pe[i]))
        else:
            i += 1
    except:
        break

for i in range(len(tickers)):
    avg_div_current.append(round(pe_ratios[i]/avg_pe_ratios[i], 2))

rank_pe_r = list(avg_div_current)
rank_pe_r.sort()
rank_stocks = []
rank_pe = []
rank_avg = []

for ratio in rank_pe_r:
    rank_stocks.append(tickers[avg_div_current.index(ratio)])
    rank_pe.append(pe_ratios[avg_div_current.index(ratio)])
    rank_avg.append(avg_pe_ratios[avg_div_current.index(ratio)])

data = {
    "Stocks" : rank_stocks,
    "Ratios" : rank_pe_r,
    "PE" : rank_pe,
    "Average PE" : rank_avg
}

pd.set_option("display.max_rows", None)
print(pd.DataFrame(data))
