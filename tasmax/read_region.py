import sys
import numpy as np
import logging


USE_H5PY = False
slice_number = None
step_number = None
argn = 1
while argn < len(sys.argv):
    arg = sys.argv[argn]
    if arg in ("-h", "--help"):
        print("usage: python read_region.py [slice] [step] [use_h5py]")
        sys.exit(-1)
    if arg == "use_h5py":
        USE_H5PY = True
        print("using h5py")
        argn += 1
    elif slice_number is None:
        slice_number = int(arg)
        print("slice: {}".format(slice_number))
        argn += 1
    elif step_number is None:
        step_number = int(arg)
        print("step: {}".format(step_number))
        argn += 1

if USE_H5PY:
    import h5py
    folder = "/home/john/HDF/data/NEX/"
else:
    import h5pyd as h5py
    folder = "/home/john/NEX/"

if slice_number is None:
    slice_number = 0
if step_number is None:
    step_number = 1
    
loglevel = logging.ERROR
logfname=None
logging.basicConfig(filename=logfname, format='%(asctime)s %(message)s', level=loglevel)
logging.debug("set log_level to {}".format(loglevel))

# This is a larger dataset
#filename = folder + "tasmax_amon_BCSD_historical_r1i1p1_CONUS_CSIRO-Mk3-6-0_199001-199412.nc"
filename = folder + "tasmax_day_BCSD_rcp45_r1i1p1_CanESM2_2050.nc"
f = h5py.File(filename, 'r')
dset = f["/tasmax"]
print("tasmax shape: {}".format(dset.shape))
if slice_number < 0 or slice_number >= dset.shape[0]:
    print("slice value out of range")
    sys.exit(-1)
print("tasmax chunk layout: {}".format(dset.chunks))

if step_number == 1:
    num_bytes = dset.shape[1] * dset.shape[2] * dset.dtype.itemsize
    print("reading {} bytes".format(num_bytes))
    print("selection: [{},::,::]".format(slice_number))
    data = dset[slice_number,:,:]
else:
    num_rows = dset.shape[1] // step_number
    num_cols = dset.shape[2] // step_number
    num_bytes = num_rows * num_cols * dset.dtype.itemsize
    print("selection: [{},::{},::{}]".format(slice_number, step_number, step_number))
    data = dset[slice_number,::step_number,::step_number]
print("done!")
print("min: {}".format(np.min(data)))
print("max: {}".format(np.max(data)))

f.close()
