'''
File Description

'''

from sys import argv
from os import path
import geopandas as gpd

def plot_boundary(boundary, rasterCoords, remImgCoords):
    '''

    '''
    pass

def remove_extra_images(imgCoords):
    '''

    '''
    pass

def split_images(rasterCoords):
    '''

    '''
    pass

def get_images(boundary):
    '''

    '''
    pass

def isValidInput():
    if len(argv) <= 1:
        print("Error: Not enough arguments provided!")
        return False

    shapefilePath = argv[1]
    if not path.isfile(shapefilePath):
        print("Error: Provided boundary file doesn't exist!")
        return False
    if shapefilePath.split('.')[-1] != "shp":
        print("Warning: Provided boundary file doesn't have the Shapefile extension!")
    return True

def main():
    if not isValidInput():
        return

    shapefilePath = argv[1]
    boundary = gpd.read_file(shapefilePath)
    rasterCoords = get_images(boundary)
    imgCoords = split_images(rasterCoords)
    remImgCoords = remove_extra_images(imgCoords)
    plot_boundary(boundary, rasterCoords, remImgCoords)

if __name__ == "__main__":
    main()
