Test h5py with i7 + HDD
-----------------------
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

