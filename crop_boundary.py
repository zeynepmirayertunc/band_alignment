"""
TODO: Explain the aim of the "crop_boundary.py" script briefly. 
https://www.python.org/dev/peps/pep-0257/

"""



import cv2
import os
import settings


def cropped_black_boundary_images(imagepath):
    """
    TODO: Explain the function briefly. What is the aim of this function?
    TODO: What is input?
    TODO: What is output? 
    TODO: Are there any exceptions? For example, what happens if someone tries to run this function with binary image.    
    """
    img = cv2.imread(imagepath)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #  !!! You assume that the given image is RGB, but I couldn't see any control in your code for that assumption.
    _, thresh = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
    _, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnt = contours[0]
    x, y, w, h = cv2.boundingRect(cnt)
    crop_black = img[y:y + h, x:x + w]
    return crop_black

def cropped(crop,crop2):
    """
    TODO: Explain the function.
    """
    h = crop.shape[0]
    w = crop.shape[1]
    crop2 = cv2.resize(crop2, (w, h))
    return crop2

for i in range(len(settings.NIR_im_paths)):

    NIR_crop = cropped_black_boundary_images(settings.NIR_im_paths[i])
    RED_crop = cropped_black_boundary_images(settings.RED_im_paths[i])

    # Why do you need cropped function?
    # RED_crop = cv2.resize(RED_crop, (NIR_crop.shape[1], NIR_crop.shape[0]))
    RED_crop = cropped(NIR_crop, RED_crop) 


    cv2.imwrite(os.path.join(settings.out_NIR, "NIR" + str(i)+".tif"), cv2.cvtColor(NIR_crop, cv2.COLOR_RGB2GRAY))
    cv2.imwrite(os.path.join(settings.out_NIR, "RED" + str(i)+".tif"), cv2.cvtColor(RED_crop, cv2.COLOR_RGB2GRAY))

