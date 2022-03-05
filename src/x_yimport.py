'''
@file x_yimport.py
'''

import task_share.py

filename = 'xy.txt'
xypos = []

next_x = task_share.Queue('f', 1000, thread_protect = False, overwrite = False,
                         name = 'x-coordinates')
next_y = task_share.Queue('f', 1000, thread_protect = False, overwrite = False,
                         name = 'y-coordinates')


with open(filename, 'r') as x_y:
    listpos = x_y.readlines()
    for i in listpos:
        xypos.append(i.strip().split(','))
    for xind in range(1,len(listpos)):
        next_x.put(float(xypos[xind][1].strip('"')))
    for yind in range(1,len(listpos)):
        next_y.put(float(xypos[yind][2].strip('"')))

print(next_x)
print(next_y)

#ask wade or ridgely why task_share.py not being found
# also ask if our use of queues is right
          