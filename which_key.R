
get_keys <- function(iter = 100000, num_keys = 50){
  orig_keys <- c(rep("L", num_keys - 1), "W") # One winning key, the rest are losers
  pos <- c()
  for (i in 1:iter){ # try this many times
    keys <- sample(orig_keys) # Shuffle up the winning key
    p <- which(keys == "W") # Get the position of the winning key
    pos <- c(pos, p)
  }
  return(pos)
}

# Get the distribution of winning keys
l = get_keys()

# Assume I walked up when there are 20 keys left
l2 <- l[l<=20]

# I could pull the key at any point remaining, so lets try them all
# If I picked the key when there were n remaining, the only time I win is if the nth key was the winner
df <- data.frame(winner = l2)

# While it's already obvious now...let's plot it just to see how silly I should feel
library(ggplot2)
ggplot(df, aes(x = winner)) +
  geom_histogram(bins = 20, fill = "steelblue") +
  xlab("Key") +
  ylab("Frequency of Winning") +
  ggtitle("Which key should you pick?")

