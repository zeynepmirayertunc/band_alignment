# -*- coding: utf-8 -*-

"""
@author: Zeynep Miray

Feature-based methods are methods that look for salient features in both images (such as edges, lines, and vertices)
 and then try to match them in a separate matching step. Many feature-based methods are available. In this script,
 it is aimed to perform the most accurate alignment of an NIR band image to a Red band image or vice versa using
 the def(align_images) function below, then save these images to a file.
"""

import numpy as np
import cv2
import os
import time
import NIR_REDbuffer
import settings

start_time = time.time()

redimage_list, nirimage_list = NIR_REDbuffer.select_images(settings.dir_ALLimages)


def align_images(moving, fixed, dtc, mtch):
    """
    This align_images function performs the alignment of two images relative to each other using the "feature-based"
     image alignment technique. A sparse set of features is detected in one image and mapped to features in the other
     image. Binary options are presented to the user in choosing the descriptor method, matcher method and motion
     model to be used for these operations.

    Inputs:
            moving - Image to be distorted (the image you want to align)
            fixed  - The image to be matched
            dtc    - dtc is the value used for detector selection. If you enter 1, you will use SIFT detector, if you
                      enter 2, you will use SURF detector. (The settings.py file should be used to change the hessian
                      threshold for the SURF method)

            mtch   - mtch is the value used for matcher selection. If you enter "f" you will use FlannBased mathcer,
             if you enter "b" you will use Brute Force matcher.


    Outputs:
           out_img - An image aligned to the other image that has the same dimensions as the original image.
    """
    MIN_MATCH_COUNT = 10

    moving_im = cv2.imread(moving, cv2.IMREAD_GRAYSCALE)  # read the image to be distorted
    fixed_im = cv2.imread(fixed, cv2.IMREAD_GRAYSCALE)  # read the image to be matched

    # Initiate detector
    detector = settings.switch_detector(dtc)

    # find the keypoints and descriptors
    kp1, des1 = detector.detectAndCompute(moving_im, None)
    kp2, des2 = detector.detectAndCompute(fixed_im, None)

    # use FLANN method to match keypoints. Brute force matches not appreciably better
    # and added processing time is significant.
    matcher = settings.switch_matcher(mtch)

    # find the corresponding point pairs (match descriptors)
    matches = matcher.knnMatch(des1, des2, k=2)

    # store all the good matches following Lowe's ratio test.
    good = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            good.append(m)

    print(str(len(good)) + " Matches were Found")

    # Extract location of good matches
    if len(good) > MIN_MATCH_COUNT:
        src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
        dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)

        # choose the appropriate motion model(If you want to use the findHomography method,
        # simply change this part to settings.findHomography(src_pts, dst_pts) )
        M, _ = settings.estimateAffine2D(src_pts, dst_pts)

        h, w = moving_im.shape  # shape of input images, needs to remain the same for output

        # Warp source image to destination based on motion model
        out_img = cv2.warpPerspective(moving_im, M, (w, h))

        return out_img


    else:
        print("Not enough matches are found for moving image")


print("The merging starting. Depending on the excess of the images this can take from a few seconds to many minutes.")
for i in range(0, len(redimage_list)):
    nir = align_images(os.path.join(settings.dir_ALLimages, nirimage_list[i]),
                       os.path.join(settings.dir_ALLimages, redimage_list[i]), 2, "f")

    red = align_images(os.path.join(settings.dir_ALLimages, redimage_list[i]),
                       os.path.join(settings.dir_ALLimages, nirimage_list[i]), 2, "f")

    cv2.imwrite(os.path.join(settings.out_NIRdir, "NIR" + str(i) + ".tif"), nir)
    cv2.imwrite(os.path.join(settings.out_REDdir, "RED" + str(i) + ".tif"), red)

print(str(i) + "\t", "Images Completely Merged.")
print("--- %s seconds ---" % (time.time() - start_time))
