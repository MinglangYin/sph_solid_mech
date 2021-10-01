import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import Rbf

# ## ITEM: ATOMS_id type x y z vx vy vz c_S[1] c_S[2] c_S[4] c_nn c_E[1] c_E[2] c_E[4] vx vy vz
# data_fn = np.loadtxt('stress_strain.dat')
# data_sph = np.loadtxt('SMD_id2576.dat')

# fig = plt.figure(constrained_layout=False, figsize=(12, 4))
# gs = fig.add_gridspec(1, 3)    

# ## fig 1: s11
# ax = fig.add_subplot(gs[0])
# ax.plot(data_fn[:, 3], data_fn[:, 4] , '--r',linewidth=3, label='fenics')
# ax.plot(data_sph[:, 3]-data_sph[0, 3],  data_sph[:, 8], 'orange',linewidth=3, label='sph')
# ax.set_title("s11")

# ## fig 2: s22
# ax = fig.add_subplot(gs[1])
# ax.plot(data_fn[:, 3], data_fn[:, 7] , '--r',linewidth=3, label='fenics')
# ax.plot(data_sph[:, 3]-data_sph[0, 3],  data_sph[:, 9], 'orange',linewidth=3, label='sph')
# ax.set_title("s22")

# ## fig 3: s13
# ax = fig.add_subplot(gs[2])
# ax.plot(data_fn[:, 3], data_fn[:, 5] , '--r',linewidth=3, label='fenics')
# ax.plot(data_sph[:, 3]-data_sph[0, 3],  data_sph[:, 10], 'orange',linewidth=3, label='sph')
# ax.set_title("s12")

# ax.set_xlabel('Strain')
# ax.set_ylabel('Stress')
# ax.set_title("last")

# ax.legend()   
# plt.tight_layout()
# fig.savefig('./Results.png')
# plt.close()    

## plot stress field
data_fn = np.loadtxt('snapshot_FEM.dat')

data_sph = np.loadtxt('snapshot_10.dat')
sort_id = data_sph[:, 0].argsort()
data_sph = data_sph[sort_id]

data_sph_init = np.loadtxt('snapshot_0.dat')
sort_id = data_sph_init[:, 0].argsort()
data_sph_init = data_sph_init[sort_id]

dim = 26

x = np.linspace(0, 1, dim)[:, None]
xx, yy = np.meshgrid(x, x)
xx_flat = xx.flatten()[:, None]
yy_flat = yy.flatten()[:, None]

s_fn = data_fn[:, -1:]
x_fn = data_fn[:, 0:2]
s_fn_func = Rbf(x_fn[:, 0], x_fn[:, 1], s_fn[:, 0])
s_fn_intp = s_fn_func(xx_flat, yy_flat).reshape(dim, dim)


s_sph = data_sph[:, 9:10]
x_sph = data_sph_init[:, 2:4]
s_sph_func = Rbf(x_sph[:, 0], x_sph[:, 1], s_sph[:, 0])
s_sph_intp = s_sph_func(xx_flat, yy_flat).reshape(dim, dim)


fig = plt.figure(constrained_layout=False, figsize=(12, 4))
gs = fig.add_gridspec(1, 3)    

## fig 1: FEM
ax = fig.add_subplot(gs[0])
ax.imshow(s_fn_intp, vmin=0.1, vmax=0.2)
ax.set_title("FEM")

## fig 2: SPH
ax = fig.add_subplot(gs[1])
ax.imshow(s_sph_intp, vmin=0.1, vmax=0.2)
ax.set_title("SPH")

# ## fig 3: Err
ax = fig.add_subplot(gs[2])
ax.imshow(abs(s_sph_intp - s_fn_intp), vmin=0.0, vmax=0.02)
ax.set_title("Error")

ax.set_xlabel('x')
ax.set_ylabel('y')

plt.tight_layout()
fig.savefig('./Results.png')
plt.close()    

