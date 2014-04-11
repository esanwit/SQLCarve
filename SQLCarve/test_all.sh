#!/bin/bash


#
#  See ../LICENSE
#
# This file can be used to automate some tests.
#
#

#Make output directory
mkdir log


#Easy running of one test, argument is which config file to use
#Output logged is at least the statistics at the end

function runonetest(){
LOGFILE="./log/$1.log"
echo $LOGFILE
./scanner.py $1 --d -s --r > $LOGFILE &
}

runonetest config_inno_a.py
runonetest config_inno_b.py
runonetest config_inno_c.py
runonetest config_inno_city.py
runonetest config_innor_a.py
runonetest config_isam_a.py
runonetest config_isam_b.py
runonetest config_isam_city.py

wait

