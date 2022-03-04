'''
@file x_yimport.py
'''

# import pyb
# import utime

filename = 'xy.txt'
xypos = []
x = []
y = []

with open(filename, 'r') as x_y:
    listpos = x_y.readlines()
    for i in listpos:
        xypos.append(i.strip().split(','))
    for xind in range(1,len(listpos)):
        x.append(float(xypos[xind][1].strip('"')))
    for yind in range(1,len(listpos)):
        y.append(float(xypos[yind][2].strip('"')))
    print(x)
    print(y)
    