import sys
import numpy as np
import logging
import h5pyd

loglevel = logging.DEBUG
logging.basicConfig(format='%(asctime)s %(message)s', level=loglevel)
cube_side = 256

if len(sys.argv) > 1:
    if sys.argv[1] in ("-h", "--help"):
        print("Usage: python writecube.py [cube_side]")
        sys.exit(-1)
    else:
        cube_side = int(sys.argv[1])

filename = "/home/john/cubes/"
filename += "cube_" + str(cube_side) + ".h5"

print("creating domain:", filename)
f = h5pyd.File(filename, "w") 

print("filename,", f.filename)

print("create dataset")

dset = f.create_dataset('dset', (cube_side, cube_side, cube_side), dtype='f8')

print("name:", dset.name)
print("shape:", dset.shape)
print("dset.type:", dset.dtype)

print("writing data...")

for i in range(cube_side):
    arr = np.random.rand(cube_side, cube_side)
    dset[i,:,:] = arr
print("done!")

f.close()
