#!/bin/sh
echo ${0}
find . -type f ! -name '*.sh' -delete
mkdir largefiles
truncate -s 10M 10M_largefile
cd largefiles
truncate -s 5M 5M_largefile_0
truncate -s 5M 5M_largefile_1
truncate -s 5M 5M_largefile_2