#!/usr/bin/env python3
#
# -*- coding: utf-8 -*-
# 日本語

import smbus
from time import sleep
import subprocess
from datetime import datetime
from AQM0802A import AQM0802A

def getipaddr():
    proc = subprocess.Popen(['hostname', '-I'], stdout=subprocess.PIPE)
    ret = proc.communicate()[0].decode('utf-8').strip()
    if ret != '':
        return ret.split()[0]
    else:
        return ''

def main():
    lcd = AQM0802A()
    lcd.init_lcd()

    while True:
        lcd.clear()

        # date & time
        t = datetime.now()
        str = t.strftime('%m/%d ')
        str += t.strftime('%a')[:2]
        lcd.print(str)
        lcd.sec_line()
        lcd.print(t.strftime('%H:%M'))

        sleep(3)

        # IP address
        ipaddr = getipaddr().split('.')
        lcd.clear()
        if len(ipaddr) == 4:
            lcd.print(ipaddr[0]+'.'+ipaddr[1]+'.')
            lcd.sec_line()
            lcd.print(ipaddr[2]+'.'+ipaddr[3])
        else:
            lcd.print('no IP')
            lcd.sec_line()
            lcd.print(' address')

        sleep(3)

if __name__ == '__main__':
    main()
