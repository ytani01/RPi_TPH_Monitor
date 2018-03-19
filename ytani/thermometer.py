#!/usr/bin/env python3
# $Id:$
#
# -*- coding: utf-8 -*-
#
from time import sleep
from BME280I2C import BME280I2C 
from AQM0802A import AQM0802A

def main():
    bme280ch = BME280I2C(0x76)
    lcd = AQM0802A()
    lcd.init_lcd()

    i = 0
    while bme280ch.meas():
        print('{0:5.2f} C {1:5.2f} %'.format(bme280ch.T, bme280ch.H))
        lcd.clear()
        lcd.print('{0:4.1f} C'.format(bme280ch.T))
        if i == 0:
            lcd.print(' .')

        lcd.sec_line()
        lcd.print('{0:4.1f} %'.format(bme280ch.H)) 
        if i == 1:
            lcd.print(' .')

        i = (i + 1) % 2
        sleep(1)

if __name__ == '__main__':
    main()
