import cv2
import os


def cropped_black_boundary_images(imagepath):
    img = cv2.imread(imagepath)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
    _, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnt = contours[0]
    x, y, w, h = cv2.boundingRect(cnt)
    crop_black = img[y:y + h, x:x + w]
    return crop_black

input_folder = "D:\\3_Sinif\Staj\\NIRalign"
input_folder2 = "D:\\3_Sinif\Staj\\REDalign"
directory = os.listdir(input_folder)
image_list = []
image_list2 = []
directory = os.listdir(input_folder)
directory2 = os.listdir(input_folder2)
# print(directory)

for files,files2 in zip(directory,directory2):
        file_path = os.path.join(input_folder, files)
        file_path2 = os.path.join(input_folder2, files2)
        image_list.append(file_path)
        image_list.sort(key=lambda image_list: image_list[:-5])
        image_list2.append(file_path2)
        image_list2.sort(key=lambda image_list2: image_list2[:-5])
# print(image_list2)

def cropped(crop,crop2):
    h = crop.shape[0]
    w = crop.shape[1]
    crop2 = cv2.resize(crop2, (w, h))
    return crop2

for i in range(len(image_list)):
    crop = cropped_black_boundary_images(image_list[i])
    crop2 = cropped_black_boundary_images(image_list2[i])
    crop2 = cropped(crop, crop2)
    cv2.imwrite('D:\\3_Sinif\\Staj\\NIRCropped\\' "NIR" + str(i) + ".tif", cv2.cvtColor(crop, cv2.COLOR_RGB2GRAY))
    cv2.imwrite('D:\\3_Sinif\\Staj\\REDCropped\\' "RED" + str(i) + ".tif", cv2.cvtColor(crop2, cv2.COLOR_RGB2GRAY))

