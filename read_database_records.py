'''
verifying our database records

'''

import sqlite3
import pandas as pd

conn = sqlite3.connect('records.db')
c = conn.cursor()
df = pd.read_sql('SELECT * from data', conn)
df = df.sort_values(by='num_bikes', ascending=False)
print(df)


'''
[254276 rows x 3 columns]

'''