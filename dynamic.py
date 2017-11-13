#!/usr/bin/env python
import json

import boto3
import botocore
from osgeo import gdal
from shapely import geometry, ops
from tiletanic import tilecover, tileschemes

def get_latest_version(project_name):
    bucket_name, prefix = 'flame-projects', project_name + '/'
    client = boto3.client('s3')
    bucket_name, prefix = 'flame-projects', project_name + '/'
    result = client.list_objects(Bucket=bucket, Prefix=prefix, Delimiter='/')
    versions = [o.get('Prefix').split('/')[-2] for o in result.get('CommonPrefixes')]
    versions.reverse()
    return versions[0]  

def materialize_tif(project_name, version, aoi_geojson, output_filename = 'dynamic.tif'):

    gdal.SetConfigOption('GDAL_DISABLE_READDIR_ON_OPEN', 'TRUE')
    gdal.SetConfigOption('VSI_CACHE', 'TRUE')
    # gdal.SetConfigOption('CPL_CURL_VERBOSE', 'YES') # see the http calls
    gdal.SetConfigOption('CPL_VSIL_CURL_ALLOWED_EXTENSIONS', 'TIF')
    
    # a box in australia:
    #aoi_geojson = '{"type":"FeatureCollection","features":[{"type":"Feature","properties":{},"geometry":{"type":"Polygon","coordinates":[[[153.42390060424805,-28.00989892967722],[153.43647480010986,-28.00989892967722],[153.43647480010986,-27.999933788434422],[153.42390060424805,-27.999933788434422],[153.42390060424805,-28.00989892967722]]]}}]}'
    aoi = ops.unary_union([geometry.shape(f['geometry']) for f in json.loads(aoi_geojson)['features']])

    #project_name = 'DYNAMIC-Australia-Q32017/1'
    
    bucket_name, prefix = 'flame-projects', project_name + '/' + version + '/raster_tiles/'

    s3 = boto3.resource('s3')
    tiler = tileschemes.DGTiling()
    paths = []
    for key in (prefix + tiler.quadkey(tile) + '.tif' for tile in tilecover.cover_geometry(tiler, aoi, 12)):

        # Check if tif exists.
        try:
            s3.Object(bucket_name=bucket_name, key=key).load()
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                continue
            else:
                raise

        paths.append('/vsis3/{}/{}'.format(bucket_name, key))

    # Build an inmem vrt and translate.
    try:
        ds = gdal.BuildVRT('/vsimem/combo.vrt', paths, outputBounds=aoi.bounds)
        ds_out = gdal.Translate(output_filename, ds)
    finally:
        ds_out = None
        ds = None