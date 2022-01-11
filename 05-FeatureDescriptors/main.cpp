extern int featureDetectionMatching();
extern int harris( const char *filename);

#include "CameraCalibration.h"
//#include "CameraCalibration_in_class.h"

int main()  {
   //featureDetectionMatching();

 //   harris("/home/charalambos/Downloads/assignment3_sample_images/Boxes.png");

    calibrate();

    return 0;
}
