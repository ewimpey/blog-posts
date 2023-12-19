library(baseballr)
library(dplyr)
library(ggplot2)

game_data <- read.csv("C:/Users/evan.wimpey/Downloads/splits.csv")

phils <- game_data %>% 
  filter(Tm == "PHI") %>%
  select(HR) %>%
  mutate(data = "Regular Season")

ggplot(phils, aes(x = HR)) +
  geom_histogram(binwidth = 1) +
  labs(title = "Phils HR/game",
       subtitle = "Regular Season",
       y = "Games") +
  theme_bw()

phils_ws <- data.frame(HR = c(1,0,5,0,1,1)) %>%
  mutate(data = "World Series")

df <- rbind(phils, phils_ws)

ggplot(df, aes(x = HR)) +
  geom_density(binwidth = 1) +
  labs(title = "Phillies Home Runs per Game",
       #subtitle = "World Series",
       y = element_blank(),
       x = element_blank()) +
  theme(axis.ticks.y = element_blank(),
           axis.line.y = element_blank(),
           axis.text.y = element_blank()) +
  facet_wrap(~ data)
