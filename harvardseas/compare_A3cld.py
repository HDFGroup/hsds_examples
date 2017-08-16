import sys
import numpy as np
import h5pyd

# compare data in compressed vs. uncompress versions of A3cld.Native.nc

# uncompressed and compressed file
f_raw = h5pyd.File("/home/harvardseas/GEOSFP/GEOSFP.20150701.A3cld.Native.nc", 'r')
f_com = h5pyd.File("/home/harvardseas/GEOSFP/GEOSFP.20150701.A3cld.NativeZ.nc", 'r')

# compare metadata
# check variable names
for names in zip(f_com, f_raw):
    print(names)
    if names[0] != names[1]:
        sys.exit("name mismatch: {} vs. {}".format(names[0], names[1]))

# get a variable
dset_raw = f_raw['CLOUD']
dset_com = f_com['CLOUD']

# check basic properties
if dset_raw.shape != dset_com.shape:
    sys.exit("dataset shapes don't match")
if dset_raw.chunks != dset_com.chunks:
    sys.exit("dataset chunks don't match")

if dset_raw.dtype != dset_com.dtype:
    sys.exit("dataset types don't match")

for i in range(dset_raw.shape[0]):
    for j in range(dset_raw.shape[1]):
        print("get uncompressed data[{},{},:,:] for CLOUD".format(i,j))
        data_raw = dset_raw[i,j,:,:]
        print("get compressed data[{},{},:,:] for CLOUD".format(i,j))
        data_com = dset_com[i,j,:,:]
        if not np.allclose(data_raw, data_com):
            sys.exit("dataset data doesn't match")



