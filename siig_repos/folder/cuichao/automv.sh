#!/bin/sh

# Get current day
MDY=`date +%m%d%y`
H=`date +%H`

FILENAME='alarm_rec4.'${MDY}

MAX_SIZE=2140000000
#MAX_SIZE=10

FILE_EXIT=`ls ${FILENAME} || echo "0"`

if [ ${FILE_EXIT} = "0" ]
then
#   echo "FILE NOT AVALIABLE"
   exit
fi

CUR_SIZE=`ls -l ${FILENAME} | awk '{print $5}'`

if [ ${CUR_SIZE} -ge ${MAX_SIZE} ]
then
  mv ${FILENAME} ${FILENAME}${H}
#else
#  echo "NOT NEED TO MV"
fi


