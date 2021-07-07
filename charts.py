import matplotlib.pyplot as plt
import matplotlib.ticker
import pandas as pd

df = pd.read_csv('CSU_parking_live.csv', index_col='date', parse_dates=True)
cols = df.columns
select_col = [field for field in cols if 'perc' in field if 'permit' in field]

plotdf = df[select_col]
dailymins = plotdf.resample('1D').min()
dailymins.columns = ['South', 'Prospect', 'West', 'Central', 'East']

plt.style.use('seaborn')
ax = dailymins.plot(style='o-')
ax.yaxis.set_major_formatter('{x:.0%}')
ax.set_ylabel('Lowest daily garage vacancy')
ax.set_xlabel('')
plt.tight_layout()