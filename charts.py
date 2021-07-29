# Run this entire script to generate a plot for subscription parking and for public parking in interactive setting
# You can choose to save the figures
import matplotlib.pyplot as plt
import matplotlib.dates as md
import matplotlib.ticker
import pandas as pd
import matplotlib as mpl

plt.style.use('ggplot')
mpl.rcParams['font.family'] = 'Segoe UI'
df = pd.read_csv('CSU_parking_live.csv', index_col='date', parse_dates=True)
cols = df.columns

# plotter
select_col = [field for field in cols if 'spaces' in field]
parking_total = sum([611, 291, 600, 867, 600])  # total parking capacity per facility found on website in order of
# data,i.e. 'South', 'Prospect', 'West', 'Central', 'East'
plotdf = df[select_col].copy()
plotdf['total_use'] = 1 - (plotdf.sum(axis=1) / parking_total)
plotdf['total_open'] = plotdf.iloc[:, 0:-1].sum(axis=1)
avg_empty = plotdf['total_open'].mean()
construction_cost = avg_empty * 20000 / 1000000  # cost of empty spaces in millions

# resample the data to 1 hour increments. recode to whatever is best for you scheduling
hourlymins = plotdf.resample('1H').max()

# plot the final column percentages
ax = hourlymins.loc[:, 'total_use'].plot(style='-', ms=3.5, lw=2, legend=False)

# format
ax.yaxis.set_major_formatter('{x:.0%}')
locator = md.AutoDateLocator()
# ax.xaxis.set_major_formatter(md.DateFormatter('%b %d'))
ax.set_ylabel('% Occupied Parking')
ax.set_xlabel('')
ax.set_ylim(0, 1)
plt.text(.65, .825, f'{parking_total:,d}' + ' spaces total' + '\n'
         + f'{avg_empty:,.0f} avg. spaces empty' + '\n'
         + f'${construction_cost:.1f}m unused capital cost*',
         ha='left', linespacing=1.5, transform=ax.transAxes,)
plt.text(.65, .78, '*Based on $20k per space construction cost', color='.25',
         ha='left', fontsize=6.5, linespacing=1.5, transform=ax.transAxes,)

bbox = {'boxstyle': 'round', 'color': '.8'}
average_spaces = hourlymins

plt.suptitle(f'All Garages (South, Prospect, West, Central, East)')
plt.tight_layout()
