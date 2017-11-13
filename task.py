import json
from dynamic import materialize_tif, get_latest_version
outdir = '/mnt/work/output/'
indir = '/mnt/work/input/'

input_data = json.load(open('/mnt/work/input/ports.json'))

# required params (will raise Exception if not there)
aoi_geojson = input_data['aoi_geojson']
project_name = input_data['project_name']

# optional params
output_filename = input_data.get('output_filename', 'dynamic.tif')
output_filename = '/mnt/work/output/data/' + output_filename
version = input_data.get('version')

if not version:
	version = get_latest_version(project_name)

materialize_tif(project_name, version, aoi_geojson, output_filename)