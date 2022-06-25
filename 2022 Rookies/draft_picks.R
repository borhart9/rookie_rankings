library(nflreadr)
library(tidyverse)

draft <- load_draft_picks(seasons = 2022) %>%
  select(pfr_name, round, pick, team, position)

write.csv(draft, "draft_picks.csv")
