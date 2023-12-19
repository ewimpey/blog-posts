# Load necessary libraries
library(ggplot2)

# Define the parabola function
parabola <- function(x) {
  return(x^2)
}

# Create data for the parabola
x_vals <- seq(-5, 5, by = 0.1)
parabola_data <- data.frame(x = x_vals, y = parabola(x_vals))

# Define the tangent points
tangent_point1 <- c(2, parabola(2))
tangent_point2 <- c(-2, parabola(-2))

# Create data for the tangent lines
tangent1_data <- data.frame(x = c(tangent_point1[1] - 1, tangent_point1[1] + 1),
                            y = c(tangent_point1[2] - 2, tangent_point1[2] + 2))

tangent2_data <- data.frame(x = c(tangent_point2[1] - 1, tangent_point2[1] + 1),
                            y = c(tangent_point2[2] + 2, tangent_point2[2] - 2))

# Create the plot
plot <- ggplot() +
  geom_line(data = parabola_data, aes(x = x, y = y), color = "blue") +
  geom_segment(data = tangent1_data, aes(x = x, y = y, xend = x, yend = y), color = "red") +
  geom_segment(data = tangent2_data, aes(x = x, y = y, xend = x, yend = y), color = "green") +
  annotate("text", x = tangent_point1[1] + 1, y = tangent_point1[2] - 0.5, label = "Sunglasses tangled in hair", color = "red") +
  annotate("text", x = tangent_point2[1] - 1, y = tangent_point2[2] + 0.5, label = "Sunglasses sliding off head", color = "green") +
  annotate("text", x = 0, y = min(parabola_data$y) - 1, label = "Minimum Cost (Ideal Hair Lenght)", color = "blue") +
  labs(title = "Hair Descent", x = "Hair Lenght", y = "Cost") +
  theme_minimal() +
  theme(axis.text = element_blank(),  # Remove axis text
        axis.ticks = element_blank())

# Display the plot
print(plot)
