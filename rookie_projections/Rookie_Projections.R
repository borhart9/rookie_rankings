library(readxl)
library(tidyverse)
Rookies <- read_excel("C:/Users/bborh/OneDrive - The Ohio State University/Fantasy Football/2020_Rookie_Profiles.xlsx", 
                      sheet = "Running Backs")


model <- lm(FPPG ~ log(Rush.Atts), data = Rookies)
predict(model, newdata = data.frame(Rush.Atts = 251), interval = "confidence", level = .80)


summary(lm(FPPG ~ log(Rush.Atts), data = Rookies))


plot(log(Rookies$Rush.Atts), Rookies$FPPG)
