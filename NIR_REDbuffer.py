# -*- coding: utf-8 -*-

"""
@author: Zeynep Miray

When shooting with the UAV, the camera on the UAV starts to take images as soon as the UAV starts to take off.
 Using these meaningless images captured in Image Alignment processes will slow down the algorithm very much and
 is unnecessary. Therefore, using this script, the image reduction process is performed by the def(select_images)
 function below and the number of images to be used for alignment is reduced.

"""
import os
from GPSPhoto import gpsphoto
import pandas as pd
from shapely.geometry import Point
from geopandas import GeoDataFrame
from glob import glob
import settings

# Please follow the PEP8 Guide https://www.python.org/dev/peps/pep-0008/


coordinates = []  # A list with latitude longitude and altitude of all Red band images
images = []  # A list with all Red band images along with file path
processed_REDimgs = []  # A list of the Red band images in the buffer
processed_NIRimgs = []  # A list of the NIR band equivalents of the Red band images in the buffer


def select_images(dir_images):
    """
    This definition function enables images with red bands to be reduced to a certain area with the help of a buffer
     using GPS information (given directly in exif information) and transferring selected images to a list depending
     on the size of this buffer. Then, images with NIR band matching the image names in this list are transferred to
     another list. This function returns these two lists.

    Input:
            dir_images - File path of images with both bands(RED,NIR) of all images

    Outputs:
            processed_REDimgs - A list of the Red band images in the buffer
            processed_NIRimgs - A list of the NIR band equivalents of the Red band images in the buffer
    """
    # Get the RED band(3 is equal to RED band e.g. IMG_0453_3.tif) from image file and return a list
    for files in settings.directory:
        if files.endswith('.tif') and files[-5].endswith('3'):
            file_path = os.path.join(dir_images, files)
            images.append(file_path)

            # Get the data from image file and return a dictionary
            data = gpsphoto.getGPSData(file_path)

            # If the data is exist return a list that contains GPS informations of the images
            if data:
                coordinates.append(data)


    # Create a dataframe that contains GPS informations of the images
    df = pd.DataFrame.from_dict(coordinates)
    # Add the Image names from images list to dataframe as the Image Names
    df["Image Names"] = images

    # To create geo dataframe, create geometry by using the dataframe and set crs
    geometry = [Point(xy) for xy in zip(df.Longitude, df.Latitude)]
    crs = {'init': 'epsg:4326'}  # http://www.spatialreference.org/ref/epsg/2263/
    geo_df = GeoDataFrame(df, crs=crs, geometry=geometry)

    # Create a buffer to select some images
    buffer = geo_df.geometry[30].buffer(0.002)
    # Return a set that contains the items that exist in both geo_df, and buffer
    selected = geo_df.intersects(buffer)
    # Add the selected boolean to the dataframe
    df["Selected"] = selected

    # If boolean(selected) is true in the dataframe, add image names to a list
    for i in range(len(df)):
        if df.iloc[i]["Selected"]:
            processed_REDimgs.append(df.iloc[i]["Image Names"])

    # Get the NIR band(4 is equal to NIR band e.g. IMG_0453_4.tif) from image file and return a list
    nir_b = glob(os.path.join(dir_images, '*_4.tif'))
    nir_b.sort()

    # Compare in the list of all NIR band image names with the reduced red band images and assign the
    # matching NIR band images to a new list.
    for items in nir_b:
        for items2 in processed_REDimgs:
            if items[-14:-6] == items2[-14:-6]:
                processed_NIRimgs.append(items)

    return processed_REDimgs, processed_NIRimgs


