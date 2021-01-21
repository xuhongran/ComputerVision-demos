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

import numpy as np
import cv2

#Load the image
original = cv2.imread("../figures/santorini.jpeg")
#Set the desired scale
scale = 10
#Resize the original image
original = cv2.resize(original, (int(original.shape[1]/scale), int(original.shape[0]/scale)) , interpolation=cv2.INTER_AREA)

#Apply filters with different borders
kernel_size = 3
constant = cv2.boxFilter(original, cv2.CV_8U, (kernel_size, kernel_size), borderType=cv2.BORDER_CONSTANT)
replicate = cv2.boxFilter(original, cv2.CV_8U, (kernel_size, kernel_size), borderType=cv2.BORDER_REPLICATE)
reflect = cv2.boxFilter(original, cv2.CV_8U, (kernel_size, kernel_size), borderType=cv2.BORDER_REFLECT)
isolated = cv2.boxFilter(original, cv2.CV_8U, (kernel_size, kernel_size), borderType=cv2.BORDER_ISOLATED)

#Combine the images together
result = np.concatenate((original, constant), axis=1)
result = np.concatenate((result, replicate), axis=1)
result = np.concatenate((result, reflect), axis=1)
result = np.concatenate((result, isolated), axis=1)

cv2.namedWindow("Borders")
cv2.imshow("Borders", result)
cv2.waitKey()