#!/usr/bin/env python3
# $Id: thermometer-ipaddr.py,v 1.1 2018/03/26 16:38:13 pi Exp pi $
#
# -*- coding: utf-8 -*-
#

from time import sleep
from BME280I2C import BME280I2C 
from AQM0802A import AQM0802A
import subprocess

def getipaddr():
    proc = subprocess.Popen(['hostname', '-I'], stdout=subprocess.PIPE)
    return proc.communicate()[0].decode('utf-8').split()[0]

def main():
    global lcd

    bme280ch = BME280I2C(0x76)
    lcd = AQM0802A()
    lcd.init_lcd()

    t = ''
    h = ''
    i = 0
    while bme280ch.meas():
        prev_t = t
        prev_h = h
        t = '{0:4.1f} C'.format(bme280ch.T)
        h = '{0:4.1f} %'.format(bme280ch.H)

        lcd.clear()
        lcd.print(t)
        if i == 0:
            lcd.print('.')

        lcd.sec_line()
        lcd.print(h)
        if i == 1:
            lcd.print('.')

        if t != prev_t:
            print(t+', '+h)

        i = (i + 1) % 2
        sleep(2)

        # print IP address
        ipaddr = getipaddr().split('.')
        lcd.clear()
        lcd.print(ipaddr[0]+'.'+ipaddr[1]+'.')
        lcd.sec_line()
        lcd.print(ipaddr[2]+'.'+ipaddr[3])
        sleep(2)

if __name__ == '__main__':
    try:
        main()
    finally:
        lcd.clear()
