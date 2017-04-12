import h5pyd as h5py
import numpy as np
import sys


def main():
    filepath = "/home/john/sample/ghcn.h5"  # 82 GB  
    station_id = "US1WAKG0020"  # seattle station
    f = h5py.File(filepath, 'r')
    dset = f["/dset"]
    print("nrows:", dset.shape[0])
    query = "station == b'{}'".format(station_id)
    result = dset.read_where(query)
    print("result: {} rows".format(len(result)))
    f.close()
    
main()
