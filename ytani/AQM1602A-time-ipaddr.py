#!/usr/bin/env python3
#
# -*- coding: utf-8 -*-
# 日本語

import smbus
from time import sleep
import subprocess
from datetime import datetime
from AQM1602A import AQM1602A

def getipaddr():
    proc = subprocess.Popen(['hostname', '-I'], stdout=subprocess.PIPE)
    ret = proc.communicate()[0].decode('utf-8').strip()
    if ret != '':
        return ret.split()[0]
    else:
        return ''

def main():
    lcd = AQM1602A()
    lcd.init_lcd()

    while True:
        lcd.clear()

        # date & time
        t = datetime.now()
        str = t.strftime('%m/%d')
        wday_str = t.strftime('(%a)')
        str += wday_str
        sec = int(t.strftime('%S'))
        if sec % 2 == 0:
            str += t.strftime(' %H:%M')
        else:
            str += t.strftime(' %H %M')
        lcd.print(str)

        # IP address
        lcd.sec_line()
        lcd.print(getipaddr()[:16])

        sleep(.5)

if __name__ == '__main__':
    main()
