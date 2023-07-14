import pandas as pd

x = pd.read_csv(r'C:\Users\colea\OneDrive\Documents\nyse_sectors.txt')
x.to_csv(r'C:\Users\colea\Downloads\nyse_sectors.csv')
print(x)