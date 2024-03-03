# Linear Regression from scratch
data("mtcars")

# Split the data into X and y matrices
y <- data.matrix(mtcars[,1])
x <- data.matrix(mtcars[,2:11])

# add a column of 1 for an intercept estimate
int_col <- rep(1, nrow(x))
x <- cbind(int_col, x)

# linear algebra for solution
params_manual <- solve(t(x) %*% x) %*% (t(x) %*% y) 

# test against built in method
params_lm <- lm(mpg ~ ., data = mtcars)

# viewing manually calculated params
params_manual
# viewing params from lm
params_lm$coefficients
