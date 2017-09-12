#!/usr/bin/env python
import os
import sys
import optparse
import numpy as np
import PIL
from PIL import *
from osgeo import gdal,ogr,osr	#Geospatial Data Abstraction Library
gdal.UseExceptions()
osgeo.ogr.UseExceptions()

g_red = gdal.Open( 'LC81390442014343LGN00_B4.TIF' )
#print g_red.GetMetadata()	#this will give raster metadata type
red = g_red.ReadAsArray()
g_nir = gdal.Open('LC81390442014343LGN00_B5.TIF')
#print g_nir.GetMetadata()
nir = g_nir.ReadAsArray()
red = np.array(red, dtype = float)
nir = np.array(nir, dtype = float)
check = np.logical_and ( red > 1, nir > 1 )
ndvi = np.where ( check,  (nir - red ) / ( nir + red ), -999 )
geo = g_red.GetGeoTransform()
proj = g_red.GetProjection()
shape = red.shape
driver = gdal.GetDriverByName("GTiff")
outFile = driver.Create( "ndvi.tif", shape[1], shape[0], 1, gdal.GDT_Float32)
outFile.SetGeoTransform( geo )
outFile.SetProjection( proj )
outFile.GetRasterBand(1).WriteArray(ndvi)
outFile = None
