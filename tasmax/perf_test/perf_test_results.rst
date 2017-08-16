tasmax dataset
==============

Uncompressed
------------

::

    tasmax                   Dataset {600/Inf, 3105/3105, 7025/7025}
    UUID: d-b340ac50-7afb-11e7-8817-0242ac110008
    Chunks: [1, 369, 836] 1,233,936 bytes, 48,600 allocated chunks
    Storage: 52,350,300,000 logical bytes, 59,969,289,600 allocated bytes, 87.30% utilization
    Type:: float32

Compressed
----------

::

    tasmax                   Dataset {420/Inf, 3105/3105, 7025/7025}
    UUID: d-102c88c2-7f01-11e7-9343-0242ac110008
    Chunks: [1, 369, 836] 1,233,936 bytes, 28,334 allocated chunks
    Storage: 36,645,210,000 logical bytes, 10,733,686,344 allocated bytes, 341.40% utilization
    Type:: float32





Test h5py with i7 + HDD
-----------------------

::
    $ time python perf_test.py
    test_region slice [n,:369,:836]
    test_region done
    test_series
    test_series done

    real	0m4.472s
    user	0m4.377s
    sys	0m0.098s

Test h5py with i7 + SSD
-----------------------

::
  
    $ time python perf_test.py
    test_region slice [n,:369,:836]
    test_region done
    test_series
    test_series done

    real	0m4.692s
    user	0m4.585s
    sys	0m0.111s

Test h5pyd with m2.2xlarge & 4 nodes - No compression
-----------------------------------------------------

::

    $ time python perf_test2.py
    test_region slice [n,:369,:836]
    test_region done
    test_series
    test_series done

    real	0m19.325s
    user	0m1.123s
    sys	0m0.803s

Test h5pyd with m2.2xlarge & 4 nodes - With compression
-----------------------------------------------------

Cold:

::

    $ time python perf_test2.py
    test_region slice [n,:369,:836]
    test_region done
    test_series
    test_series done

    real	0m37.857s
    user	0m1.144s
    sys	0m0.788s

Hot:

     time python perf_test2.py
    test_region slice [n,:369,:836]
    test_region done
    test_series
    test_series done

    real	0m23.170s
    user	0m1.153s
    sys	0m0.665s

