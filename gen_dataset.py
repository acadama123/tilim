import pandas as pd
import geopandas as gpd
import os
import shutil
from shapely.geometry import Polygon, Point

'''
    NOTE: Funky bug when running this script with Washington_pure_swine_500_more and cafo_img,
    the switch to Washington_other_swine_farms and cafo_img_2 where cafo_img_2 will contain
    all images from cafo_img, instead of the new images.
    Bug doesn't seem to occur if run the script in Python shell.
    Likely some optimizations with shutil that stored the copied files.
'''

pure_swine = pd.read_csv("Washington_pure_swine_500_more.csv")
# pure_swine = pd.read_csv("Washington_other_swine_farms.csv")
lats = pure_swine['Latitude']
longs = pure_swine['Longitude']

farm_coordinates = []
for i in range(len(lats)):
    farm_coordinates.append(Point(longs[i], lats[i]))
'''
countyPath = "./county/county.shp"
countyBorder = gpd.read_file(countyPath)

wgs84Proj = 4326
countyBorderLatLong = countyBorder.to_crs(epsg=wgs84Proj)
washingtonBorder = countyBorderLatLong['geometry'][28]

for i in range(len(farm_coordinates)):
    if not washingtonBorder.contains(farm_coordinates[i]):
        print(farm_coordinates[i].bounds)
'''

img_dir_path = "./img_splitted"
filenames = [f for f in os.listdir(img_dir_path) if os.path.isfile(os.path.join(img_dir_path, f))]

img_geom_list = []
for name in filenames:
    # file name has form: "imageID_latmin,longmin,latmax,longmax.png"
    coord_str = name[:name.rindex('.')] # Removes the .png extension
    coordinates = coord_str.split(',')
    latmin = float(coordinates[0])
    longmin = float(coordinates[1])
    latmax = float(coordinates[2])
    longmax = float(coordinates[3])
    img_geom_list.append(Polygon([(latmin,longmin), (latmin, longmax), (latmax, longmax), (latmax, longmin)]))

cafo_img_dir_path = "./cafo_img"
# cafo_img_dir_path = "./cafo_img_2"
if not os.path.exists(cafo_img_dir_path):
    os.makedirs(cafo_img_dir_path)

print(len(farm_coordinates), len(img_geom_list))

for i in range(len(farm_coordinates)):
    for j in range(len(img_geom_list)):
        if img_geom_list[j].contains(farm_coordinates[i]):
            old_loc = os.path.join(img_dir_path, filenames[j])
            if not os.path.exists(old_loc):
                print("Same image " + str(i) + " " + filenames[j])
                break
            new_name = str(i) + "_" + filenames[j]
            new_loc = os.path.join(cafo_img_dir_path, new_name)
            shutil.move(old_loc, new_loc)
            break
