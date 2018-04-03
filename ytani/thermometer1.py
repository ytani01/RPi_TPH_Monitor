#!/usr/bin/env python3
# $Id: thermometer1.py,v 1.1 2018/04/03 16:54:52 pi Exp $
#
# -*- coding: utf-8 -*-
#
from time import sleep
from BME280I2C import BME280I2C 

def main():
    bme280ch = BME280I2C(0x76)

    t = ''
    h = ''
    i = 0
    while bme280ch.meas():
        prev_t = t
        prev_h = h
        t = '{0:4.1f} C'.format(bme280ch.T)
        h = '{0:4.1f} %'.format(bme280ch.H)

        if t != prev_t:
            print(t+', '+h)

        i = (i + 1) % 2
        sleep(1)

if __name__ == '__main__':
        main()
