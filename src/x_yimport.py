'''
    @file           x_yimport.py
    @author         Jeremy Baechler
    @author         Kendall Chappell
    @author         Matthew Wimberley
    @date           22-Feb-2022
'''

import task_share

filename = 'xy.txt'
xypos = []

next_y = []
next_x = []


def x_yimport(filename):
    with open(filename, 'r') as x_y:
        
        listpos = x_y.readlines()
        
        for i in listpos:
            xypos.append(i.strip().split(','))

        for xind in range(1,len(listpos)):
            next_x.append(float(xypos[xind][1].strip('"'))) # xypos[xind] is the problem
            
            
        for yind in range(1,len(listpos)):
            next_y.append(float(xypos[yind][2].strip('"')))

    return(next_x, next_y)     
