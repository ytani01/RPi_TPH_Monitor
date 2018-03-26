#!/usr/bin/env python3
#
# -*- coding: utf-8 -*-
# 日本語

import smbus
from time import sleep
import subprocess
from datetime import datetime

class AQM1602A:
    def __init__(self):
        self.i2c_addr = 0x3E
        self.i2c = smbus.SMBus(1)
        self.count = 0  # Count number of character in current line
        self.line = 1   # Current line number

    # I2C write one byte data to addr
    def write_address_onebyte(self, addr, data):
        data_list = [data]
        try:
            self.i2c.write_i2c_block_data(self.i2c_addr, addr, data_list)
        except IOError:
            return False

        sleep(100/1000000)

        return True

    # Initialize LCD
    def init_lcd(self):
        self.write_address_onebyte(0, 0x38)
        self.write_address_onebyte(0, 0x39)
        self.write_address_onebyte(0, 0x14)
        self.write_address_onebyte(0, 0x73)
        self.write_address_onebyte(0, 0x56)
        self.write_address_onebyte(0, 0x6C)
        sleep(0.25)
        self.write_address_onebyte(0, 0x38)
        self.write_address_onebyte(0, 0x0C)
        self.clear();

    # Print string on LCD
    def print(self, str):
        chars = list(str)
        for i in range(len(chars)):
            self.count += 1
            if self.count > 16:
                if self.line==2:
                    self.home()
                else:
                    self.sec_line()
                self.count += 1
            self.write_address_onebyte(0x40, ord(chars[i]))

    # Clear LCD and return to home
    def clear(self):
        self.count = 0
        self.line = 1
        self.write_address_onebyte(0, 0x1)
        sleep(0.002)

    # Return to home without deleting characters
    def home(self):
        self.count = 0
        self.line = 1
        self.write_address_onebyte(0, 0x2)
        sleep(0.002)

    # Go to second line
    def sec_line(self):
        self.count = 0
        self.line = 2
        self.write_address_onebyte(0, 0xC0)
        sleep(0.001)


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
