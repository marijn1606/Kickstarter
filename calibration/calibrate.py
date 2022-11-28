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
images = glob.glob("calibration/*.jpeg")
print(len(images))
for fname in images:
    img = cv.imread(fname)
    img = cv.resize(img, (1640, 1232))
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
        cv.waitKey(200)
    else:
        print("No corners found")
cv.destroyAllWindows()

ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(
    objpoints, imgpoints, gray.shape[::-1], None, None)

print("Camera matrix : \n")
print(mtx)
print("dist : \n")
print(dist)
print("rvecs : \n")
print(rvecs)
print("tvecs : \n")
print(tvecs)

with open("calibration/matrix.txt", 'w') as f:
    f.write("Camera matrix : \n")
    f.write(np.array2string(mtx))
    f.write("\n\ndist : \n")
    f.write(np.array2string(dist))
