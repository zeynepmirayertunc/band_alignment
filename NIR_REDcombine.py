import numpy as np
import cv2
import os
import time
import NIR_REDbuffer

start_time = time.time()


# input_folder = "D:\\3_Sinif\Staj\\000"
input_folder = "D:\\3_Sinif\Staj\\ceylanpinar"
directory = os.listdir(input_folder)
# print(directory)

redimage_list, nirimage_list = NIR_REDbuffer.ayıkla(input_folder)


# print(len(redimage_list),redimage_list)
# print(len(nirimage_list),nirimage_list)
def align_images(moving, fixed):
    MIN_MATCH_COUNT = 10

    moving_im = cv2.imread(moving, 0)  # image to be distorted
    fixed_im = cv2.imread(fixed, 0)  # image to be matched

    # Initiate SIFT detector
    # sift = cv2.ORB_create(nfeatures=10000)
    surf = cv2.xfeatures2d_SURF.create(19)

    # find the keypoints and descriptors with SIFT
    kp1, des1 = surf.detectAndCompute(moving_im, None)
    kp2, des2 = surf.detectAndCompute(fixed_im, None)

    # use FLANN method to match keypoints. Brute force matches not appreciably better
    # and added processing time is significant.
    # FLANN_INDEX_KDTREE = 0
    # index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    # search_params = dict(checks=50)

    # matcher = cv2.DescriptorMatcher_create(cv2.DescriptorMatcher_FLANNBASED)
    # matcher =cv2.BFMatcher()
    matcher = cv2.FlannBasedMatcher()
    matches = matcher.knnMatch(des1, des2, k=2)

    # store all the good matches following Lowe's ratio test.
    good = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            good.append(m)

    print(str(len(good)) + " Matches were Found")

    if len(good) > MIN_MATCH_COUNT:
        src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
        dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)

        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC)
        # M, _ = cv2.estimateAffine2D(src_pts, dst_pts)
        # M = np.vstack((M, [0, 0, 1]))

        h, w = moving_im.shape  # shape of input images, needs to remain the same for output

        outimg = cv2.warpPerspective(moving_im, M, (w, h))

        return outimg


    else:
        print("Not enough matches are found for moving image")
        matchesMask = None


print("The merging starting. Depending on the excess of the images this can take from a few seconds to many minutes.")
for i in range(0, len(redimage_list)):
    # offset = [0, 0, 0, 0]
    # print(i)
    # tup = image_list
    nir = align_images(os.path.join(input_folder, nirimage_list[i]),
                       os.path.join(input_folder, redimage_list[i]))
    #
    # red = align_images(os.path.join(input_folder, redimage_list[i]),
    #                    os.path.join(input_folder, nirimage_list[i]))

    cv2.imwrite('D:\\3_Sinif\\Staj\\Ceylanpinar_NIR_Align\\' "NIR" + str(i) + ".tif", nir)
    # cv2.imwrite('D:\\3_Sinif\\Staj\\REDalign\\' "RED" + str(i) + ".tif", red)
print(str(i) + "\t", "Images Completely Merged.")
print("--- %s seconds ---" % (time.time() - start_time))
