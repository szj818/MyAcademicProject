##本脚本生成翼型以及翼型上方圆柱的振动轨迹，最初版本，未封装函数
import os
import numpy as np

rad = 0.0254
dots = 201
cutoff = 110000 # from which timestep to plot the trajectory

xcoord = open('x_coordinate.txt')
ycoord = open('y_coordinate.txt')
fo = open('trajectory.x',"w+")
xlines = xcoord.readlines()[cutoff:]
ylines = ycoord.readlines()[cutoff:]

line1 = '{:>8d}\n'.format(2)
fo.write(line1)
line2 = '{0:>8d}{1:>9d}{2:>9d}{3:>9d}\n'.format(len(xlines),1, dots*2+1, 1)
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



# plot the naca0012 airfoil:
def naca4_symmetric(dots):
    import numpy as np
    import sympy as sym
    
    #airfoil parameters:
    ds1 = ds2 = 0.0005
    c = 1.0
    t = 0.12
    dots = 201

    #generate x coordinates in tanh distribution:
    x_s = sym.Symbol('x_s')
    ksi = np.linspace(0.0,c,dots)
    A = np.sqrt(ds2)/np.sqrt(ds1)
    B = 1/(c*np.sqrt(ds1*ds2))
    delta = sym.nsolve(sym.sinh(x_s)/x_s - B, x_s, 11.7)
    delta = np.array(delta,dtype=float)
    u = 0.5*(1+np.tanh(delta*(ksi/c-0.5))/np.tanh(delta/2))
    s = u/(A+(1-A)*u)
    x = s*c
    
    #genertae y coordinates:
    y = 5.0 * t * c * ( \
        0.2969 * np.sqrt ( x / c )\
        + (((( \
          - 0.1015 ) * ( x / c ) \
          + 0.2843 ) * ( x / c ) \
          - 0.3516 ) * ( x / c ) \
          - 0.1260 ) * ( x / c ) )
    return x,y

x_t,y_t = naca4_symmetric(dots)
x_a = np.r_[x_t[::-1],0,x_t]
y_a = np.r_[y_t[::-1],0,-y_t]
for i in range(len(x_a)):
    flag = ' \n' if (i+1) % 4 == 0 else ''
    fo.write('{: >16.8f}'.format(x_a[i]))
    fo.write(flag)
fo.write('\n')
for i in range(len(x_a)):
    flag = ' \n' if (i+1) % 4 == 0 else ''
    fo.write('{: >16.8f}'.format(y_a[i]))
    fo.write(flag)
	
fo.close()
xcoord.close()
ycoord.close()	
