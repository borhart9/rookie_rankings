library(readxl)
library(tidyverse)

WR_2020 <- read_excel("C:/Users/bborh/OneDrive - The Ohio State University/Fantasy Football/2020_Rookie_Profiles.xlsx", 
                 sheet = "Wide Receivers")
WR_2020$TDPG <- WR_2020$Rec.TDs/WR_2020$Games.Played

wr.lm <- lm(FPPG ~ TDPG + Pick.No, data = WR_2020)
summary(wr.lm)
wr.lm$coefficients

WR_2021 <- read_excel("C:/Users/bborh/OneDrive - The Ohio State University/Fantasy Football/2021_Rookie_Profiles.xlsx", 
                      sheet = "Wide Receivers")
WR_2021$TDPG <- WR_2021$Rec.TDs/WR_2021$Games.Played

WR_2021$FPPG <- round(wr.lm$coefficients[1] + 
  (WR_2021$TDPG * wr.lm$coefficients[2]) + 
  (WR_2021$Pick.No * wr.lm$coefficients[3]), 2)

player <- WR_2021 %>% select(Player, FPPG)

plot(WR_2020$Rec.TDs, WR_2020$FPPG)

summary(lm(FPPG ~ TDPG, data = WR_2020))
