library(nflreadr)
library(tidyverse)

draft <- load_draft_picks(seasons = 2024) %>%
  select(pfr_player_name, round, pick, team, position)

write.csv(draft, "Rookie Ranking\\2024 Rookies\\draft_picks.csv")
