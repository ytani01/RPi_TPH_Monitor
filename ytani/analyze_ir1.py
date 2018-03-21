#!/usr/bin/env python3
# $Id: analyze_ir1.py,v 1.2 2018/03/21 10:36:13 pi Exp pi $
# -*- coding: utf-8 -*-
# 日本語

import sys
import os

def main():
    if len(sys.argv) != 2:
        print('usage:')
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
    vptnlist = []
    for line in f:
        [key, value] = line.split()
        value = int(value)
        if value > 10000:
            value = 10000

        vptnlist.append(value)
        if key == 'pulse':
            a = [value]
        else:
            a.append(value)
            vlist.append(a)

    f.close()

    if key == 'pulse':
        vptnlist.append(999999)
        a.append(999999)
        vlist.append(a)

    print('vlist =', vlist)

    vptnlist = sorted(list(set(vptnlist)))
    print('vptnlist =', vptnlist)

    v_min = min(vptnlist)
    print('v_min =', v_min)

    sum = 0
    count = 0
    for [v1, v2] in vlist:
        if v1/v_min < 1.1:
            sum += v1
            count += 1
        if v2/v_min < 1.1:
            sum += v2
            count += 1
    v_min2 = int(sum / count)
    print('v_min2 =', v_min2)

    sig_list = []
    for v in vlist:
        v1 = []
        for vv in v:
            vv = round(float('{0:.1g}'.format(vv/v_min2)))
            v1.append(vv)
        sig_list.append(v1)
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

    sym_str = '-01/ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    print('sym_str = \''+sym_str+'\'')

    bit_count = 0
    for v in sig_list:
        key = str(v)
        idx = sig_ptn_list.index(key)
        ch = sym_str[idx]
        print(ch, end='')
        if ch == '0' or ch == '1':
            bit_count += 1
            if bit_count == 4:
                print(' ', end='')
                bit_count = 0
        else:
            bit_count = 0

        if ch == '/':
            print()

    print()


if __name__ == '__main__':
    main()
