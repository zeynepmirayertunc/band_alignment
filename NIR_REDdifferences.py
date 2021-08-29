"""
TODO: Explain the script

"""

import cv2
import os
import numpy as np
import settings



def differences_calculation(img1path, img2path):
    """
    TODO: Function explanation ??
    """
    img1 = cv2.imread(img1path, 0)
    img2 = cv2.imread(img2path, 0)
    # --- take the absolute difference of the images ---
    res = cv2.absdiff(img1, img2)

    # --- convert the result to integer type ---
    res = res.astype(np.uint8)

    # --- find percentage difference based on number of pixels that are not zero ---
    percentage = (np.count_nonzero(res) * 100) / res.size
    return percentage


for i in range(len(settings.NIRCropped_im_paths)):
    pct = differences_calculation(settings.NIRCropped_im_pathst[i], settings.REDCropped_im_paths[i])
    print(pct) # If you need to monitor this section, you can use the logging module
