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
start = None
count = None
use_h5py = False
argn = 1

while argn < len(sys.argv):
    arg = sys.argv[argn]
    if arg in ("-h", "--help"):
        print("Usage: python readrows.py symbol [start] [count] [filename] [use5py] ")
        sys.exit()
    if start is None:
        start = int(arg)
    elif count is None:
        count = int(arg)  
    elif filename is None:
        filename = arg     
    elif arg == "useh5py":
        use_h5py = True        
    else:
        print("unexpected argument")
        sys.exit(-1)
    argn += 1

if start is None:
    start = 0
if count is None:
    count = 100

if filename is None:
    filename = "/home/hdf/snp500.h5"
 
if use_h5py:    
    print("opening:",filename, "with h5py")
    f = h5py.File(filename, 'r')
else:
    print("opening:",filename, "with h5pyd")
    f = h5pyd.File(filename, 'r')
 

print("root uuid:", f.id.id)

dset = f['/dset']
print("name:", dset.name)
print("shape:", dset.shape)
if start+count > dset.shape[0]:
    print("selection area out range")
else:

    rows = dset[start:(start+count)]

    for i in range(len(rows)):
        row = rows[i]
        print("{}: {}".format(i, row))    
 
f.close()

