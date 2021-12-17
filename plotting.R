library(tidyverse)
library(dplyr)
library(lubridate)
library(ggplot2)

capacity<- c(south=611,prospect= 291, west=600, central=867, east= 600) # from https://www.csuohio.edu/parking/xxx-garages
capacity_total = sum(capacity)

df <- read_csv('./CSU_parking_live.csv')

columns <- colnames(df)
space_cols <- columns[grepl('spaces', columns)]

perc_df <- df %>%
  mutate(percopen= (1-rowSums(df[,space_cols], na.rm=TRUE) / capacity_total) *100) %>%
  select(c('date','percopen')) %>%
  mutate(block = floor_date(date, "15 mins") , day = date(date),
         time= factor(strftime(block, " %H:%M"))
         ) %>%
  group_by(block) %>%
  mutate(percopen2=min(percopen)) %>%
  ungroup() %>%
  filter(percopen == percopen2)



countdf <- df %>%
  mutate(percopen= (1-rowSums(df[,space_cols], na.rm=TRUE) / capacity_total) *100) %>%
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
  geom_line( aes(x=time, y=percopen,group=day, color=phase), alpha=.33,show.legend = TRUE,size=.5 ) +
  guides(x=guide_axis(angle = 90), color=guide_legend()  ) +
  scale_x_discrete(breaks=breaks[seq(1,96,5)]) +
  scale_color_manual(values=c('red','blue')) +
  labs(x= 'Time of Day (24H)', color='School\nSemester', y='Percent Occupied %',
       title='Cleveland State Daily Parking Occupancy') +
  ylim(10,100)


ggsave('./exports/DailyCycle_R.png', dpi=300, width = 8, type='cairo' )



# By Garage

garagedf <- df %>%
  pivot_longer(!date,
               names_to = c(".value"),
               names_pattern = "gar_\\d_(.*)") %>%
  select(!ends_with('perc')) %>%
  mutate(open_total = rowSums(across(ends_with('openspaces')))) %>%
  mutate(
    block = floor_date(date, "15 mins") ,
    day = date(date),
    time = factor(strftime(block, " %H:%M"))
  ) %>%
  filter(permit_openspaces > 0 & public_openspaces >0) %>%
  mutate( week = factor(weekdays(date),
                        levels=c('Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday')))
  
  

garagedf %>%
  ggplot() +
  geom_line( aes(x=time, y=open_total,group=day, color=name), alpha=.2,show.legend = TRUE,size=.1 ) +
  guides(x=guide_axis(angle = 90)) +
  scale_x_discrete(breaks=breaks[seq(1,96,20)]) +
  labs(x= 'Time of Day (24H)', color='School\nSemester', y='Open Spaces',
       title='Cleveland State Daily Parking Occupancy By Garage and Weekday') +
  facet_grid(name~week)

ggsave('./exports/GarageBreakdown_R.png', dpi=300, width = 12, type='cairo' )
