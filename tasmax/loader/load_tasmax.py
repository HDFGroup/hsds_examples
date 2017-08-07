import sys
import h5pyd
import h5py
import hslogger as log

SLICE_PER_FILE = 60
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

if len(sys.argv) < 4 or sys.argv[1] in ("-h", "--help"):
    print("usage: python load_tasmax.py <input_file> <output_file> <file_number>")
    sys.exit(1)

filein = sys.argv[1]
fileout = sys.argv[2]
fileno = int(sys.argv[3])
if fileno < 1:
   print("fileno must be 1 or greater")
   sys.exit(1)

# open input for read
fin = h5py.File(filein, 'r')

# output file for append
fout = h5pyd.File(fileout, 'a')

# when the first file is loaded, the
# recreate the extensible datasets if they
# are fixed width
for dset_name in extensible_dsets:
    dset_in = fin[dset_name]
    dset_out = fout[dset_name]
    if dset_in.shape[0] != SLICE_PER_FILE:
        log.error("expected: {} slices per file but got: {}".format(SLICE_PER_FILE, dset_in.shape[0]))
        sys.exit(1)
    extent = dset_out.shape[0]
    rank = len(dset_in.shape)
    slice_start = fileno * SLICE_PER_FILE
    slice_end = slice_start + SLICE_PER_FILE
    if slice_end > extent:
        log.info("extending {} by {}".format(dset_name, slice_end - extent))
        dset_out.resize(slice_end, axis=0)
    for i in range(SLICE_PER_FILE):
        log.info("input {} -> output {}".format(i, slice_start+i))
        if rank == 3:
            data = dset_in[i, :, :]
            dset_out[slice_start + i, :, :] = data
        elif rank == 2:
            data = dset_in[i, :]
            dset_out[slice_start + i, :] = data
        elif rank == 1:
            data = dset_in[i]
            dset_out[slice_start + i] = data
        else:
            log.error("Unsupported rank: {}".format(rank))
            sys.exit(1)



log.info("{} done".format(fileout))

fin.close()
fout.close()