import sys
import numpy as np


USE_H5PY = False
slice_number = 0
argn = 1
while argn < len(sys.argv):
    arg = sys.argv[argn]
    if arg in ("-h", "--help"):
        print("usage: python read_region.py [slice] [use_h5py]")
        sys.exit(-1)
    if arg == "use_h5py":
        USE_H5PY = True
        print("using h5py")
        argn += 1
    else:
        slice_number = int(arg)
        print("slice: {}".format(slice_number))
        argn += 1

if USE_H5PY:
    import h5py
    folder = "/home/john/HDF/data/NEX/"
else:
    import h5pyd as h5py
    folder = "/home/john/NEX/"
    
    
filename = folder + "tasmax_amon_BCSD_historical_r1i1p1_CONUS_CSIRO-Mk3-6-0_199001-199412.nc"

f = h5py.File(filename, 'r')
dset = f["/tasmax"]
print("tasmax shape: {}".format(dset.shape))
if slice_number < 0 or slice_number >= dset.shape[0]:
    print("slice value out of range")
    sys.exit(-1)
print("tasmax chunk layout: {}".format(dset.chunks))
num_bytes = dset.shape[1] * dset.shape[2] * dset.dtype.itemsize
print("selection: [{},:,:]".format(slice_number))
print("reading {} bytes".format(num_bytes))
data = dset[slice_number,:,:]
print("done!")
print("min: {}".format(np.min(data)))
print("max: {}".format(np.max(data)))

f.close()
