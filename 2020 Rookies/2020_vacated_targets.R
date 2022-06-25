library(nflreadr)
library(tidyverse)

# load team abbreviations
teams <- load_teams()

teams$team_abbr[1]

vac_tar <- data.frame(cbind(teams$team_abbr, rep(NA, nrow(teams)))) %>%
  rename(Team = X1, Vac.Tar = X2)


for (i in 1:nrow(teams)) {
  # load stats for 2019 season
  stats2019 <- load_player_stats(seasons = 2019) %>%
    filter(recent_team == teams$team_abbr[i], season_type =="REG") %>%
    group_by(player_name, player_id) %>%
    summarize(targets = sum(targets)) %>%
    arrange(-targets)
  
  roster_2019 <- load_rosters(seasons = 2019) %>%
    filter(position %in% c("WR")) %>%
    mutate(player_name = 
             gsub(" ", 
                  "", 
                  paste(substring(first_name, first = 0, last = 1), ".", last_name)),
           player_id = gsis_id) %>%
    select(season, position, player_name, player_id)
  
  
  roster_2020 <- load_rosters(seasons = 2020) %>%
    filter(team == teams$team_abbr[i], position %in% c("WR")) %>%
    mutate(player_name = 
             gsub(" ", 
                  "", 
                  paste(substring(first_name, first = 0, last = 1), ".", last_name)),
           player_id = gsis_id) %>%
    select(season, position, player_name, player_id)
  
  wr_2019 <- right_join(roster_2019, stats2019, by="player_id") %>%
    filter(!is.na(position))
  
  
  lost_players <- left_join(wr_2019, roster_2020, by="player_id") %>%
    filter(is.na(player_name))
  
  
  
  lost_targets <- lost_players %>%
    mutate(position = "WR") %>%
    group_by(position) %>%
    summarize(targets = sum(targets)) 
  
  
  
  total_targets <- wr_2019 %>%
    group_by(position) %>%
    summarize(targets = sum(targets))
  
  targets <- rbind(lost_targets, total_targets)
  
  vac_tar$Vac.Tar[i] <- round((targets$targets[1])/(targets$targets[2])*100, 3)
}
vac_tar$Vac.Tar <- ifelse(is.na(vac_tar$Vac.Tar), 0, vac_tar$Vac.Tar)

write.csv(vac_tar, "2020_targets.csv", row.names = FALSE)

remove(lost_players, lost_targets, roster_2019, roster_2020, stats2019, targets, teams, 
       total_targets, wr_2019)