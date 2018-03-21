#!/usr/bin/env python3
# $Id: analyze_ir1.py,v 1.4 2018/03/21 13:48:36 pi Exp $
# -*- coding: utf-8 -*-
# 日本語

import sys
import os

def main():
    if len(sys.argv) != 2:
        print('usage:')
        print(' $ sudo service lircd stop')
        print(' $ mode2 | tee filename')
        print(' < Push button(s) >')
        print(' [Ctrl]-[C]')
        print(' $ {0} filename'.format(os.path.basename(sys.argv[0])))
        exit(1)

    filename = sys.argv[1]
    f = open(filename, "r")

    line = f.readline()
    while not 'space ' in line:
        line = f.readline()
    #print(line)

    vlist = []
    v1ptnlist = []
    v2ptnlist = []
    for line in f:
        [key, value] = line.split()
        value = int(value)
        if value > 10000:
            value = 10000

        if key == 'pulse':
            a = [value]
            v1ptnlist.append(value)
        else: # space
            a.append(value)
            v2ptnlist.append(value)
            vlist.append(a)

    f.close()

    if key == 'pulse':
        value = 999999
        v2ptnlist.append(value)
        a.append(value)
        vlist.append(a)

    print('vlist =', vlist)

    v1ptnlist = sorted(list(set(v1ptnlist)))
    print('v1ptnlist =', v1ptnlist)
    v1_min = min(v1ptnlist)
    print('v1_min =', v1_min)

    v2ptnlist = sorted(list(set(v2ptnlist)))
    print('v2ptnlist =', v2ptnlist)
    v2_min = min(v2ptnlist)
    print('v2_min =', v2_min)

    sum1 = 0
    count1 = 0
    sum2 = 0
    count2 = 0
    for [v1, v2] in vlist:
        if v1/v1_min < 1.1:
            sum1 += v1
            count1 += 1
        if v2/v2_min < 1.1:
            sum2 += v2
            count2 += 1

    v1_min2 = int(sum1 / count1)
    print('v1_min2 =', v1_min2)
    v2_min2 = int(sum2 / count2)
    print('v2_min2 =', v2_min2)

    sig_list = []
    for [v1, v2] in vlist:
        v = []
        v1 = round(float('{0:.2g}'.format(v1/v1_min2)))
        v.append(v1)
        v2 = round(float('{0:.2g}'.format(v2/v2_min2)))
        v.append(v2)

        sig_list.append(v)
    print('sig_list =', sig_list)

    sig_ptn_list = []
    for v in sig_list:
        key = str(v)
        flag1 = False
        for k in sig_ptn_list:
            if k == key:
                flag1 = True
        if not flag1:
            sig_ptn_list.append(key)
    print('sig_ptn_list = ', sig_ptn_list)

    sym_str = '-01/*ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    print('sym_str = \''+sym_str+'\'')

    bit_count = 0
    byte_value = 0
    for v in sig_list:
        key = str(v)
        idx = sig_ptn_list.index(key)
        ch = sym_str[idx]

        if ch != '0' and ch != '1' and bit_count != 0:
            print('({0:1X}) '.format(byte_value), end='')

        print(ch, end='')

        if ch == '0' or ch == '1':
            if ch == '1':
                byte_value += 2 ** (3-bit_count)
            bit_count += 1
            if bit_count == 4:
                print('({0:1X}) '.format(byte_value), end='')
                bit_count = 0
                byte_value = 0
        else:
            bit_count = 0  
            byte_value = 0

        if ch == '/':
            print()

    print()


if __name__ == '__main__':
    main()
