#!/usr/bin/env python3
# $Id: ir_analyze.py,v 1.7 2018/03/23 15:29:32 pi Exp pi $
# -*- coding: utf-8 -*-
# 日本語

import sys
import os

SIG_LONG = 9999
SIG_END  = 99999

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

    sig_list_raw = []
    for line in f:
        [key, value] = line.split()
        sig_list_raw.append(int(value))
    f.close()
    print('sig_list_raw =')
    print(sig_list_raw)

    if key == 'pulse':
        sig_list_raw.append(SIG_END)

    sig_list = []
    v1ptnlist = []
    v2ptnlist = []
    a = []
    for v in sig_list_raw:
        if v > SIG_LONG:
            v = SIG_LONG

        a.append(v)
        if len(a) == 1:
            v1ptnlist.append(v)
        if len(a) == 2:
            v2ptnlist.append(v)
            sig_list.append(a)
            a = []

    print('sig_list =')
    print(sig_list)

    v1ptnlist = sorted(list(set(v1ptnlist)))
    print('v1ptnlist =')
    print(v1ptnlist)
    v2ptnlist = sorted(list(set(v2ptnlist)))
    print('v2ptnlist =')
    print(v2ptnlist)

    t1 = min(v1ptnlist)
    t2 = min(v2ptnlist)
    print('(t1, t2) =', (t1, t2))

#    t1_max = t1
#    for v in v1ptnlist:
#        if v >= t1 * 1.2:
#            break
#        t1_max = v
#    t1a = (t1 + t1_max) / 2
#
#    t2_max = t2
#    for v in v2ptnlist:
#        if v > t2 * 1.2:
#            break
#        t2_max = v
#    t2a = (t2 + t2_max) / 2
#
#    print('(t1_max, t2_max) =', (t1_max, t2_max))
#    print('(t1a, t2a) =', (t1a, t2a))

    sum1 = 0
    count1 = 0
    sum2 = 0
    count2 = 0
    v_max_factor = 1.1
    for [v1, v2] in sig_list:
        if v1/t1 < v_max_factor:
            sum1 += v1
            count1 += 1
        if v2/t2 < v_max_factor:
            sum2 += v2
            count2 += 1

    t1a = int(sum1 / count1)
    t2a = int(sum2 / count2)
    print('(t1a, t2a) =', (t1a, t2a))

    sig_list_round = []
    for [v1, v2] in sig_list:
        v1 = round(float('{0:.2g}'.format(v1/t1a)))
        v2 = round(float('{0:.2g}'.format(v2/t2a)))
        sig_list_round.append([v1, v2])
    print('sig_list_round =')
    print(sig_list_round)

    sig_ptn_list = []
    for v in sig_list_round:
        if not v in sig_ptn_list:
            sig_ptn_list.append(v)
    print('sig_ptn_list =', sig_ptn_list)

    sym_str = '-01/abcdefghijklmnopqrstuvwxyz'
    if sig_ptn_list[1][1] != 1:
        sym_str = '-10/abcdefghijklmnopqrstuvwxyz'
    print('sym_str = \'' + sym_str + '\'')

    print()
    bit_ptn = ''
    sig_str = ''
    for v in sig_list_round:
        idx = sig_ptn_list.index(v)
        ch = sym_str[idx]

        if len(bit_ptn) > 0 and (not ch in '01'):
#            print(':{0:1X}/{1:1X} '.format(int(bit_ptn, 2), int(bit_ptn[::-1], 2)), end='')
            bit_ptn = ''

#        print(ch, end='')
        sig_str += ch

        if ch in '01':
            bit_ptn += ch
            if len(bit_ptn) == 4:
#                print(':{0:1X}/{1:1X} '.format(int(bit_ptn, 2), int(bit_ptn[::-1], 2)), end='')
                bit_ptn = ''
        else:
            bit_ptn = ''

#        if ch == '/':
#            print()

#    if bit_ptn != '':
#        print(':{0:1X}/{1:1X} '.format(int(bit_ptn, 2), int(bit_ptn[::-1], 2)), end='')
#        print('bit_ptn = \'' + bit_ptn + '\'')

    print('sig_str = \''+sig_str+'\'')
    print()

    sig_str2 = '2:'
    bit_ptn = ''
    for ch in sig_str:
        if len(bit_ptn) == 4:
            sig_str2 += ' '
            bit_ptn = ''
        sig_str2 += ch
        if ch in '01':
            bit_ptn += ch
        if ch == '/':
            sig_str2 += '\n2:'
            bit_ptn = ''
    print('sig_str2 =')
    print(sig_str2)

    sig_str3 = '3:'
    bit_ptn = ''
    for ch in sig_str:
        if ((not ch in '01') and len(bit_ptn) > 0) or ((ch in '01') and len(bit_ptn) == 4):
            sig_str3 += '{0:1X}'.format(int(bit_ptn, 2))
            bit_ptn = ''
        if ch in '01':
            bit_ptn += ch
        else:
            sig_str3 += ch
        if ch == '/':
            sig_str3 += '\n3:'
    if bit_ptn != '':
        sig_str3 += '{0:1X}'.format(int(bit_ptn, 2))
    print('sig_str3 =')
    print(sig_str3)

    sig_str4 = '4:'
    bit_ptn = ''
    for ch in sig_str:
        if ((not ch in '01') and len(bit_ptn) > 0) or ((ch in '01') and len(bit_ptn) == 4):
            sig_str4 += '{0:1X}'.format(int(bit_ptn[::-1], 2))
            bit_ptn = ''
        if ch in '01':
            bit_ptn += ch
        else:
            sig_str4 += ch
        if ch == '/':
            sig_str4 += '\n4:'
    if bit_ptn != '':
        sig_str4 += '{0:1X}'.format(int(bit_ptn, 2))
    print('sig_str4 =')
    print(sig_str4)

    print()
    print('sig_list_raw =')
    v_count = 0
    v_prev = 0
    for v in sig_list_raw:
        print('{0:4d} '.format(v), end='')
        v_count += 1
        v1 = round(float('{0:.2g}'.format(v_prev/t1a)))
        v2 = round(float('{0:.2g}'.format(v     /t2a)))
        #print('(v1, v2) =', (v1, v2))
        if v_count == 16 or v >= SIG_LONG or \
                (v_count % 2 == 0 and v1 == sig_ptn_list[0][0] and v2 == sig_ptn_list[0][1]):
            print()
            v_count = 0
            v = 0
        v_prev = v

if __name__ == '__main__':
    main()
