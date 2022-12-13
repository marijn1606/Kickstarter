import numpy as np
import cv2 as cv
import glob
# import os

# termination criteria
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((10*15, 3), np.float32)
objp[:, :2] = np.mgrid[0:15, 0:10].T.reshape(-1, 2)
# Arrays to store object points and image points from all the images.
objpoints = []  # 3d point in real world space
imgpoints = []  # 2d points in image plane.
images = glob.glob("cal_img_*.jpeg")
print(len(images))
for fname in images:
    img = cv.imread(fname)
    # img = cv.resize(img, (1640, 1232))
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # Find the chess board corners
    ret, corners = cv.findChessboardCorners(gray, (15, 10), None)
    # If found, add object points, image points (after refining them)
    if ret == True:
        objpoints.append(objp)
        corners2 = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        imgpoints.append(corners2)
        # Draw and display the corners
        cv.drawChessboardCorners(img, (15, 10), corners2, ret)
        cv.imshow('img', img)
        cv.waitKey(100)
    else:
        print("No corners found")
cv.destroyAllWindows()

ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(
    objpoints, imgpoints, gray.shape[::-1], None, None)

distorted_image = cv.imread("test_image.jpeg")
# distorted_image = cv.resize(distorted_image, (1640, 1232))
h, w = distorted_image.shape[:2]
print(h, w)
new_camera_matrix, roi = cv.getOptimalNewCameraMatrix(
    mtx, dist, (w, h), 1, (w, h))

undistorted_image = cv.undistort(
    distorted_image, mtx, dist, None, new_camera_matrix)

cv.namedWindow("dist", cv.WINDOW_NORMAL)
cv.resizeWindow("dist", 1280, 720)
cv.imshow("dist", distorted_image)

cv.namedWindow("undist", cv.WINDOW_NORMAL)
cv.resizeWindow("undist", 1280, 720)
cv.imshow("undist", undistorted_image)

cv.waitKey(0)

print("Camera matrix : \n")
print(mtx)
print("dist : \n")
print(dist)
print("New camera matrix : \n")
print(new_camera_matrix)
# print("rvecs : \n")
# print(rvecs)
# print("tvecs : \n")
# print(tvecs)

# with open("matrix.txt", 'w') as f:
#     f.write("Camera matrix : \n")
#     f.write(np.array2string(mtx))
#     f.write("\n\ndist : \n")
#     f.write(np.array2string(dist))
