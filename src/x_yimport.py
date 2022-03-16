'''
    @file           x_yimport.py
    @brief          imports x and y coordinates to be added to lists
    @details        This program imports the xy coordinates the user selects
                    then puts them into useable tuples. This tuple is then 
                    passed to the kinematics program to calculate the 
                    necessary arm angles. 
                    
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
    ''' @brief       opens file and appends columns to useable lists
        @details     After reading the lines from filename, this function will
                     delimit the commas and quotes, then append the values to 
                     lists. 
        
        @param       filename   This is the file that the user selected.
        @return      the x and y coordinates as a tuple
    '''
    
    with open(filename, 'r') as x_y:
        
        listpos = x_y.readlines()
        print(listpos)
        for i in listpos:
            xypos.append(i.strip().split(','))
        print(xypos)
        print(xypos[1][1])
        for xind in range(1,len(listpos)):
            next_x.append(float(xypos[xind][1].strip('"'))) # xypos[xind] is the problem
            
            
        for yind in range(1,len(listpos)):
            next_y.append(float(xypos[yind][2].strip('"')))

    return(next_x, next_y)     


if __name__ == '__main__':
    x_yimport('xy.txt')