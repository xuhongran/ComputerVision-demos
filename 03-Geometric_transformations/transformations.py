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

import cv2 as cv
import numpy as np

#Cartesian coordinates in Euclidean space 2D
rectangle = np.array([[100, 150],
                      [200, 150],
                      [200, 250],
                      [100, 250]])


#Convert to homogeneous coordinates 3D
rectangle_h = np.ones((4,2+1))
rectangle_h[:,:-1] = rectangle

#projective transformation
projective = np.array([
    [10.0, 40.0, 10.0],
    [50.0, -40.0, 300.0],
    [1.0, 2.0, 1]
])

#Affine transformation i.e. last row 0,0,1, any linear transformation followed by a translation
affine = np.array([
    [2.0, 4.0, -500.0],
    [5.0, -2.0, 300.0],
    [0.0, 0.0, 1.0]
])

#Similarity transformation i.e. scale, rotation, translation
similarity = np.array([
    [2.0*np.cos(np.pi/4), -np.sin(np.pi/4), 100.0],
    [np.cos(np.pi/4), 2.0*np.sin(np.pi/4), 100.0],
    [0.0, 0.0, 1.0]
])

#Euclidean transformation i.e. rigid; rotation and translation only
euclidean = np.array([
    [np.cos(np.pi/4), -np.sin(np.pi/4), 300.0],
    [np.cos(np.pi/4), np.sin(np.pi/4), 100.0],
    [0.0, 0.0, 1.0]
])

key = ''
transformation = euclidean
while (key != ord('q')):
    key = cv.waitKey(0)
    #Switch between the transformations
    if key == ord('1'):
        transformation = euclidean
    elif key == ord('2'):
        transformation = similarity
    elif key == ord('3'):
        transformation = affine
    elif key == ord('4'):
        transformation = projective
    else:
        transformation = euclidean

    #Draw the original in red color; polylines takes 2D points as input
    canvas = np.zeros((1024, 1024, 3), dtype="uint8")
    canvas = cv.polylines(canvas, [rectangle], True, (0, 0, 255), 3)

    #Transform the rectangle
    transformed_rectangle_h = np.matmul(transformation, np.transpose(rectangle_h)).transpose()
    #print(transformed_rectangle_h)
    #Divide by w
    for i in range(4):
        transformed_rectangle_h[i,:] /= transformed_rectangle_h[i,2]
    #Convert from homogeneous to Cartesian by dropping w
    transformed_rectangle = np.ones((4,2))
    transformed_rectangle = transformed_rectangle_h[:,:-1]
    transformed_rectangle = transformed_rectangle.astype(int)
    # print(transformed_rectangle)

    #Draw the transformed rectangle with blue color
    canvas = cv.polylines(canvas, [transformed_rectangle], True, (255, 0, 0),3)

    #Show the canvas
    cv.imshow('Transformations', canvas)

cv.destroyAllWindows()