'''
File Description

'''

from sys import argv
from os import path
import geopandas as gpd

def plot_boundary(boundaryList, rasterCoords, remImgCoords):
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

def get_images(boundaryList):
    '''

    '''
    pass

def extract_geometries(boundaryDF):
    ''' Generate a list of geometries for specified entries in a DataFrame.

    Extract the desired entries from the boundary DataFrame, then combine their
    geometries together into a list.

    Args:
        boundaryDF: A DataFrame object obtained by reading a Shapefile using
        Geopandas.

    Returns:
        boundaryList: A list of geometry objects for entries specified in the
        command arguments that exist in the DataFrame (or for all entries if no
        argument was specified).
    '''

    boundaryList = []
    if len(boundaryDF) == 1:
        boundaryList.append(boundaryDF["geometry"][0])
    elif len(argv) == 2:
        print("Warning: No entry specification. Program will extract images for all geometries in the Shapefile!")
        for i in range(len(boundaryDF)):
            boundaryList.append(boundaryDF["geometry"][i])
    else:
        for i in range(2, len(argv)):
            entryIdx = int(argv[i])
            if entryIdx >= len(boundaryDF):
                print(f"Warning: Entry {entryIdx} is skipped due to being outside the range of the boundary DataFrame!")
            else:
                boundaryList.append(boundaryDF["geometry"][entryIdx])
    return boundaryList

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
    boundaryDF = gpd.read_file(shapefilePath)
    # Change the boundary's coordinate system to the WGS84 system
    # so we can work with latitudianland longitudinal values.
    # The EPSG value for WGS84 is 4326.
    boundaryDF = boundaryDF.to_crs(epsg=4326)
    boundaryList = extract_geometries(boundaryDF)
    rasterCoords = get_images(boundaryList)
    imgCoords = split_images(rasterCoords)
    remImgCoords = remove_extra_images(imgCoords)
    plot_boundary(boundaryList, rasterCoords, remImgCoords)

if __name__ == "__main__":
    main()
