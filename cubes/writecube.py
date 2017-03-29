cube_side = 256

if len(sys.argv) > 1:
    cube_side = int(sys.argv[1])

#filename = "/home/john/load_test/"
filename = "cube_"
filename += str(cube_side) + "_" + str(cube_side) + "_" + str(cube_side) + ".h5"

f = h5pyd.File(filename, "w") 

print("filename,", f.filename)

print("create dataset")

dset = f.create_dataset('dset', (cube_side, cube_side, cube_side), dtype='f4')

print("name:", dset.name)
print("shape:", dset.shape)
print("dset.type:", dset.dtype)
print("dset.maxshape:", dset.maxshape)

print("writing data...")

for i in range(cube_side):
    arr = np.random.rand(cube_side, cube_side)
    dset[i,:,:] = arr
print("done!")

f.close()
