# -*- coding: utf-8 -*-
"""
@author: Zeynep Miray

Aligned images obtained using NIR_REDcombine.py are saved using the size of the original images when saving to a file.
 Therefore, the parts cut from the aligned images appear as black corners. With the help of the following function
 in this script, the cropping of these black corners is performed. Then one of the two images is resized
 relative to the other.

"""

import cv2
import os
import settings


def cropped_black_boundary_images(imagepath):
    """
    This function performs the trimming of black edges formed around images. While doing this, firstly,
     if the image is RGB, it converts this image to a grayscale image, then a threshold is applied to this grayscale
     image to distinguish the black corners from the objects. Finally, by applying findContours to this threshold
     image, the rectangular boundaries of the area outside the black corners are determined and
     the new image is resized according to this limit.

    Input:
            imagepath - File path of the images to be cropped

    Output:
            crop_black - Cropped and resized image

    Exeption:
            Since this function is focused on thresholding the image, if you try this function with binary image,
             you will not get an accurate result.
    """
    # Read the image
    img = cv2.imread(imagepath)
    # If image is RGB, convert it into grayscale
    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img

    # Make in binary image for threshold value of 1
    # cv2.THRESH_BINARY: If pixel intensity is greater than the set threshold, value set to 255, else set to 0 (black)
    _, thresh = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)

    # Find contours in it and then find bounding rectangle for it
    _, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnt = contours[0]
    x, y, w, h = cv2.boundingRect(cnt)
    # Crop the image
    crop_black = img[y:y + h, x:x + w]

    return crop_black


for i in range(len(settings.NIR_im_paths)):

    NIR_crop = cropped_black_boundary_images(settings.NIR_im_paths[i])

    RED_crop = cropped_black_boundary_images(settings.RED_im_paths[i])
    RED_crop = cv2.resize(RED_crop, (NIR_crop.shape[1], NIR_crop.shape[0]))

    cv2.imwrite(os.path.join(settings.out_NIR, "NIR" + str(i) + ".tif"), NIR_crop)
    cv2.imwrite(os.path.join(settings.out_RED, "RED" + str(i) + ".tif"), RED_crop)





