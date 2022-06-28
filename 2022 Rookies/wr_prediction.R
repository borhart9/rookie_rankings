library(tidyverse)
library(readxl)

setwd("C:/Users/bborh/OneDrive - The Ohio State University/Fantasy Football/Rookie Ranking/2022 Rookies")
WR_data <- read_excel("2022_Rookie_Profiles.xlsx", 
                      sheet = "Wide Receivers") %>%
  mutate(Power5_ND=ifelse(Conference %in% c("SEC", "Big Ten", "ACC", "Big 12", "Pac-12") | School == "ND", 
                          1, 0),
         SEC_Big10=ifelse(Conference %in% c("SEC", "Big Ten"), 1, 0),
         Top2=ifelse(Round <= 2, 1, 0), 
         Top3=ifelse(Round <= 3, 1, 0),
         Top4=ifelse(Round <= 4, 1, 0))
         
coef <- model2$coefficients

WR_data$FP <- coef[1] + coef[2] * WR_data$Top2 + coef[3] * WR_data$Power5_ND + 
  coef[4] * WR_data$Vac.Tar + coef[5] * WR_data$Rec.TDs
