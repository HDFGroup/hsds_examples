import sys
import h5py as h5py
import numpy as np
import hslogger as log

LAT_EXTENT = 1602
X_EXTENT = 2976

# these all have dimensions: inf x Y_EXTENT x X_EXTENT
 
"""
bnds                     Dataset {2}
lat                      Dataset {3105}
lat_bnds                 Dataset {3105, 2}
lon                      Dataset {7025}
lon_bnds                 Dataset {7025, 2}
tasmax                   Dataset {60/Inf, 3105, 7025}
time                     Dataset {60/Inf}
time_bnds                Dataset {60/Inf, 2}
"""

# these all datasets  will be concatenated to for 
# each import file
extensible_dsets = ('tasmax', 'time', 'time_bnds')  

 
# chunk layout for tasmax dataset
chunk_layout = [4, 621, 281]   # 2.5MB / chunk

if len(sys.argv) < 3 or sys.argv[1] in ("-h", "--help"):
    print("usage: python load_tasmax.py <input_file> <output_file>")
    sys.exit(1)

filein = sys.argv[1]
fileout = sys.argv[2]

# open input for read
fin = h5py.File(filein, 'r')

# output file for append
fout = h5py.File(fileout, 'a')

# when the first file is loaded, the
# recreate the extensible datasets if they
# are fixed width
for dset_name in extensible_dsets:
    dset_in = fin[dset_name]
    dset_out = fout[dset_name]
    extend = dset_in.shape[0]
    dsize = dset_out.shape[0]
    rank = len(dset_in.shape)
    log.info("extending {} by {}".format(dset_name, extend))
    dset_out.resize(dsize + extend, axis=0)
    for i in range(extend):
        log.info("input {} -> output {}".format(i, dsize+i))
        if rank == 3:
            data = dset_in[i, :, :]
            dset_out[dsize + i, :, :] = data
        elif rank == 2:
            data = dset_in[i, :]
            dset_out[dsize + i, :] = data
        elif rank == 1:
            data = dset_in[i]
            dset_out[dsize + i] = data
        else:
            log.error("Unsuppoerted rank: {}".format(rank))
            sys.exit(1)

 

log.info("{} done".format(fileout))
         
fin.close()
fout.close()


