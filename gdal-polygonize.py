from gc import callbacks
import os
from osgeo import gdal, ogr,osr
import sys
from alive_progress import alive_bar

gdal.UseExceptions()  # This Allows GDAL to Throw python exceptions

#
# Get Raster DataSources
#

# Directory where file is
tif = str(os.path.expanduser(
    '~') + "/Área de Trabalho/MapBiomas/1985/brasil_collection-6_lclu_coverage_brasil_coverage_1985.tif")

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

spatial_ref=osr.SpatialReference()
spatial_ref.SetFromUserInput('EPSG:4326')


tif_Layername = 'brasil_collection-6_lclu_coverage_brasil_coverage_1985'
DriveSearch = ogr.GetDriverByName('GPKG')

NewNameFile = DriveSearch.CreateDataSource(tif_Layername + '.gpkg')
tif_layer = NewNameFile.CreateLayer(tif_Layername, srs=None )

field = ogr.FieldDefn('Color_Gradient', ogr.OFTInteger)
tif_layer.CreateField(field)
tif_field=tif_layer.GetLayerDefn().GetFieldIndex("class")
with alive_bar as progressbar:
    gdal.Polygonize(srcband, None, tif_layer, tif_field , [], callback=None)

#close .tif
tifFile = None