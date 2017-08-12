#!/bin/sh
CLIENT_RAM=1g
docker run -d --name hs_import_1 \
   --memory=${CLIENT_RAM} \
   -v ${HOME}/.hscfg:/root/.hscfg \
   -v ${PWD}:/usr/local/src/loader  \
   hdfgroup/h5pyd /usr/local/src/loader/docker_run.sh 

