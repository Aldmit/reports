import pandas as pd 
import numpy as np   

from datetime import datetime, timedelta

df = pd.read_csv("./src/Reports/avrorakuhni-spb.csv",header=1, sep='\t', index_col=0, encoding="cp1251")

Date = '2024-10-16'

x = df.loc[[Date],['Impressions', 'Clicks', 'Cost']]

print(x)

view = int(x.iloc[0,0])
click = int(x.iloc[0,1])
cost =x.iloc[0,2]
cpc = cost/click


print(f"{view} - {click} - {cost} - {cpc}")


yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
print(yesterday)
# print(f"Clicks: {int(y['Clicks'][Date])}\nViews: {int(y['Impressions'][Date])}\nCost: {y['Cost'][Date]}")


# x = df['Date']


# print(x)

