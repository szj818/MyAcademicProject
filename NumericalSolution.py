import sympy as sym
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
sym.init_printing()
%matplotlib inline

x0 = 0.5
dx0 = 0.0
fn = 0.4
zeta = 0.00542
z = 0.5
q = 1.0

omega_0 = 2*np.pi*fn
dt = 1/(fn*50)
t_tot = 1/fn*150

def func(q_dt,X_0,U_0):
    return q_dt - omega_0**2*X_0-2*zeta*omega_0*U_0

def solveRK4(q_dt,dt,X_0,U_0):
    L1 = func(q_dt,X_0,U_0)
    L2 = func(q_dt,X_0+dt*U_0/2,U_0+dt*L1/2)
    L3 = func(q_dt,X_0+dt*U_0/2+dt**2*L1/4,U_0+dt*L2/2)
    L4 = func(q_dt,X_0+dt*U_0+dt**2*L2/2,U_0+dt*L3)
    X_dt = X_0+dt*U_0+dt**2*(L1+L2+L3)/6
    U_dt = U_0+dt*(L1+2*L2+2*L3+L4)/6
    return X_dt,U_dt

t = np.arange(0,t_tot,dt)
X_t,U_t=np.array(([x0],[dx0]))
Q_t = q*np.sin(z*omega_0*t)

for i in range(t.shape[0]-1):
    X_temp,U_temp = solveRK4(Q_t[i+1],dt,X_t[i],U_t[i])
    X_t = np.append(X_t,X_temp)
    U_t = np.append(U_t,U_temp)

plt.figure(figsize=(12,8))
plt.plot(t,X_t)
plt.title('简谐激振力下粘性阻尼系统的受迫振动的解析解与数值解比较',fontsize=20,loc = 'center')
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.grid(True)
plt.ylabel('$y$(m)',size=24,rotation=90)
plt.xlabel('$t(s)$',size=24)
plt.legend(['数值解'],fontsize='xx-large',loc='upper right',fancybox=False,shadow=True,edgecolor='black')
plt.savefig('UDFverification/z='+str(z)+'数值解.png',dpi=200)
data = np.stack([t,X_t],axis=1)
np.savetxt('UDFverification/z='+str(z)+'数值解.dat',data,fmt='%f',delimiter=',')