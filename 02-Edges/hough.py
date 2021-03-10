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
import cv2 as cv

#Example demonstrating Hough transform using OpenCV

#The video capture
vid = None
#Bypass the video setup
setup_video_capture = True
#The current frame
frame =  0
#The array with the lines returned by HoughLines
lines = []
#Type of Hough transform algorithm. OpenCV has 2 different implementations: standard and probabilistic
type = True
#All keys and their ordinals
keys = {chr(i):i for i in range(0,127)}
#Minimum number of votes
min_number_of_votes = 100
#Keep reading frames until 'q' is pressed
while (True):
    #Configure the video capture
    while (setup_video_capture):
        #Capture a frame if video capture has been initialized
        if vid:
            ret, frame = vid.read()
            if not ret:
                frame = 0
        cv.imshow('frame', frame)
        #Wait for the next key
        key = cv.waitKey()
        if key == keys['q'] or key == keys['Q']: # Quit
            #Release the video capture
            if vid:
                vid.release()
            #Kill all the CV windows
            cv.destroyAllWindows()
            exit()
        elif key == keys['\r'] or key == keys['\n']: #Enter (CR or newline)
            #The configuration is done. break the inner loop
            setup_video_capture = False
            break
        else:
            for (k,v) in keys.items():
                if v  == key and v in range(keys['0'], keys['9']+1):    #Number from 0 to 9
                    if vid:
                        vid.release()
                    #Try capturing from this device ID
                    devID = keys[k] - keys['0']
                    print("Attempting video capture of devide: {0}".format(devID))
                    vid = cv.VideoCapture(devID)
                    break

    #read the next frame
    ret, frame = vid.read()
    #Convert to grayscale
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    #Get the edge map
    edges = cv.Canny(gray, 100,200, L2gradient= True)

    #Apply Hough transform
    if type:
        lines = cv.HoughLines(edges, 1, np.pi / 180, min_number_of_votes)
        if lines is None:
            pass
        else:
            #Otherwise convert to Euclidian space and draw on the image
            for line in lines:
                for rho, theta in line:
                    a = np.cos(theta)
                    b = np.sin(theta)
                    x0 = a * rho
                    y0 = b * rho
                    x1 = int(x0 + 1000 * (-b))
                    y1 = int(y0 + 1000 * (a))
                    x2 = int(x0 - 1000 * (-b))
                    y2 = int(y0 - 1000 * (a))

                    cv.line(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
    else:
        # minLineLength = 100
        # maxLineGap = 10
        lines = cv.HoughLinesP(edges, 1, np.pi / 180, min_number_of_votes) #minLineLength, maxLineGap)
        if lines is None:
            pass
        else:
            for line in lines:
                for x1, y1, x2, y2 in line:
                    cv.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # Show the annotated frame
    cv.imshow('frame', frame)

    #If you press 'q' then quit
    key = cv.waitKey(2)
    if key == keys['q'] or key == keys['Q']:
        # Release the video capture
        if vid:
            vid.release()
        # Kill all the CV windows
        cv.destroyAllWindows()
        exit()
    if key == keys[' ']: #Spacebar switches between the hough implementations
        type = not type
        if type:
            print('Switching to standard Hough transform')
        else:
            print('Switching to probabilistic Hough transform')
    #Increase the minimum threshold for the votes
    if key == keys['+']:
        min_number_of_votes+=1
    #Decrease the minimum threshold for the votes
    if key == keys['-']:
        min_number_of_votes-=1
    #Reset the minimum number for the votes
    if key == keys['`']:
        min_number_of_votes = 100

print("Should never reach this point!")

