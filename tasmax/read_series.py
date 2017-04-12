import numpy as np

USE_H5PY = False
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
x = dset.shape[1] // 2
y = dset.shape[2] // 2
print("tasmax chunk layout: {}".format(dset.chunks))
num_bytes = dset.shape[0] * dset.dtype.itemsize
print("selection: [:,{},{}]".format(x, y))
print("reading {} bytes".format(num_bytes))
data = dset[0,:,:]
print("done!")
print("min: {}".format(np.min(data)))
print("max: {}".format(np.max(data)))

f.close()
