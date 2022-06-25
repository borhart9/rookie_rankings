library(tidyverse)
library(nflreadr)

# load all snap counts throughout season
snaps <- load_snap_counts(2021) %>%
  filter(week <= 18) %>% 
  mutate(pfr_id = pfr_player_id) %>%
  select(player, week, position, offense_snaps, offense_pct, pfr_id) 
 

# load all offensive skill position rookies
rookies <- load_rosters(seasons = 2022) %>%
  filter(years_exp ==1, position %in% c("QB", "WR", "RB", "TE")) %>%
  mutate(player = full_name) %>%
  select(player, position, years_exp, pfr_id)


# join QBs to snap counts
qbs <- right_join(snaps, rookies, by="player") %>%
  filter(position.x == "QB")

# use 50% of game played to count as game
qbs %>%
  group_by(player) %>%
  filter(offense_pct >= .5) %>%
  summarize(games = n()) %>%
  view() 

# count snaps taken 
qbs %>%
  group_by(player) %>%
  summarize(snaps = sum(offense_snaps)) %>%
  view()


# join RBs to snap counts
rbs <- right_join(snaps, rookies, by="player") %>%
  filter(position.x == "RB") 


# use 35% of game played to count as game
rbs %>%
  filter(offense_pct >= .35) %>%
  group_by(player, pfr_id.x) %>%
  summarize(games = n()) %>%
  view()

# count snaps on field
rbs %>%
  group_by(player, pfr_id.x) %>%
  summarize(snaps = sum(offense_snaps)) %>%
  arrange(-snaps) %>%
  view()


# joins WRs to snap counts
wrs <- right_join(snaps, rookies, by="pfr_id") %>%
  filter(position.x == "WR")

# use 40% of game played to count as game
wrs %>%
  filter(offense_pct >= .40) %>%
  group_by(player.x, pfr_id) %>%
  summarize(games = n()) %>%
  arrange(-games) %>%
  view()

# count snaps played
wrs %>%
  group_by(player.x, pfr_id) %>%
  summarize(snaps = sum(offense_snaps)) %>%
  arrange(-snaps) %>%
  view()

# joins TEs to snap counts
tes <- right_join(snaps, rookies, by="pfr_id") %>%
  filter(position.x == "TE")

# use 30% of game played to count as game
tes %>%
  filter(offense_pct >= .35) %>%
  group_by(player.x, pfr_id) %>%
  summarize(games = n()) %>%
  arrange(-games) %>%
  view()

# count snaps played
tes %>%
  group_by(player.x, pfr_id) %>%
  summarize(snaps = sum(offense_snaps)) %>%
  arrange(-snaps) %>%
  view()
