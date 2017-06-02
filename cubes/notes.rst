cube data generator
------------------

Provide an integer argument to the script to generate a HDF5 containing a nxnxn dataset initialized with random data.

Example: 

::

	$ h5ls -r -v cube_256_256_256.h5
	Opened "cube_256_256_256.h5" with sec2 driver.
	/                        Group
    	Location:  1:96
    	Links:     1
	/dset                    Dataset {256/256, 256/256, 256/256}
    	Location:  1:800
    	Links:     1
    	Storage:   67108864 logical bytes, 67108864 allocated bytes, 100.00% utilization
    	Type:      native float
