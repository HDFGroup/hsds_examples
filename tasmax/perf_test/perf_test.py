import sys
from random import randint
import h5py
import numpy as np

#
# tasmax dataset shape: (60, 3105, 7025)
#                chunk: (1, 369, 836)
#                type:  float32
#
def test_region(dset):
    num_slices = 50
    y_width = dset.chunks[1]
    x_width = dset.chunks[2]
    print("test_region slice [n,:{},:{}]".format(y_width, x_width))       
    for i in range(num_slices):
        nslice = randint(0, 59)
        data = dset[nslice, :y_width, :x_width]
        if len(data) != y_width:
            sys.exit("unexpected shape returned")
    print("test_region done")

def test_series(dset):
    print("test_series")
    num_slices = 25
    for i in range(num_slices):
        y = randint(0, dset.shape[1]-1)
        x = randint(0, dset.shape[2]-1)  
        data = dset[:60, y, x]  
        if len(data) != 60:
            sys.exit("unexpected shape returned")
    print("test_series done")

          

#
# main
#
filename = "/Volumes/data/NEX/tasmax_ens-avg_amon_historical_CONUS_195001-195412.nc"
f = h5py.File(filename, 'r')
tasmax = f['tasmax']
test_region(tasmax)
test_series(tasmax)
f.close()
	


