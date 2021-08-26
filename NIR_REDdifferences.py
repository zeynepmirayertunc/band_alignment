import cv2
import os
import numpy as np

input_folder = "D:\\3_Sinif\Staj\\NIRCropped"
input_folder2 = "D:\\3_Sinif\Staj\\REDCropped"
directory = os.listdir(input_folder)
image_list = []
image_list2 = []
directory = os.listdir(input_folder)
directory2 = os.listdir(input_folder2)
# print(directory)
for files, files2 in zip(directory, directory2):
    file_path = os.path.join(input_folder, files)
    file_path2 = os.path.join(input_folder2, files2)
    image_list.append(file_path)
    image_list.sort()
    image_list2.append(file_path2)
    image_list2.sort()


def differencescalculation(img1_path, img2_path):
    img1 = cv2.imread(img1_path, 0)
    img2 = cv2.imread(img2_path, 0)
    # --- take the absolute difference of the images ---
    res = cv2.absdiff(img1, img2)

    # --- convert the result to integer type ---
    res = res.astype(np.uint8)

    # --- find percentage difference based on number of pixels that are not zero ---
    percentage = (np.count_nonzero(res) * 100) / res.size
    return percentage


for i in range(len(image_list)):
    pct = differencescalculation(image_list[i], image_list2[i])
    print(pct)
