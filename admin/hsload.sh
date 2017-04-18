#!/bin/bash
if [ $# -eq 0 ] || [ $1 == "-h" ]; then
   echo "Usage hsload.sh <data_file>"
   echo "<data_file> must be in ~/data directory"
   exit 1
fi
docker run --name hsload -d --env HS_ENDPOINT="http://hsds_sn_1:5101" --link hsds_sn_1:hsds_sn_1 -v ${HOME}/.hscfg:/root/.hscfg -v ${HOME}/data/:/data hdfgroup/h5pyd python hsload.py -v /data/$1 /home/john/NEX/$1
