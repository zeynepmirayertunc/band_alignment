# -*- coding: utf-8 -*-

"""
TODO: Explain the script

"""
import os
from GPSPhoto import gpsphoto
import simplekml
import pandas as pd
from shapely.geometry import Point
from geopandas import GeoDataFrame
import matplotlib.pyplot as plt
from glob import glob
import settings

# Please follow the PEP8 Guide https://www.python.org/dev/peps/pep-0008/
# Explain your variables and functions
kml = simplekml.Kml() # Why? 
kml2 = simplekml.Kml() # Why?

coordinates = []
images = []
islemimages = [] 




def ayıkla(dircont):  # Is it possible to rename this function? "ı" letter can be problematic for some systems.
    """
    TODO: Explain the function
    """
    for files in settings.directory:
        if files.endswith('.tif') and files[-5].endswith('3'):
            file_path = os.path.join(dircont, files)
            images.append(file_path)
            # print(file_path)
            # Get the data from image file and return a dictionary
            data = gpsphoto.getGPSData(file_path)
            # print("Data:", data)
            if data:
                kml.newpoint(name=file_path, coords=[(data['Longitude'], data['Latitude'])])
                coordinates.append(data)
    kml.save("photos.kml")
    df = pd.DataFrame.from_dict(coordinates)
    df["Image Names"] = images
    
    df.to_csv('coordinates.csv')
    df2 = pd.read_csv('coordinates.csv')
    geometry = [Point(xy) for xy in zip(df.Longitude, df.Latitude)]
    crs = {'init': 'epsg:4326'}  # http://www.spatialreference.org/ref/epsg/2263/
    geo_df = GeoDataFrame(df2, crs=crs, geometry=geometry)
    buffer = geo_df.geometry[30].buffer(0.002)
    selected = geo_df.intersects(buffer)
    df["Selected"] = selected
 

    new = []
    for i in range(len(df)):
        if df.iloc[i]["Selected"]:
            islemimages.append(df.iloc[i]["Image Names"])
            kml2.newpoint(name=df.iloc[i]["Image Names"], coords=[(df.iloc[i]["Longitude"], df.iloc[i]["Latitude"])])
            coordinate = {df.iloc[i]["Image Names"], df.iloc[i]["Longitude"], df.iloc[i]["Latitude"]}
            new.append(coordinate)
            kml2.save("selected_photos.kml")

    nir_b = glob(os.path.join(dircont, '*_4.tif'))
    nir_b.sort()
    newlist = []
    for items in nir_b:
        for numbers in islemimages:
            if items[-14:-6] == numbers[-14:-6]:
                newlist.append(items)

    return islemimages,newlist



