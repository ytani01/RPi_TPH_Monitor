#!/usr/bin/python3 -u
# $Id: thermometer-ipaddr-time.py,v 1.5 2018/03/26 15:35:41 pi Exp pi $
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

    t = ''
    h = ''
    i = 0
    while bme280ch.meas():
        # date & time
        t = datetime.now()
        wday_str = t.strftime('%a')
        lcd.clear()
        datestr = t.strftime('%m-%d '+wday_str[0]+wday_str[1])
        timestr = t.strftime('%H:%M ')
        lcd.print(datestr)
        lcd.print(timestr)
        print(t.strftime('%Y-%m-%d(%a) %H:%M:%S'))
        sleep(3)

        # Temperature
        if bme280ch.meas():
            prev_t = t
            prev_h = h
            t = '{0:4.1f}{1:c}C'.format(bme280ch.T,0xdf)
            h = '{0:4.1f} %'.format(bme280ch.H)
    
            lcd.clear()
            lcd.print(t)
            if i == 0:
                lcd.print(' .')
    
            lcd.sec_line()
            lcd.print(h)
            if i == 1:
                lcd.print(' .')
    
            print(t+', '+h)
    
            i = (i + 1) % 2
            sleep(3)

        # IP address
        ipaddr = getipaddr().split('.')
        if len(ipaddr) == 4:
            lcd.clear()
            lcd.print(ipaddr[0]+'.'+ipaddr[1]+'.')
            lcd.sec_line()
            lcd.print(ipaddr[2]+'.'+ipaddr[3])
            print(ipaddr)
            sleep(3)

if __name__ == '__main__':
    try:
        main()
    finally:
        lcd.clear()
