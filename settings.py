import os
import cv2
import numpy as np

# CROP BOUNDARY SCRIPT Settings

in_NIR = "D:\\3_Sinif\Staj\\NIRalign"
in_RED = "D:\\3_Sinif\Staj\\REDalign"
out_NIR = 'D:\\3_Sinif\\Staj\\NIRCropped\\'
out_RED = 'D:\\3_Sinif\\Staj\\REDCropped\\'
dir_NIR = os.listdir(in_NIR)
dir_RED = os.listdir(in_RED)

NIR_im_paths = []
RED_im_paths = []
for f_nir, f_red in zip(dir_NIR, dir_RED):
    fp_NIR = os.path.join(in_NIR, f_nir)
    fp_RED = os.path.join(in_RED, f_red)
    NIR_im_paths.append(fp_NIR)
    NIR_im_paths.sort(key=lambda NIR_im_paths: NIR_im_paths[:-5])
    RED_im_paths.append(fp_RED)
    RED_im_paths.sort(key=lambda RED_im_paths: RED_im_paths[:-5])

# NIR_REDdifferences Settings

input_folder = "D:\\3_Sinif\Staj\\NIRCropped"
input_folder2 = "D:\\3_Sinif\Staj\\REDCropped"
dir_NIRCropped = os.listdir(out_NIR)
dir_REDCropped = os.listdir(out_RED)

NIRCropped_im_paths = []
REDCropped_im_paths = []

for f_nir_c, f_red_c in zip(dir_NIRCropped, dir_REDCropped):
    fp_NIR_c = os.path.join(out_NIR, f_nir_c)
    fp_RED_c = os.path.join(out_RED, f_red_c)
    NIRCropped_im_paths.append(fp_NIR_c)
    NIRCropped_im_paths.sort()
    REDCropped_im_paths.append(fp_RED_c)
    REDCropped_im_paths.sort()

# NIR_REDBuffer Settings
dir_ALLimages = "D:\\3_Sinif\Staj\\ceylanpinar"
directory = os.listdir(dir_ALLimages)

# NIR_REDCombine Settings
out_NIRdir = 'D:\\3_Sinif\\Staj\\NIRalign\\'
out_REDdir = 'D:\\3_Sinif\\Staj\\REDalign\\'


def SIFT():
    return cv2.xfeatures2d_SIFT.create()


def SURF():
    return cv2.xfeatures2d_SURF.create(19)


def default():
    print("Incorrect detector")


case1 = {

    1: SIFT,
    2: SURF,
}


def switch_detector(dtctor_method):
    return case1.get(dtctor_method, default)()


# ---------------------------------------------------------
def flann():
    return cv2.FlannBasedMatcher()


def bf():
    return cv2.BFMatcher()


def default():
    print("Incorrect method")


case2 = {

    "f": flann,
    "b": bf,
}


def switch_matcher(matcher_method):
    return case2.get(matcher_method, default)()


# ---------------------------------------------------------

def findHomography(pts_1, pts_2):
    # Variables caused by rotation, translation and distortion can be found with the 3*3 homography
    # matrix that associates two images with each other using the RANSAC method.
    M, _ = cv2.findHomography(pts_1, pts_2, cv2.RANSAC)
    return M, _


def estimateAffine2D(pts_1, pts_2):
    M, _ = cv2.estimateAffine2D(pts_1, pts_2)
    M = np.vstack((M, [0, 0, 1]))
    return M, _
