#!/usr/bin/python3 -u
# $Id: thermometer-ipaddr-time.py,v 1.7 2018/04/03 16:54:52 pi Exp $
#
# -*- coding: utf-8 -*-
#

from time import sleep
from BME280I2C import BME280I2C 
from AQM1602A import AQM1602A
from AQM1602A import EightCharsColumns
import subprocess
from datetime import datetime

def getipaddr():
    proc = subprocess.Popen(['hostname', '-I'], stdout=subprocess.PIPE)
    ret = proc.communicate()[0].decode('utf-8').strip()
#    print('ret =', ret)
    if ret != '':
        return ret.split()[0]
    else:
        return ''

def main():
    global lcd

    bme280ch = BME280I2C(0x76)
    ecc = EightCharsColumns()
    ecc.init()

    while True:
        # date & time
        t = datetime.now()
        line1 = t.strftime('%m/%d%a')[:7]
        line2 = t.strftime('%H:%M')

        ecc.print(line1, line2)

        print(t.strftime('%Y-%m-%d(%a) %H:%M:%S'))
        sleep(3)

        # Temperature
        if bme280ch.meas():
            t_value = bme280ch.T
            h_value = bme280ch.H

            t = '{0:4.1f}{1:c}C'.format(t_value, 0xdf)
            h = '{0:4.1f} %'.format(h_value)
    
            ecc.print(t, h)
    
            t = '{0:4.1f} C'.format(t_value)
            print('{}, {}'.format(t,h))
            sleep(3)

        # IP address
        ipaddr = getipaddr().split('.')
        if len(ipaddr) == 4:
            ecc.print(ipaddr[0]+'.'+ipaddr[1]+'.', ipaddr[2]+'.'+ipaddr[3])

            print('IP address = {0}'.format('.'.join(ipaddr)))
            sleep(3)

if __name__ == '__main__':
    try:
        main()
    finally:
        lcd.clear()
