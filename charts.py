# Run this entire script to generate a plot for subscription parking and for public parking in interactive setting
# You can choose to save the figures
import matplotlib.pyplot as plt
import matplotlib.ticker
import pandas as pd

plt.style.use('seaborn')
df = pd.read_csv('CSU_parking_live.csv', index_col='date', parse_dates=True)
cols = df.columns

# Subscriptions
select_col = [field for field in cols if 'perc' in field if 'permit' in field]
plotdf = df[select_col]
dailymins = plotdf.resample('60T').min() # resample the data to 30 minute increments. recode to whatever is best for you scheduling
dailymins.columns = ['South', 'Prospect', 'West', 'Central', 'East']
ax = dailymins.plot(style='o-', ms=3.5, lw=1)
ax.yaxis.set_major_formatter('{x:.0%}')
ax.set_ylabel('Garage Vacancy (Subscribers)')
ax.set_xlabel('')
ax.set_ylim(0)
plt.legend(bbox_to_anchor=(.5, .98), bbox_transform=plt.gcf().transFigure, ncol=5, loc="upper center",)
plt.tight_layout()

# Public spaces
select_col = [field for field in cols if 'perc' in field if 'public' in field]
plotdf = df[select_col]
dailymins = plotdf.resample('60T').min()
dailymins.columns = ['South', 'Prospect', 'West', 'Central', 'East']
ax = dailymins.plot(style='o-', ms=3.5, lw=1)
ax.yaxis.set_major_formatter('{x:.0%}')
ax.set_ylabel('Garage Vacancy (Open to Public)')
ax.set_xlabel('')
ax.set_ylim(0)
plt.legend(bbox_to_anchor=(.5, .98), bbox_transform=plt.gcf().transFigure, ncol=5, loc="upper center",)
plt.tight_layout()