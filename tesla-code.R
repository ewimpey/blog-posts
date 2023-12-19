teslas  <- c(6, 9)
vehicles <- c(95, 86)
prop.test(teslas, vehicles, correct = FALSE)

sf_teslas <- 9
nc_teslas <- 6
sf_non <- 75
nc_non <-90

getBetaParams <- function(mu, sigma){
  alpha = mu**2 * ((1 - mu) / sigma**2 - 1 / mu)

  beta = alpha * (1 / mu - 1)

  return(c(alpha, beta))
}

beta_params <- getBetaParams(.05, .05)
alpha = beta_params[1]
beta = beta_params[2]

#Sampling 10,000 random variables from the posterior distributions of SF and Cary
n = 10000
post1 = rbeta(n,alpha+sf_teslas,beta+sf_non)
post2 = rbeta(n,alpha+nc_teslas,beta+nc_non)

# plotting two posterior distributions
df <- data.frame(proportion = c(post1, post2), City = c(rep("SF", n), rep("Cary", n)))
ggplot(df, aes(x = proportion, fill = City)) +
  geom_histogram(alpha = 0.5, position = "identity") +
  scale_fill_manual(values = c("blue", "red")) +
  labs(title = "Posterior Distribution of Tesla Rate",
       x = "Tesla Rate",
       y = element_blank()) +
  theme(axis.text.y = element_blank(),
        axis.ticks.y = element_blank()) +
  scale_x_continuous(labels = scales::percent)

#Calulating posterior samples from pi1 - pi2
posterior = post1 - post2

ggplot() + aes(posterior) + geom_histogram() +
  xlab("Percentage Point Difference") +
  ylab(element_blank()) +
  labs(title = "Difference in rate of Teslas",
       subtitle = "San Francisco, CA and Cary, NC") +
  geom_vline(xintercept = 0, color = "red") +
  theme(axis.text.y = element_blank(),
        axis.ticks.y = element_blank()) +
  scale_x_continuous(labels = scales::percent)
