##############################################################################
# Copyright by The HDF Group.                                                #
# All rights reserved.                                                       #
#                                                                            #
# This file is part of H5Serv (HDF5 REST Server) Service, Libraries and      #
# Utilities.  The full HDF5 REST Server copyright notice, including          #
# terms governing use, modification, and redistribution, is contained in     #
# the file COPYING, which can be found at the root of the source code        #
# distribution tree.  If you do not have access to this file, you may        #
# request a copy from help@hdfgroup.org.                                     #
##############################################################################
import sys
import h5pyd
import h5py
import numpy as np

filename = None  
symbol = None
argn = 1
use_h5py = False

while argn < len(sys.argv):
    arg = sys.argv[argn]
    if arg in ("-h", "--help"):
        print("Usage: python querysnp500.py symbol [filename] [use5py]")
        sys.exit()
    if symbol is None:
        symbol = arg
    elif filename is None:
        filename = arg       
    elif arg == "useh5py":
        use_h5py = True        
    else:
        print("unexpected argument")
        sys.exit(-1)
    argn += 1

if symbol is None:
    symbol = 'AAPL'
print("symbol:", symbol)

if filename is None:
    filename = "/home/john/sample/snp500.h5"
 
if use_h5py:    
    print("opening:",filename, "with h5py")
    f = h5py.File(filename, 'r')
else:
    print("opening:",filename, "with h5pyd")
    f = h5pyd.File(filename, 'r')
 

print("uuid:", f.id.id)

dset = f['/dset']
print("name:", dset.name)
print("shape:", dset.shape)

result = None

if use_h5py:
    # no where clause, so just go through all the dataset elements
    PAGE_SIZE = 1024
    extent = dset.shape[0]
    start = 0
    rows = []
    while start < extent:
        stop = start + PAGE_SIZE
        if stop > extent:
            stop = extent
        #print("read [{}:{}]".format(start, stop))
        arr = dset[start:stop]
        bSymbol = symbol.encode('utf-8')  # value is stored as bytes
        for i in range(stop-start):
            row = arr[i]
            if row['symbol'] == bSymbol:
                rows.append(tuple(row))
        start += PAGE_SIZE  # go on to next page
    result = np.asarray(rows, dtype=dset.dtype)
else:

    query = "symbol == b'" + symbol + "'"
    print("query:", query)
    result = dset.read_where(query)
    
num_rows = result.shape[0]
print("got:", num_rows, "rows")
if num_rows > 0:
    nparr_open = result["open"]
    print("min/max/stddev:", nparr_open.min(), nparr_open.max(), nparr_open.std())
for i in range(num_rows):
    print(result[i])

f.close()

