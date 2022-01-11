cmake_minimum_required(VERSION 3.6)
project(demos)

add_definitions(-DNO_XML -DCMAKE_BUILD_TYPE=RELEASE)

#Set the correct output directory
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/bin")

set (CMAKE_MODULE_PATH "${CMAKE_SOURCE_DIR}/cmake")	#include a script to find all Find*.cmake files


## Compiler flags
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -O2 -std=c++11")
set(CMAKE_EXE_LINKER_FLAGS "-s")  ## Strip binary

include_directories(.)


## OpenCV
find_package(OpenCV REQUIRED)
#MESSAGE(STATU "OpenCV LIBS:" ${OpenCV_LIBS})
#MESSAGE(STATU "OpenCV Includes:" ${OpenCV_INCLUDE_DIRS})
# Moving all #include "opencv.hpp" to #include "opencv2/opencv.hpp"
include_directories(/usr/include/opencv)


set(SOURCE_FILES
        CameraCalibration.h
        main.cpp)

add_executable(demos ${SOURCE_FILES})
target_link_libraries(demos
                        ${ImageMagick_LIBRARIES}
                        ${LIBFFTW3_LIBRARY}
                        ${OpenCV_LIBS})