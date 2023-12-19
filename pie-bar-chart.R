library(ggplot2)

# Set the seed for reproducibility
set.seed(123)

# Generate random data
categories <- c("Beer", "Wine", "Liquor - Mixed", "Liquor - Straight", "Non-alcoholic")
percentages <- c(1, .8, .75, .4, .2)
s <- sum(percentages)
percentages <- percentages / s

# Create a data frame
data <- data.frame(categories, percentages)

# Sort the data frame by descending order of proportions
data <- data[order(data$percentages, decreasing = TRUE), ]

library(RColorBrewer)

cp <- brewer.pal(length(categories), "Dark2")
# Create a pie chart using ggplot2
chart <- ggplot(data, aes(x = "", y = percentages, fill = categories)) +
  geom_bar(stat = "identity", width = 1) +
  coord_polar("y", start = 0) +
  labs(fill = "Categories", x = NULL, y = NULL, title = "What do people order at the bar?") +
  theme_void() +
  theme(legend.position = "bottom") +
  scale_fill_manual(values = cp) +
  geom_text(aes(label = paste0(round(percentages * 100), "%")), 
            position = position_stack(vjust = 0.5))  # Add data labels

chart

# Generate random data
categories <- c("Apple", "Peach", "Pumpkin", "Pecan", "Key Lime", "Other")
percentages <- c(1, .8, .75, .4, .6, .3)
s <- sum(percentages)
percentages <- percentages / s

# Create a data frame
data <- data.frame(categories, percentages)

# Sort the data frame by descending order of proportions
data <- data[order(data$percentages, decreasing = TRUE), ]

library(RColorBrewer)

cp <- brewer.pal(length(categories), "Dark2")
# Create a pie chart using ggplot2
chart <- ggplot(data, aes(x = categories, y = percentages)) +
  geom_bar(stat = "identity", fill = "steelblue") +
  scale_y_continuous(labels = scales::percent_format()) +
  labs(x = "Type of Pie", y = "Percentage of People", title = "Favorite Pie") +
  theme_minimal() +
  theme(legend.position = "bottom") +
  scale_fill_manual(values = cp)
  
chart

