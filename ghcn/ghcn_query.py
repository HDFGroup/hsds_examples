import logging
import h5pyd as h5py

#
# Query the GHCN weather station dataset and fetch all the rows 
# using the given station id.
#
def main():
    loglevel = logging.DEBUG  # Use logging.ERROR to hide log messages
    logging.basicConfig(format='%(asctime)s %(message)s', level=loglevel)
    filepath = "/home/hdf/sample/ghcn.h5"  # 82 GB  
    station_id = "US1WAKG0020"  # seattle station
    f = h5py.File(filepath, 'r')
    dset = f["/dset"]
    print("nrows:", dset.shape[0])
    query = "station == b'{}'".format(station_id)
    result = dset.read_where(query)
    print("result: {} rows".format(len(result)))
    f.close()
    
main()
