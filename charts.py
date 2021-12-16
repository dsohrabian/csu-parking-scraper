# Run this entire script to generate a plot for subscription parking and for public parking in interactive setting
# You can choose to save the figures
import matplotlib.pyplot as plt
import matplotlib.dates as md
import pandas as pd
import matplotlib as mpl
import numpy as np

plt.style.use('ggplot')
plt.interactive(False)
mpl.rcParams['font.family'] = 'Segoe UI'
df = pd.read_csv('CSU_parking_live.csv', parse_dates=['date'], infer_datetime_format=True)
df = df.set_index('date')
df.index = pd.to_datetime(df.index, utc=True).tz_convert(tz='US/Eastern')
cols = df.columns

# plotter
select_col = [field for field in cols if 'spaces' in field]
capacity_total = sum([611, 291, 600, 867, 600])  # total parking capacity per facility found on website in order of
# data,i.e. 'South', 'Prospect', 'West', 'Central', 'East'
plot_df = df[select_col].copy()
plot_df['total_open'] = plot_df.sum(axis=1)  # total number of open spaces in feed
plot_df['percent_use'] = 1 - (plot_df.total_open / capacity_total)  # get inverse of percent open (a.k.a percent in use)
avg_empty = plot_df['total_open'].mean()  # average number of open spaces available
construction_cost = avg_empty * 20000 / 1000000  # cost of empty spaces in millions dollars

# resample the data to 1 hour increments for more consistent sampling in case scrapes are missed
hourlymins = plot_df.resample('1H').max()
off_season_hrs = hourlymins[hourlymins.index <= '2021-08-22']
in_school_hrs = hourlymins[hourlymins.index > '2021-08-22']

# plot the final column percentages
fig, ax = plt.subplots(figsize=[8, 4], dpi=200)
ax.plot('percent_use', '-', ms=1, lw=1, data=off_season_hrs, c='tab:blue')
ax.plot('percent_use', '-', ms=1, lw=1, data=in_school_hrs, c='tab:red')

# # format the plot
# x axis major ticks as months
fmt_months = md.MonthLocator(interval=1)
ax.xaxis.set_major_locator(fmt_months)
ax.xaxis.set_major_formatter(md.DateFormatter('%b'))  # label as month and 2 digit year
plt.setp(ax.xaxis.get_majorticklabels(), fontweight='semibold')

# x minor ticks
fmt_days = md.DayLocator(interval=10, bymonthday=range(5, 25))
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

average_use_break = off_season_hrs['percent_use'].mean()
average_use_school = in_school_hrs['percent_use'].mean()

xalign = 0.05

# off peak average line
plt.axhline(average_use_break, ls=':', lw=2, c='tab:blue', alpha=.5)
plt.annotate(f'{average_use_break:.0%} avg. hourly use during break', xy=(date_min + 1, average_use_break),
             xytext=(date_min + 10, .1), c='tab:blue',
             arrowprops={'arrowstyle': '->', 'connectionstyle': "angle,angleA=180,angleB=90", 'color': 'tab:blue',
                         'lw': '.5', 'alpha': 0.75})
# school season line
plt.axhline(average_use_school, ls=':', lw=2, c='tab:red', alpha=.5)
plt.annotate(f'{average_use_school:.0%} avg. hourly use \n during class', xy=(date_min + 20, average_use_school),
             xytext=(date_min + 10, .55), c='tab:red',
             arrowprops={'arrowstyle': '->', 'connectionstyle': "angle,angleA=180,angleB=90", 'color': 'tab:red',
                         'lw': '.5', 'alpha': 0.75})

plt.text(.1, .95, f'{date_min + 2} to {date_max - 2}\n  {capacity_total:,d} spaces total', size=7, va='top', c='gray',
         ha='center', transform=ax.transAxes)

plt.suptitle(f'CSU Garages (South, Prospect, West, Central, East)', size=15)
plt.tight_layout()
plt.savefig('./exports/ex1.png')
