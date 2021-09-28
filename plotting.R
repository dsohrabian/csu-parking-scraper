library(tidyverse)
library(dplyr)
library(lubridate)
library(ggplot2)

capacity_total <- sum(c(611, 291, 600, 867, 600))

df <- read_csv('./CSU_parking_live.csv')

columns <- colnames(df)
space_cols <- columns[grepl('spaces', columns)]
df$percopen <- (1-rowSums(df[,space_cols], na.rm=TRUE) / capacity_total) *100

perc_df <- df %>%
  select(c('date','percopen')) %>%
  mutate(block = floor_date(date, "15 mins") , day = date(date),
         time= factor(strftime(block, " %H:%M"))
         ) %>%
  group_by(block) %>%
  mutate(percopen2=min(percopen)) %>%
  ungroup() %>%
  filter(percopen == percopen2)



countdf <- df %>%
  select(c('date','percopen')) %>%
  mutate(block = floor_date(date, "15 mins") , day = date(date),
         time= factor(strftime(block, " %H:%M"))
         ) %>%
  group_by(day) %>%
  summarize(blockcount = n_distinct(time)) %>%
  filter(blockcount > 70)

perc_df <- perc_df %>%
  filter(day %in% countdf$day) %>%
  mutate(phase= factor(ifelse(day < "2021-08-20", 'Summer', 'Fall')))

breaks <- unique(perc_df$time) %>% sort()

perc_df %>%
  ggplot() +
  stat_smooth(geom='line', aes(x=time, y=percopen,group=day, color=phase),
  alpha=.5,show.legend = TRUE,size=.5 ) +
  guides(x=guide_axis(angle = 90), color=guide_legend()  ) +
  scale_x_discrete(breaks=breaks[seq(1,96,5)]) +
  scale_color_manual(values=c('red','blue')) +
  labs(x= 'Time of Day (24H)', color='School\nSemester', y='Percent Occupied %',
       title='Cleveland State Daily Parking Occupancy') +
  ylim(10,100)


ggsave('./exports/DailyCycle_R.png', dpi=300, type='cairo' )
