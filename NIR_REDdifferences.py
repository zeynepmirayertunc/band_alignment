# -*- coding: utf-8 -*-
"""
@author: Zeynep Miray

In this script, the matching accuracy of the aligned images is measured by the def function below, and then
 the results obtained using the logging module are saved in the differences.log file.

"""

import cv2
import numpy as np
import settings
import logging


logging.basicConfig(level=logging.INFO, filename='differences.log',  filemode='w')

def differences_calculation(img1path, img2path):
    """
    This function was written to measure the matching accuracy of two aligned images. The Absdiff method used in
     this function makes subtraction between two given matrices. Then the percentage is calculated from the result
     of this subtraction.

     Inputs:
            img1path,img2path - File path of aligned, cropped and resized images of the same area

    Output:
            percentage - Percentage of match accuracy
    """
    # Read the images
    img1 = cv2.imread(img1path, 0)
    img2 = cv2.imread(img2path, 0)

    # Take the absolute difference of the images
    res = cv2.absdiff(img1, img2)

    # Convert the result to integer type
    res = res.astype(np.uint8)

    # Find percentage difference based on number of pixels that are not zero ---
    percentage = (np.count_nonzero(res) * 100) / res.size
    return percentage


for i in range(len(settings.NIRCropped_im_paths)):
    pct = differences_calculation(settings.NIRCropped_im_paths[i], settings.REDCropped_im_paths[i])
    logging.info(" {} %".format(pct))
