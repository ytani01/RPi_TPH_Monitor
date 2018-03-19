#!/bin/sh

OUTFILE=out.csv

while true; do
    echo -n `date +'%F %H:%M:%S'`
    ./bme280i2c | sed -n 's/^.*Temp : \(.*\)C/ \1/p'
    sleep 1
done
