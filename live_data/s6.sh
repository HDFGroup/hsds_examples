FILE_PATH=${1:-hdf5://home/test_user1/test/streamtest.h5}
python siggen.py --filepath ${FILE_PATH} --name sensor6 --scale 600 --freq 100 --update 1 --units m --minval -100.0 --maxval 100.0 --quiet y 
