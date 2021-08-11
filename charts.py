# Run this entire script to generate a plot for subscription parking and for public parking in interactive setting
# You can choose to save the figures
import matplotlib.pyplot as plt
import matplotlib.dates as md
import matplotlib.ticker
import pandas as pd
import matplotlib as mpl
import numpy as np

plt.style.use('ggplot')
mpl.rcParams['font.family'] = 'Segoe UI'
df = pd.read_csv('CSU_parking_live.csv', index_col='date', parse_dates=True)
cols = df.columns

# plotter
select_col = [field for field in cols if 'spaces' in field]
parking_total = sum([611, 291, 600, 867, 600])  # total parking capacity per facility found on website in order of
# data,i.e. 'South', 'Prospect', 'West', 'Central', 'East'
plotdf = df[select_col].copy()
plotdf['percent_use'] = 1 - (plotdf.sum(axis=1) / parking_total)  # get percent used
plotdf['total_open'] = plotdf.iloc[:, 0:-1].sum(axis=1)  # get percent open
avg_empty = plotdf['total_open'].mean()
construction_cost = avg_empty * 20000 / 1000000  # cost of empty spaces in millions

# resample the data to 1 hour increments. recode to whatever is best for you scheduling
hourlymins = plotdf.resample('1H').max()

# plot the final column percentages
fig, ax = plt.subplots()
ax.plot('percent_use', '-', ms=3.5, lw=2, data=hourlymins)

# # format the plot
# x axis major ticks as months
fmt_months = md.MonthLocator(interval=1)
ax.xaxis.set_major_locator(fmt_months)
ax.xaxis.set_major_formatter(md.DateFormatter('%b %y'))  # label as month and 2 digit year
plt.setp(ax.xaxis.get_majorticklabels(), fontweight='semibold')

# x
fmt_days = md.DayLocator(interval=2, bymonthday=range(3, 31))
ax.xaxis.set_minor_locator(fmt_days)
ax.xaxis.set_minor_formatter(md.DateFormatter('%d'))
plt.setp(ax.xaxis.get_minorticklabels(), rotation=90, size=8)

# set x axis limits
date_min = np.datetime64(hourlymins.index[0], 'D') - 2  # earliest day minus 2 days
date_max = np.datetime64(hourlymins.index[-1], 'D') + 2  # latest day plus 2 days
ax.set_xlim(date_min, date_max)

ax.set_ylabel('% Occupied Parking')
ax.set_ylim(0, 1)
ax.yaxis.set_major_formatter('{x:.0%}')

plt.text(.65, .825, f'{parking_total:,d}' + ' spaces total' + '\n'
         + f'{avg_empty:,.0f} avg. spaces empty' + '\n'
         + f'${construction_cost:.1f}m unused capital cost*',
         ha='left', linespacing=1.5, transform=ax.transAxes, )
plt.text(.65, .78, '*Based on $20k per space construction cost', color='.25',
         ha='left', fontsize=6.5, linespacing=1.5, transform=ax.transAxes, )

average_use = hourlymins['percent_use'].mean()
plt.axhline(average_use, ls=':', lw=2, c='tab:blue', alpha=.75)
plt.annotate(f'{average_use:.1%} avg. hourly use', xy=(date_min + 1, average_use), xytext=(date_min + 10, .1), c= 'tab:blue',
             arrowprops={'arrowstyle': '->', 'connectionstyle': "angle,angleA=180,angleB=90", 'color': 'tab:blue',
                         'lw': '.5', 'alpha': 0.75})

plt.suptitle(f'CSU Garages (South, Prospect, West, Central, East)')
plt.tight_layout()
plt.savefig('./example/ex1.png', dpi=150)
plt.savefig('./example/ex1_thumb.png', dpi=72)
