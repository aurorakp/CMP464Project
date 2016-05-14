

import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

m = Basemap(projection='tmerc',width=55000,height=55000,lon_0=-74.0059,lat_0=40.7127,resolution='h')
m.drawcounties()
