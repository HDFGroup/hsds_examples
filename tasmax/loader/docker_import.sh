#!/bin/sh
CLIENT_RAM=1g
CLIENT_NUMBER=1
docker run --name hs_import_1 \
   --memory=${CLIENT_RAM} \
   -v ${HOME}/.hscfg:/root/.hscfg \
   -v /data:/data \
   -v ${PWD}:/usr/local/src/loader  \
   --env CLIENT_NUMBER=${CLIENT_NUMBER} \
   --env HS_ENDPOINT="http://hsds_sn_1" \
   --link hsds_sn_1:hsds_sn_1 \
   hdfgroup/h5pyd /usr/local/src/loader/docker_run.sh 

# To run multiple clients in parallel, change client number
# to number of desired clients and run contains commented section below
#docker run -d --name hs_import_2 \
#   --memory=${CLIENT_RAM} \
#   -v ${HOME}/.hscfg:/root/.hscfg \
#   -v /data:/data \
#   -v ${PWD}:/usr/local/src/loader  \
#   --env CLIENT_NUMBER=2 \
#   --env HS_ENDPOINT="http://hsds_sn_2:5102" \
#   --link hsds_sn_2:hsds_sn_2 \
#   hdfgroup/h5pyd /usr/local/src/loader/docker_run.sh 
