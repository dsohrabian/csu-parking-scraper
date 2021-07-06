import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('CSU_parking_live.csv', index_col='date', parse_dates=True)
cols = df.columns[2:]
select_col = [field for field in cols if 'openspaces' in field]

plotdf = df[select_col]
plotdf.plot()