import cv2
import os
import numpy as np

# Opens all images in an image folder and appends it to a list
image_folder = "test_images"
images = []
for i in os.listdir(image_folder):
    image = cv2.imread(f'{image_folder}/{i}')
    # image = cv2.resize(image, (320, 240))
    images.append(image)
print(len(images))

stitcher = cv2.Stitcher.create(mode=1)
(status, result) = stitcher.stitch(images)
if (status == cv2.STITCHER_OK):
    print("Stitch Generated")
else:
    print("Stitch Failed")

cv2.imwrite("result_image/stitch.jpg", result)
print(result.shape)
cv2.waitKey(0)
