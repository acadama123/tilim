import geopandas as gpd
from matplotlib import pyplot as plt
import requests
import json
from PIL import Image
from io import BytesIO

iowaPath = "./iowa_border/iowa_border.shp"
countyPath = "./county/county.shp"

# Read shapefiles; result are GeoDataFrame objs
iowaBorder = gpd.read_file(iowaPath)
countyBorder = gpd.read_file(countyPath)

# Re-projecting the objs to the WGS84 Latitude/Longitude projection
# so we can work with latitudinal and longitudinal values.
wgs84Proj = 4326
iowaBorderLatLong = iowaBorder.to_crs(epsg=wgs84Proj)
countyBorderLatLong = countyBorder.to_crs(epsg=wgs84Proj)

iowaBorderLatLong.plot()
countyBorderLatLong.plot()
plt.show()

# NAIP Image server: https://gis.apfo.usda.gov/arcgis/rest/services/NAIP/USDA_CONUS_PRIME/ImageServer
# Spatial reference: https://spatialreference.org/ref/sr-org/epsg3857-wgs84-web-mercator-auxiliary-sphere/

"""
    To get image tiles: https://developers.arcgis.com/rest/services-reference/image-tile.htm
    Sample url: https://gis.apfo.usda.gov/arcgis/rest/services/NAIP/USDA_CONUS_PRIME/ImageServer/tile/17/45000/22000
"""

washingtonBorder = countyBorderLatLong['geometry'][28]
#li = list(washingtonBorder.exterior.coords)
#for i in range(len(li)):
#    li[i] = list(li[i])

xmin, ymin, xmax, ymax = washingtonBorder.bounds
#xmin, ymin, xmax, ymax = iowaBorderLatLong['geometry'][0].bounds
'''
https://gis.apfo.usda.gov/arcgis/rest/services/NAIP/USDA_CONUS_PRIME/ImageServer/query?where=&objectIds=&time=&geometry=%7B%22xmin%22%3A-91.94686042840655%2C%22ymin%22%3A41.16158400402034%2C%22xmax%22%3A-91.48410932887417%2C%22ymax%22%3A41.51182793250474%2C%22spatialReference%22%3A%7B%22wkid%22%3A4326%7D%7D&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&relationParam=&outFields=&returnGeometry=true&outSR=&returnIdsOnly=false&returnCountOnly=false&pixelSize=&orderByFields=&groupByFieldsForStatistics=&outStatistics=&returnDistinctValues=false&multidimensionalDefinition=&returnTrueCurves=false&maxAllowableOffset=&geometryPrecision=&f=html
'''
# Unsafe characters need encoding in URLs
geometry_json = "%7B%22xmin%22%3A" + str(xmin) + "%2C%22ymin%22%3A" + str(ymin) + "%2C%22xmax%22%3A" + str(xmax) + "%2C%22ymax%22%3A" + str(ymax) + "%2C%22spatialReference%22%3A%7B%22wkid%22%3A" + str(wgs84Proj) + "%7D%7D"
image_id_request_url = "https://gis.apfo.usda.gov/arcgis/rest/services/NAIP/USDA_CONUS_PRIME/ImageServer/query?geometry=" + geometry_json + "&geometryType=esriGeometryEnvelope&spatialRel=esriSpatialRelIntersects&returnDistinctValues=false&returnTrueCurves=false&f=pjson"

response = requests.get(image_id_request_url)
response_dict = json.loads(response.content)
image_info_list = response_dict['features']

def get_bounds(envelope_bound_list):
    '''
        envelope_bound_list: A list of lists, where each inner list contains
        contains the x and y coordinates of a corner of the envelope. The final
        inner list has the same value as the first inner list, due to requirements
        of the ring geometry.
    '''
    cur_xmin = envelope_bound_list[0][0]
    cur_xmax = envelope_bound_list[0][0]
    cur_ymin = envelope_bound_list[0][1]
    cur_ymax = envelope_bound_list[0][1]

    for i in [1, 2, 3]:
        if (envelope_bound_list[i][0] < cur_xmin):
            cur_xmin = envelope_bound_list[i][0]
        if (envelope_bound_list[i][0] > cur_xmax):
            cur_xmax = envelope_bound_list[i][0]
        if (envelope_bound_list[i][1] < cur_ymin):
            cur_ymin = envelope_bound_list[i][1]
        if (envelope_bound_list[i][1] > cur_ymax):
            cur_ymax = envelope_bound_list[i][1]

    return (cur_xmin, cur_ymin, cur_xmax, cur_ymax)

image_id_list = []
image_bounds_list = []
for i in range(len(image_info_list)):
    image_id_list.append(image_info_list[i]['attributes']['OBJECTID'])
    image_bounds_list.append(get_bounds(image_info_list[i]['geometry']['rings'][0]))

# for i in range(len(image_info_list)):
#     print(image_id_list[i], image_bounds_list[i])

folder_path = "./img"

https://gis.apfo.usda.gov/arcgis/rest/services/NAIP/USDA_CONUS_PRIME/ImageServer/exportImage?bbox=-1.07632041902E7%2C5302462.938199997%2C-1.07562447902E7%2C5311972.338200003&bboxSR=&size=3887%2C+3887&imageSR=&time=&format=jpgpng&pixelType=UNKNOWN&noData=&noDataInterpretation=esriNoDataMatchAny&interpolation=+RSP_BilinearInterpolation&compression=&compressionQuality=&bandIds=&mosaicRule=&renderingRule=&f=html
for i in range(len(image_bounds_list)):
    bounding_box = str(image_bounds_list[i][0]) + "%2C" + str(image_bounds_list[i][1]) + "%2C" + str(image_bounds_list[i][2]) + "%2C" + str(image_bounds_list[i][3])
    json_request_url = "https://gis.apfo.usda.gov/arcgis/rest/services/NAIP/USDA_CONUS_PRIME/ImageServer/exportImage?bbox=" + bounding_box + "&size=2990%2C+3887&format=png&pixelType=UNKNOWN&noDataInterpretation=esriNoDataMatchAny&interpolation=+RSP_BilinearInterpolation&f=pjson"
    json_response = requests.get(json_request_url)
    json_response_dict = json.loads(json_response.content)
    image_request_url = json_response_dict['href']
    image_response = requests.get(image_request_url)
    img = Image.open(BytesIO(image_response.content))
    # Uses coordinates from json_response since the image's actual bounds differ from the bounds that we sent due to image sizing.
    img.save(folder_path + "/" + str(image_id_list[i]) + "_" + str(json_response_dict['extent']['xmin']) + "," + str(json_response_dict['extent']['ymin']) + "," + str(json_response_dict['extent']['xmax']) + "," + str(json_response_dict['extent']['ymax']) + ".png")
    print("Finished image " + str(i) + " of " + str(len(image_bounds_list)))
