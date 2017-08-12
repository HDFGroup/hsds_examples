#! /bin/bash
URL_PREFIX="http://s3-us-west-2.amazonaws.com/nasanex/NEX-DCP30/NEX-quartile/historical/mon/atmos/tasmax/r1i1p1/v1.0/CONUS"
FILE_0="tasmax_ens-avg_amon_historical_CONUS_195001-195412.nc"
FILES=( \
"tasmax_ens-avg_amon_historical_CONUS_195501-195912.nc" \
"tasmax_ens-avg_amon_historical_CONUS_196001-196412.nc" \
"tasmax_ens-avg_amon_historical_CONUS_196501-196912.nc" \
"tasmax_ens-avg_amon_historical_CONUS_197001-197412.nc" \
"tasmax_ens-avg_amon_historical_CONUS_197501-197912.nc" \
"tasmax_ens-avg_amon_historical_CONUS_198001-198412.nc" \
"tasmax_ens-avg_amon_historical_CONUS_198501-198912.nc" \
"tasmax_ens-avg_amon_historical_CONUS_199001-199412.nc" \
"tasmax_ens-avg_amon_historical_CONUS_199501-199912.nc" \
"tasmax_ens-avg_amon_historical_CONUS_200001-200412.nc" \
"tasmax_ens-avg_amon_historical_CONUS_200501-200512.nc" \
)
DOMAIN="tasmax_ens-avg_amon_historical_CONUSz.nc"
cd /usr/local/src/loader
echo "cwd:" `pwd`
if [ -e ${URL_PREFIX}/${FILE_0} ]; then
   echo "${FILE_0} already downloaded"
else
   echo "getting first file"
   wget -q ${URL_PREFIX}/${FILE_0}
fi
echo "hsload:" ${FILE_0}
hsload -v ${FILE_0} /nex/${DOMAIN}
return_value=$?
if [ $return_value != 0 ]; then
     echo "Command hsload failed"
     exit -1
fi
rm ${FILE_0}
FILE_NUMBER=0
for tasmax_file in "${FILES[@]}"
do
     FILE_NUMBER=$((FILE_NUMBER+1))
     echo "getting file ${FILE_NUMBER}: "${tasmax_file}
     wget -q ${URL_PREFIX}/${tasmax_file}
     python load_tasmax.py ${tasmax_file} /nex/${DOMAIN} ${FILE_NUMBER}
     rm ${tasmax_file}
done
echo "done!"