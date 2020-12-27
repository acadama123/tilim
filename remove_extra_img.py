from shapely.geometry import Polygon
import geopandas as gpd
import os
import shutil

countyPath = "./county/county.shp"
countyBorder = gpd.read_file(countyPath)

wgs84Proj = 4326
countyBorderLatLong = countyBorder.to_crs(epsg=wgs84Proj)
washingtonBorder = countyBorderLatLong['geometry'][28]

img_dir_path = "./img_splitted"
filenames = [f for f in os.listdir(img_dir_path) if os.path.isfile(os.path.join(img_dir_path, f))]

rejected_img_dir_path = "./rejected_img"
if not os.path.exists(rejected_img_dir_path):
    os.makedirs(rejected_img_dir_path)

num_rejected = 0

for name in filenames:
    # file name has form: "imageID_latmin,longmin,latmax,longmax.png"
    coord_str = name[:name.rindex('.')] # Removes the .png extension
    coordinates = coord_str.split(',')
    latmin = float(coordinates[0])
    longmin = float(coordinates[1])
    latmax = float(coordinates[2])
    longmax = float(coordinates[3])

    img_boundary = Polygon([(latmin,longmin), (latmin, longmax), (latmax, longmax), (latmax, longmin)])
    if not (washingtonBorder.overlaps(img_boundary) or washingtonBorder.contains(img_boundary)):
        old_loc = os.path.join(img_dir_path, name)
        new_loc = os.path.join(rejected_img_dir_path, name)
        shutil.move(old_loc, new_loc)
        #print("Removed image " + name)
        num_rejected += 1

print("Number of rejected images: " + str(num_rejected))
