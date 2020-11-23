import os
import numpy as np

rad = 0.0254
dots = 361
cutoff = 10000 # from which timestep to plot the trajectory

xcoord = open('x_coordinate.txt')
ycoord = open('y_coordinate.txt')
fo = open('trajectory.x',"w+")
xlines = xcoord.readlines()[cutoff:]
ylines = ycoord.readlines()[cutoff:]

line1 = '{:>8d}\n'.format(2)
fo.write(line1)
line2 = '{0:>8d}{1:>9d}{2:>9d}{3:>9d}\n'.format(len(xlines),1,dots,1)
fo.write(line2)	

# plot the trajectory of the cylinder center
for i in range(len(xlines)):
	x = xlines[i].split(',')[1]
	flag = ' \n' if (i+1) % 4 == 0 else ''
	fo.write('{: >16.8f}'.format(eval(x)))
	fo.write(flag)
fo.write('\n')
for i in range(len(ylines)):
	y = ylines[i].split(',')[1]
	flag = ' \n' if (i+1) % 4 == 0 else ''
	fo.write('{: >16.8f}'.format(eval(y)))
	fo.write(flag)
fo.write('\n')

# plot the original cyliner
theta = np.arange(dots)
x = rad*np.cos(theta*np.pi/180)
y = rad*np.sin(theta*np.pi/180)
for i in range(dots):
    flag = ' \n' if (i+1) % 4 == 0 else ''
    fo.write('{: >16.8f}'.format(x[i]))
    fo.write(flag)
fo.write('\n')
for i in range(dots):
    flag = ' \n' if (i+1) % 4 == 0 else ''
    fo.write('{: >16.8f}'.format(y[i]))
    fo.write(flag)
	
fo.close()
xcoord.close()
ycoord.close()	