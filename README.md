GBDX task to materialize Dynamic data that comes out of Digitalglobe's super awesome FLAME (flexible large area mosaic engine)

gbdxtools example usage:

```python
from gbdxtools import Interface
gbdx = Interface()

dynamic = gbdx.Task('dynamic_materializer')

# Required inputs:
dynamic.inputs.project_name = 'DYNAMIC-Australia-Q32017'
dynamic.inputs.aoi_geojson = '{"type":"FeatureCollection","features":[{"type":"Feature","properties":{},"geometry":{"type":"Polygon","coordinates":[[[153.42390060424805,-28.00989892967722],[153.43647480010986,-28.00989892967722],[153.43647480010986,-27.999933788434422],[153.42390060424805,-27.999933788434422],[153.42390060424805,-28.00989892967722]]]}}]}'

# Optional inputs:
dynamic.inputs.version = '1' # default will be latest version
dynamic.inputs.output_filename = 'mynicefile.tif' # default is dynamic.tif

wf = gbdx.Workflow([dynamic])
wf.savedata(dynamic.outputs.data, 'my_output_location')
wf.execute()

```