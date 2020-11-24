##本脚本生成翼型以及翼型上方圆柱的振动轨迹，封装函数版，多攻角版,增加了初始时刻圆柱外形的绘制
import os
import numpy as np
import pandas as pd

def open_file(dir):
    try:
        data_x = np.loadtxt(dir + 'x_coordinate.txt',delimiter=',',skiprows=cutoff)
        data_y = np.loadtxt(dir + 'y_coordinate.txt',delimiter=',',skiprows=cutoff)
    except:
        print(dir + '部分文件不存在或cutoff值过高'+'\n')
        return 0
    else:
        lines = np.array([data_x.shape[0],data_y.shape[0]])
        line_min = np.min(lines)
        if np.max(lines) != line_min:
            data_x = data_x[:line_min,:]
            data_y = data_y[:line_min,:]
            print(dir +'存在行数不一致，采用最小行'+str(line_min)+'\n')
        else:
            print(dir +'行数一致，共'+str(line_min)+'行\n')
        return data_x[:,1],data_y[:,1]

# plot the naca0012 airfoil:
def naca4_symmetric(dots):
    import sympy as sym
    
    #airfoil parameters:
    ds1 = ds2 = 0.0005
    c = 1.0
    t = 0.12

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
    
def to_mesh_file(tup1):
    fo = open(dir+'trajectory.x',"a+")
    for i in range(len(tup1)):
        for j in range(len(tup1[i])):
            flag = ' \n' if (j+1) % 4 == 0 else ''
            fo.write('{: >16.8f}'.format(tup1[i][j]))
            fo.write(flag)
        fo.write('\n')
    fo.close()
    return 0


distance = [0.03,0.035,0.04,0.045,0.05,
            0.048,0.056,0.064,0.072,0.08,
            0.066,0.072,0.078,0.084,0.093,
            0.08,0.088,0.096,0.104,0.112]
timestep = [200000,120000,80000,60000] 
df = pd.DataFrame({'diameter': [ (i//5+1)/100 for i in range(20) ],
                'distance':distance,
                'total_step':[ timestep[j//5] for j in range(20) ] },
                index=['D'+str(i)+'V'+str(j) for i in range(1,5) for j in range(1,6)] )

case='D2V4' 
dots_cylinder = 101 
aoas = range(12,25)
dots_airfoil = 201
cutoff = df['total_step'][case]-5000 # from which timestep to plot the trajectory
base_dir="F:/00TEMP/temp data/2DVIV/04_airfoil/" + case + "/"
                
for i,aoa in enumerate(aoas):
    dir = base_dir + 'AOA' + str(aoa) + '/'
    print('正在进行'+dir+'的转换......')
    xcoord,ycoord=open_file(dir)

    line1 = '{:>8d}\n'.format(3)
    line2 = '{0:>8d}{1:>9d}{2:>9d}{3:>9d}{4:>9d}{5:>9d}\n'.format(len(xcoord),1, dots_airfoil*2+1, 1,dots_cylinder,1)
    fo = open(dir+'trajectory.x',"w")
    fo.write(line1+line2)
    fo.close()

    x_t,y_t = naca4_symmetric(dots_airfoil)
    x_a = np.r_[x_t[::-1],0,x_t]
    y_a = np.r_[y_t[::-1],0,-y_t]

    theta = np.linspace(0,360,dots_cylinder,endpoint=True)
    x_c = df['diameter'][case]/2*np.cos(theta*np.pi/180)
    y_c = df['distance'][case] + df['diameter'][case]/2*np.sin(theta*np.pi/180)

    tup1 = tuple([xcoord,ycoord,x_a,y_a,x_c,y_c])
    to_mesh_file(tup1)
   
