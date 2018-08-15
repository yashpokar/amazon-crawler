import pandas as pd

df = pd.read_csv('listing.csv')
print len(df.asin.unique()), len(df.asin)
