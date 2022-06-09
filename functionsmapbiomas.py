"""

Funçẽs usadas no programa MapBiomas_Downloader 


"""
import errno
import os
from osgeo import gdal, ogr, osr
import sys
import multiprocessing as mp


def CreateDir():
    try:
        mylocal = str(os.path.expanduser('~'))
        directory = "MapBiomas"
        path = os.path.join(mylocal, directory)
        os.mkdir(path)
    except OSError as err:
        if err.errno == errno.EEXIST:
            print("Directory Alredy exist")
        return path
    return path


def Polygonized(path, name_file, directory):
    """
    Poligonizar shapefiles

    args:
        path - path of archive .tif
        name_file - layername of polygonized object 
        directory - path of 'place' dpkg will save 
    """

    gdal.UseExceptions()  # This Allows GDAL to Throw python exceptions

    #
    # Get Raster DataSources
    #

    # Directory where file is
    tif = path

    # open tif and info
    tifFile = gdal.Open(tif)
    print(tifFile.GetMetadata())

    # get raster band
    try:
        band_num = 1
        srcband = tifFile.GetRasterBand(band_num)

    except RuntimeError as err:
        print("Band ( %i ) not found " % band_num)
        print(err)
        sys.exit("Exit")

    #
    # Create Output DataSource
    #

    spatial_ref = osr.SpatialReference()
    spatial_ref.SetFromUserInput('EPSG:4326')

    os.chdir(directory)

    tif_Layername = name_file
    DriveSearch = ogr.GetDriverByName('GPKG')
    NewNameFile = DriveSearch.CreateDataSource(tif_Layername + '.gpkg')
    tif_layer = NewNameFile.CreateLayer(tif_Layername, srs=None)
    field = ogr.FieldDefn('class', ogr.OFTInteger)
    tif_layer.CreateField(field)
    tif_field = tif_layer.GetLayerDefn().GetFieldIndex("class")


    gdal.Polygonize(srcband, None, tif_layer, tif_field, [], callback=None)

    #close .tif
    tifFile = None
