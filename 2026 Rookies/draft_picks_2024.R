library(nflreadr)
library(tidyverse)

draft <- load_draft_picks(seasons = 2026) %>%
  select(pfr_player_name, round, pick, team, position)

write.csv(draft, "2026 Rookies\\draft_picks.csv")
