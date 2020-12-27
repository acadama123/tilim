import os
from pyproj import Proj, transform
from PIL import Image

img_width = 299
img_height = 299

def image_splitting (img_path, img_id, coordinates, folder_path="./img_splitted"):
    # Note that if the coordinates are lat-long,
    # then the x values should be latitudes
    # and the y values should be longitudes.
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    with Image.open(img_path) as img:
    width, height = img.size
    num_img_horizontal = width // img_width
    num_img_vertical = height // img_height
    x_delta = (coordinates[2] - coordinates[0]) / num_img_horizontal
    y_delta = (coordinates[3] - coordinates[1]) / num_img_vertical

    # Pixel location (0, 0) is at the top left corner of an image
    # Coordinate location (xmin, ymin) is at the bottom left corner of the image
    # idx = 0
    print("Start splitting")
    for i in range(num_img_vertical):
        for j in range(num_img_horizontal):
            # Cutting image from left to right, from top to bottom
            # Therefore, ymin and ymax of the small img are decrements of the large image's ymax
            xmin = coordinates[0] + x_delta * j
            xmax = coordinates[0] + x_delta * (j + 1)
            ymin = coordinates[3] - y_delta * (i + 1)
            ymax = coordinates[3] - y_delta * i

            left = img_width * j
            right = img_width * (j + 1)
            upper = img_height * i
            lower = img_height * (i + 1)

            new_img = img.crop((left, upper, right, lower))
            new_img.save(folder_path + "/" + str(xmin) + "," + str(ymin) + "," + str(xmax) + "," + str(ymax) + ".png")
            # new_img.save(folder_path + "/" + str(idx) + "_" + img_id + "_" + str(xmin) + "," + str(ymin) + "," + str(xmax) + "," + str(ymax) + ".png")
            # idx += 1

    img.close()

img_dir_path = "./img"
filenames = [f for f in os.listdir(img_dir_path) if os.path.isfile(os.path.join(img_dir_path, f))]

inProj = Proj('epsg:3857')
outProj = Proj('epsg:4326')

for name in filenames:
    # file name has form: "imageID_xmin,ymin,xmax,ymax.png"
    name_no_extension = name[:name.rindex('.')]
    img_id, coord_str = name_no_extension.split('_')
    coordinates = coord_str.split(',')
    xmin = coordinates[0]
    ymin = coordinates[1]
    xmax = coordinates[2]
    ymax = coordinates[3]

    # Transform the coordinates into lat-long coordinate system
    # x gives longitude, y gives latitude
    # Notice that
    #   + longitude runs north-south, corresponding to a vertical movement
    #   + latitude runs east-west, corresponding to a horizontal movement
    longmin, latmin = transform(inProj, outProj, xmin, ymin)
    longmax, latmax = transform(inProj, outProj, xmax, ymax)

    img_path = os.path.join(img_dir_path, name)
    # Since longitude runs vertical and latitude runs horizontal, we set
    # longitude for our y-values and latitude for our x values for image traversal.
    # These x and y values are different from the above x and y values, which are
    # coordinate values of the epsg:3857 system.
    image_splitting(img_path, img_id, (latmin, longmin, latmax, longmax))
