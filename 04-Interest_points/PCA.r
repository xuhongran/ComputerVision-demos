#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <https://www.gnu.org/licenses/>.

#     Written by Charalambos (Charis) Poullis - www.poullis.org

library (mvtnorm)
library(mixtools)  

N <- 200 # Number of random samples
set.seed(153)
# Target parameters for univariate normal distributions
rho <- -0.5
mu1 <- 1; s1 <- 2
mu2 <- 1; s2 <- 8

# Parameters for bivariate normal distribution
mu <- c(mu1,mu2) # Mean
sigma <- matrix(c(s1^2, s1*s2*rho, s1*s2*rho, s2^2), nrow = 2) # Covariance matrix

# This function draws an ellipse based on a normal distribution
# alpha: Probability to be excluded from the ellipse. The default value is alpha = .05, which results in a 95% ellipse.
ellipse_from_dist <- function(dist, alpha){
  #Calculate the mean
  mean_x <- mean(dist[,1])
  mean_y <- mean(dist[,2])
  means = c(mean_x, mean_y)
  C <- cov(dist)
  ellipse(means, C, alpha = alpha, col="coral", lwd = 3, asp=1)
}

dist <- mvtnorm::rmvnorm(N,mu,sigma, method="svd")
colnames(dist) <- c("X","Y")

plot(dist, xlab="X",ylab="Y",main= "Principal Component Analysis", asp=1)
ellipse_from_dist(dist,.5)
ellipse_from_dist(dist,.05)

#Calculate the mean
mean_x <- mean(dist[,1])
mean_y <- mean(dist[,2])
center <- c(mean_x, mean_y)
#Calculate covariance matrix
C <- cov(dist)
#Calculate the eigenvectors and eigenvalues
e <- eigen(C)
eigen_values  <- e$values
eigen_vectors  <- e$vectors
# scale the eigenvectors to length = sqrt
scaled_eigen_vectors  <- eigen_vectors %*% diag(sqrt(eigen_values))  

#Form the two endpoints for each eigenvector
end_pt1 <- center + scaled_eigen_vectors[,1]
end_pt2 <- center + scaled_eigen_vectors[,2]

#Draw the +- lines along the eigenvectors
xMat    <- rbind(center[1] + scaled_eigen_vectors[1, ], center[1] - scaled_eigen_vectors[1, ])
yMat    <- rbind(center[2] + scaled_eigen_vectors[2, ], center[2] - scaled_eigen_vectors[2, ])
matlines(xMat, yMat, lty=1, lwd=2, col="cornflowerblue")


#Eigenvectors (Blue: largest eigenvalue, Red: second larger eigenvalue )
arrows(center[1], center[2], end_pt1[1], end_pt1[2], col = "blue", lwd=3, asp=1)
arrows(center[1], center[2], end_pt2[1], end_pt2[2], col = "red", lwd=3, asp=1)

#Draw the mean
points(center[1], center[2], pch=4, col="black", lwd=3)
