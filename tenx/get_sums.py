import h5pyd as h5py
import numpy as np

BATCH_SIZE=1000
f = h5py.File("/home/hdf/tenx_full.h5", "r")
g = h5py.File("/home/hdf/tenx_count.h5", "w")

dset_in = f['newassay001']
neuron_cnt = dset_in.shape[0]
gene_cnt = dset_in.shape[1]
dset_out = g.create_dataset("newassay001_counts", (neuron_cnt,), dtype=np.uint32)
print("neurons: {} genes: {}".format(neuron_cnt, gene_cnt))
start = 0
while start < neuron_cnt:
    stop = start + BATCH_SIZE
    if stop > neuron_cnt:
        stop = neuron_cnt
    batch_count = stop - start
    count_arr = np.zeros((batch_count,), dtype=np.uint32)
    for i in range(batch_count):
        arr = dset_in[start+i, :]
        count_arr[i] = arr.sum()
        print("i: {} sum: {}".format(i, count_arr[i]))
    dset_out[start:stop] = count_arr

f.close()
g.close()

