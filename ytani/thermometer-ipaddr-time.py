#!/usr/bin/python3 -u
# $Id: thermometer-ipaddr-time.py,v 1.1 2018/03/26 16:38:13 pi Exp pi $
#
# -*- coding: utf-8 -*-
#

from time import sleep
from BME280I2C import BME280I2C 
from AQM0802A import AQM0802A
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
    lcd = AQM0802A()
    lcd.init_lcd()

    while bme280ch.meas():
        # date & time
        t = datetime.now()
        line1 = t.strftime('%m/%d %a')[:8]
        line2 = t.strftime('%H:%M')

        lcd.clear()
        lcd.print(line1)
        lcd.sec_line()
        lcd.print(line2)

        print(t.strftime('%Y-%m-%d(%a) %H:%M:%S'))
        sleep(3)

        # Temperature
        if bme280ch.meas():
            t = '{0:4.1f}{1:c}C'.format(bme280ch.T,0xdf)
            h = '{0:4.1f} %'.format(bme280ch.H)
    
            lcd.clear()
            lcd.print(t)
            lcd.sec_line()
            lcd.print(h)
    
            t = '{0:4.1f} C'.format(bme280ch.T)
            print('{}, {}'.format(t,h))
            sleep(3)

        # IP address
        ipaddr = getipaddr().split('.')
        if len(ipaddr) == 4:
            lcd.clear()
            lcd.print(ipaddr[0]+'.'+ipaddr[1]+'.')
            lcd.sec_line()
            lcd.print('{:>8}'.format(ipaddr[2]+'.'+ipaddr[3]))

            print('IP address = {0}'.format('.'.join(ipaddr)))
            sleep(3)

if __name__ == '__main__':
    try:
        main()
    finally:
        lcd.clear()
