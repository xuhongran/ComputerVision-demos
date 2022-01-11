#ifndef __CAMERA_CALIBRATION_H__
#define __CAMERA_CALIBRATION_H__

#include <opencv2/imgproc/types_c.h>
#include "opencv2/opencv.hpp"

#define PATTERN_TILES_X                 9
#define PATTERN_TILES_Y                 6
#define PATTERN_TILE_WIDTH      35
#define PATTERN_TILE_HEIGHT    35

bool findCorrespondences(cv::Mat const &calibration_image, std::vector<cv::Point2f> &corners)    {
    cv::Size pattern_size(PATTERN_TILES_X,PATTERN_TILES_Y); //interior number of corners
    cv::Mat gray_calibration_image;
    cvtColor( calibration_image, gray_calibration_image, CV_BGR2GRAY );

    //this will be filled by the detected corners

    //CALIB_CB_FAST_CHECK saves a lot of time on images
    //that do not contain any chessboard corners
    bool patternfound = cv::findChessboardCorners(gray_calibration_image, pattern_size, corners, cv::CALIB_CB_ADAPTIVE_THRESH + cv::CALIB_CB_NORMALIZE_IMAGE + cv::CALIB_CB_FAST_CHECK);

    if(patternfound)    {
        cv::cornerSubPix(gray_calibration_image, corners, cv::Size(11, 11), cv::Size(-1, -1), cv::TermCriteria(CV_TERMCRIT_EPS + CV_TERMCRIT_ITER, 30, 0.1));

        cv::Mat dummy = calibration_image;
        cv::drawChessboardCorners(calibration_image, pattern_size, cv::Mat(corners), patternfound);
        cv::imshow("Current frame", calibration_image);
        while (true)    {
            int key = cv::waitKey(0);
            switch (key)    {
            case 13:    ///ENTER - accept the image
                            return true;
                            break;
            case 8:     ///BACKSPACE - reject the image
                            return false;
            }
        }
    }
    return false;
}

void captureFrames(cv::Size &image_size, std::vector<std::vector<cv::Point2f> > &calibration_images_corners)    {
    cv::VideoCapture cap("udp://10.5.5.9:8554",cv::CAP_FFMPEG); // open the default camera
    if(!cap.isOpened())  // check if we succeeded
        return;
std::cout << "video captured" << std::endl;

    char file_name[100];
    cv::Mat current_frame;
    std::vector<cv::Point2f> corners;
//    cv::namedWindow("Current frame",1);
    bool not_done = true;
    int counter = 0;
    while(not_done) {
        ///Get a new frame from camera each time
        cap >> current_frame;
        image_size = current_frame.size();
        ///Show it in the window
//        cv::imshow("Current frame", current_frame);
        sprintf(file_name, "calibration_image_%d.png",counter++);
        std::cout << file_name << std::endl;
        cv::imwrite(file_name, current_frame);

        /*
        int key = cv::waitKey(1);
        switch(key) {
            case 13: corners.clear();
                            if (findCorrespondences(current_frame, corners))    {
                                calibration_images_corners.push_back(corners);
                                sprintf(file_name, "calibration_image_%d.png",calibration_images_corners.size());
                                cv::imwrite(file_name, current_frame);
                                std::cout << "Calibration images so far: " << calibration_images_corners.size() << std::endl;
                            }
                            break;
            case 27: not_done = false;
                            break;
            default: break;
        }
*/
    }

    std::cout << "Total calibration images: " << calibration_images_corners.size() << std::endl;
//    cv::destroyAllWindows();
    return;
}

void calculateParameters(cv::Size const &image_size, std::vector<std::vector<cv::Point2f> > const &calibration_images_corners,
                                                    cv::Mat &camera_matrix, cv::Mat &distortion_coeffs, std::vector<cv::Mat> &rvecs, std::vector<cv::Mat> &tvecs)    {
    int number_of_images = calibration_images_corners.size();
    std::vector<std::vector<cv::Point3f> > all_object_points;

    for (int i=0;i<number_of_images;i++)   {
        std::vector<cv::Point3f> object_points;
        for (int j=0;j<calibration_images_corners[i].size();j++)    {
            object_points.push_back(cv::Point3f( PATTERN_TILE_WIDTH*float(j%PATTERN_TILES_X),
                                                                                    PATTERN_TILE_WIDTH*float(j/PATTERN_TILES_X),
                                                                                    0.0f));
        }
        all_object_points.push_back(object_points);
    }

    ///Run the calibration
   cv::calibrateCamera(all_object_points, calibration_images_corners, image_size, camera_matrix, distortion_coeffs, rvecs, tvecs);

    std::cout << "Camera matrix: " << camera_matrix << std::endl;
    std::cout << "Distortion coefficients: " << distortion_coeffs << std::endl;
    for (int i=0;i<number_of_images;i++)    {
        std::cout << "Image " << i << ": " << std::endl;
        std::cout << rvecs[i] << std::endl;
        std::cout << tvecs[i] << std::endl;
        std::cout << "----------------------------------------" << std::endl;
    }

    return;
}

void undistortedVideo(cv::Mat const &camera_matrix, cv::Mat const &distortion_coeffs)    {
/*
    cv::Mat view, rview, map1, map2;
    cv::Size imageSize = calibration_images[0].size();
    cv::initUndistortRectifyMap(camera_matrix, distortion_coeffs, cv::Mat(),
      getOptimalNewCameraMatrix(camera_matrix, distortion_coeffs, imageSize, 1, imageSize, 0),
      imageSize, CV_16SC2, map1, map2);

  for(int i = 0; i < calibration_images.size(); i++ ) {
      view = calibration_images[i];
      if(view.empty())  continue;
      cv::remap(view, rview, map1, map2, cv::INTER_LINEAR);
      cv::imshow("Image View", rview);
      cv::waitKey(0);
  }
  */

    cv::VideoCapture cap(0); // open the default camera
    if(!cap.isOpened())  // check if we succeeded
        return;

    char file_name[100];
    cv::Mat current_frame;
    std::vector<cv::Point2f> corners;
    cv::namedWindow("Undistorted feed",1);
    bool not_done = true;
    cv::Mat undistorted;
    while(not_done) {
        ///Get a new frame from camera each time
        cap >> current_frame;
        cv::undistort(current_frame, undistorted, camera_matrix, distortion_coeffs);

        ///Show it in the window
        cv::imshow("Undistorted feed", undistorted);

        int key = cv::waitKey(1);
        switch(key) {
            case 13:
                            break;
            case 27: not_done = false;
                            break;
            default: break;
        }
    }
    return;
}

bool calibrate()    {

    cv::Size image_size;
    std::vector<std::vector<cv::Point2f> > calibration_images_corners;
    captureFrames(image_size, calibration_images_corners);

    cv::Mat camera_matrix;
    cv::Mat distortion_coeffs;
    std::vector<cv::Mat> rvecs;
    std::vector<cv::Mat> tvecs;

    calculateParameters(image_size, calibration_images_corners, camera_matrix, distortion_coeffs, rvecs, tvecs);

    undistortedVideo(camera_matrix, distortion_coeffs);
    return true;
}




#endif // __CAMERA_CALIBRATION_H__
