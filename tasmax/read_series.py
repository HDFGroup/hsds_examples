import sys
import numpy as np


USE_H5PY = False
x_index = -1
y_index = -1
argn = 1
while argn < len(sys.argv):
    arg = sys.argv[argn]
    if arg in ("-h", "--help"):
        print("usage: python read_series.py [x] [y] [use_h5py]")
        sys.exit(-1)
    if arg == "use_h5py":
        USE_H5PY = True
        argn += 1
    else:
        index = int(arg)
        if x_index < 0:
            x_index = index
        else:
            y_index = index
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

if x_index < 0:
    x_index = dset.shape[1] // 2
elif x_index >= dset.shape[1]:
    print("x index out of range")
    sys.exit(-1)
if y_index < 0:
    y_index = dset.shape[2] // 2
elif y_index >= dset.shape[2]:
    print("y index out of range")
    sys.exit(-1)

print("tasmax chunk layout: {}".format(dset.chunks))
num_bytes = dset.shape[0] * dset.dtype.itemsize
print("selection: [:,{},{}]".format(x_index, y_index))
print("reading {} bytes".format(num_bytes))
data = dset[:,x_index,y_index]
print("done!")
print("min: {}".format(np.min(data)))
print("max: {}".format(np.max(data)))

f.close()
