import numpy as np
import matplotlib.pyplot as plt

## ITEM: ATOMS_id type x y z vx vy vz c_S[1] c_S[2] c_S[4] c_nn c_E[1] c_E[2] c_E[4] vx vy vz
data_fn = np.loadtxt('stress_strain.dat')
data_sph = np.loadtxt('SMD_id2576.dat')

fig = plt.figure(constrained_layout=False, figsize=(12, 4))
gs = fig.add_gridspec(1, 3)    

## fig 1: s11
ax = fig.add_subplot(gs[0])
ax.plot(data_fn[:, 3], data_fn[:, 4] , '--r',linewidth=3, label='fenics')
ax.plot(data_sph[:, 3]-data_sph[0, 3],  data_sph[:, 8], 'orange',linewidth=3, label='sph')
ax.set_title("s11")

## fig 2: s22
ax = fig.add_subplot(gs[1])
ax.plot(data_fn[:, 3], data_fn[:, 7] , '--r',linewidth=3, label='fenics')
ax.plot(data_sph[:, 3]-data_sph[0, 3],  data_sph[:, 9], 'orange',linewidth=3, label='sph')
ax.set_title("s22")

## fig 3: s13
ax = fig.add_subplot(gs[2])
ax.plot(data_fn[:, 3], data_fn[:, 5] , '--r',linewidth=3, label='fenics')
ax.plot(data_sph[:, 3]-data_sph[0, 3],  data_sph[:, 10], 'orange',linewidth=3, label='sph')
ax.set_title("s12")

ax.set_xlabel('Strain')
ax.set_ylabel('Stress')
ax.set_title("last")

ax.legend()   
plt.tight_layout()
fig.savefig('./Results.png')
plt.close()    
