FILE_PATH=${1:-hdf5://home/test_user1/test/streamtest.h5}
python ../siggen.py --filepath ${FILE_PATH} --name sensor3 --scale 200 --freq 100 --update 1 --units m --minval 40.0 --maxval 200.0 --quiet y 
