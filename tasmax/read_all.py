import sys
import numpy as np


USE_H5PY = False
argn = 1
while argn < len(sys.argv):
    arg = sys.argv[argn]
    if arg in ("-h", "--help"):
        print("usage: python read_all.py [use_h5py]")
        sys.exit(-1)
    if arg == "use_h5py":
        USE_H5PY = True
        print("using h5py")
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
print("tasmax chunk layout: {}".format(dset.chunks))
num_bytes = dset.shape[1] * dset.shape[2] * dset.dtype.itemsize
print("reading {} bytes per slice".format(num_bytes))
for slice_number in range(dset.shape[0]):
    print("selection: [{},:,:]".format(slice_number))
    data = dset[slice_number,:,:]
    print("min: {}".format(np.min(data)))
    print("max: {}".format(np.max(data)))
print("done!")

f.close()
