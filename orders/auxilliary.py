from re import search

def format_pointstr_from_osmwidget(osm_output):
   srid = 3857

   pattern = '([0-9.]+,[0-9.]+)'

   c = search(pattern, osm_output).group(0).split(sep=',')

   coord = {
            'srid': srid,
            'lat': c[0],
            'lon': c[1]
           }
   pointstr = "SRID={srid};POINT({lat} {lon})".format(**coord)

   return pointstr
