#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 日本語

import smbus
from time import sleep

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


class EightCharsColumns:
    def __init__(self):
        self.lcd = AQM1602A()

    def init_lines(self):
        self.line1 = '----------------'
        self.line2 = '----------------'

    def clear(self):
        self.lcd.clear()
        self.init_lines()

    def init(self):
        self.lcd.init_lcd()
        self.clear()

    def print(self, l1, l2):

        l1 = (l1[:7] + '        ')[:8]
        l2 = (l2[:7] + '        ')[:8]

        self.line1 += l1
        self.line2 += l2

        for i in range(8):
            self.line1 = self.line1[1:]
            self.line2 = self.line2[1:]

            tmp_l1 = self.line1[:16]
            tmp_l2 = self.line2[:16]

            self.lcd.clear()
            self.lcd.print(tmp_l1)
            self.lcd.sec_line()
            self.lcd.print(tmp_l2)

            print(self.line1)
            print(tmp_l1)
            print(self.line2)
            print(tmp_l2)
            print()

            sleep(.1)


def main():
    ecc = EightCharsColumns()
    ecc.init()

    ecc.print('abc', '123')
    sleep(3)
    ecc.print('def', '456')
    sleep(3)
    ecc.print('ghi', '789')
    sleep(3)
    ecc.print('jkl', '012')
    
'''
    lcd = AQM1602A()
    lcd.init_lcd()

    lcd.print('AQM1602')
    sleep(1)
    lcd.clear()
    sleep(1)
    lcd.print('Test')
    sleep(1)
    lcd.sec_line()
    lcd.print('Success')
    sleep(1)

    lcd.clear()
    ch = 0x0f
    while True:
        lcd.print(chr(ch))
        ch += 1
        if ch > 0xff:
            ch = 0x0f
        sleep(0.1)
'''

if __name__ == '__main__':
    main()
