import os
from shapely.geometry import Polygon
from matplotlib import pyplot as plt
import geopandas as gpd
import pandas as pd

img_dir_path = "./rejected_img"
filenames = [f for f in os.listdir(img_dir_path) if os.path.isfile(os.path.join(img_dir_path, f))]

rejected_boundaries = []

for name in filenames:
    # file name has form: "imageID_latmin,longmin,latmax,longmax.png"
    coord_str = name[:name.rindex('.')] # Removes the .png extension
    coordinates = coord_str.split(',')
    latmin = float(coordinates[0])
    longmin = float(coordinates[1])
    latmax = float(coordinates[2])
    longmax = float(coordinates[3])

    img_boundary = Polygon([(latmin,longmin), (latmin, longmax), (latmax, longmax), (latmax, longmin)])
    rejected_boundaries.append(img_boundary)

data_rejected = {'geometry': rejected_boundaries}
df_rejected = pd.DataFrame(data_rejected)
gdf_rejected = gpd.GeoDataFrame(df_rejected, geometry='geometry')

countyPath = "./county/county.shp"
countyBorder = gpd.read_file(countyPath)

wgs84Proj = 4326
countyBorderLatLong = countyBorder.to_crs(epsg=wgs84Proj)
washingtonBorder = countyBorderLatLong['geometry'][28]
data_washington = {'geometry': [washingtonBorder]}
df_washington = pd.DataFrame(data_washington)
gdf_washington = gpd.GeoDataFrame(df_washington, geometry='geometry')

fig, ax = plt.subplots()
gdf_washington.plot(ax=ax, color='r')
gdf_rejected.plot(ax=ax)
plt.show()
