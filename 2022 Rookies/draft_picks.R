library(nflreadr)
library(tidyverse)

draft <- load_draft_picks(seasons = 2024) %>%
  select(pfr_player_name, round, pick, team, position)

write.csv(draft, "C:\\Users\\bborh\\Documents\\Fantasy Football\\Rookie Ranking\\2024 Rookies\\draft_picks.csv")
