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

require(reshape2)
require(imager)
require(lattice)
require(ggplot2)


library(imager)
library(lattice)

#ONLY WORKS ON SQUARE IMAGES. DATA FRAME CREATION DOES NOT HANDLE RECTANGULAR MATRICES.

#Noisy image
fpath <- 'noise_example.png'
#Smoothed image
#fpath <- 'noise_example_gaussian.png'

img <- load.image(fpath)

plot(img)

size = width(img)

img <- resize(img, size/4, size/4)
size = size/4

data = data.frame(
  x = rep(c(1:size),each=size),
  y = rep(c(1:size),each=size)
)

data$z = c(img[,,,1])

data
str(data)

wireframe(z ~ x * y, data=data)

p <- wireframe(z ~ x * y, data=data)
npanel <- c(4, 2)
rotx <- c(-50, -80)
rotz <- seq(30, 300, length = npanel[1]+1)
update(p[rep(1, prod(npanel))], layout = npanel,
       panel = function(..., screen) {
         panel.wireframe(..., screen = list(z = rotz[current.column()],
                                            x = rotx[current.row()]))
       })

#PROFILE OF COLUMN 15
row_number = 15
row = c(img[,row_number,3])
  
data = data.frame(
  x = c(1:size),
  y = row
)

ggplot(data) + 
  geom_line(aes(y=y, x=x)) +
  geom_point(aes(x = x, y = y), size = 3) 
#  stat_smooth(aes(y=y, x=x), method = lm, formula = y ~ poly(x, 10), se = FALSE)


#FIRST DERIVATIVE
intensity <- row
dx <- c(NA, 1:(size-1),0)
for (i in 2:size){
  dx[i] = intensity[i] - intensity[i-1]  
}

data = data.frame(
  x = c(1:(size+1)),
  y = c(dx)
)

ggplot(data) + 
  geom_line(aes(y=y, x=x)) +
  geom_point(aes(x = x, y = y), size = 3) 

