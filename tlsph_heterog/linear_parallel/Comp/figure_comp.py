import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import Rbf

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

s_fn = data_fn[:, 4:8]
x_fn = data_fn[:, 0:2]
s_sph = data_sph[:, 8:11]
x_sph = data_sph_init[:, 2:4]

fig = plt.figure(constrained_layout=False, figsize=(12, 12))
gs = fig.add_gridspec(3, 3)    

# s11
s11_fn_func = Rbf(x_fn[:, 0], x_fn[:, 1], s_fn[:, 0])
s11_fn_intp = s11_fn_func(xx_flat, yy_flat).reshape(dim, dim)
s12_fn_func = Rbf(x_fn[:, 0], x_fn[:, 1], s_fn[:, 1])
s12_fn_intp = s12_fn_func(xx_flat, yy_flat).reshape(dim, dim)
s22_fn_func = Rbf(x_fn[:, 0], x_fn[:, 1], s_fn[:, 3])
s22_fn_intp = s22_fn_func(xx_flat, yy_flat).reshape(dim, dim)

s11_sph_func = Rbf(x_sph[:, 0], x_sph[:, 1], s_sph[:, 0])
s11_sph_intp = s11_sph_func(xx_flat, yy_flat).reshape(dim, dim)
s12_sph_func = Rbf(x_sph[:, 0], x_sph[:, 1], s_sph[:, 2])
s12_sph_intp = s12_sph_func(xx_flat, yy_flat).reshape(dim, dim)
s22_sph_func = Rbf(x_sph[:, 0], x_sph[:, 1], s_sph[:, 1])
s22_sph_intp = s22_sph_func(xx_flat, yy_flat).reshape(dim, dim)

## fig 1: FEM
ax = fig.add_subplot(gs[0])
h = ax.imshow(s11_fn_intp, vmin=0.0, vmax=0.1)
ax.set_title("FEM")
ax.set_xlabel('x')
ax.set_ylabel('y')
fig.colorbar(h, ax=ax,orientation='horizontal')

## fig 2: SPH
ax = fig.add_subplot(gs[1])
h = ax.imshow(s11_sph_intp, vmin=0.0, vmax=0.1)
ax.set_title("SPH")
fig.colorbar(h, ax=ax,orientation='horizontal')

# ## fig 3: Err
ax = fig.add_subplot(gs[2])
h = ax.imshow(abs(s11_sph_intp - s11_fn_intp), vmin=0.0, vmax=0.01)
ax.set_title("Error s11")
fig.colorbar(h, ax=ax,orientation='horizontal')


## fig 4: FEM
ax = fig.add_subplot(gs[3])
h = ax.imshow(s12_fn_intp, vmin=-0.05, vmax=0.05)
ax.set_title("FEM")
ax.set_xlabel('x')
ax.set_ylabel('y')
fig.colorbar(h, ax=ax,orientation='horizontal')


## fig 5: SPH
ax = fig.add_subplot(gs[4])
h = ax.imshow(s12_sph_intp, vmin=-0.05, vmax=0.05)
ax.set_title("SPH")
fig.colorbar(h, ax=ax, orientation='horizontal')

# ## fig 6: Err
ax = fig.add_subplot(gs[5])
h = ax.imshow(abs(s12_sph_intp - s12_fn_intp), vmin=0.0, vmax=0.01)
ax.set_title("Error s12")
fig.colorbar(h, ax=ax,orientation='horizontal')

## fig 7: FEM
ax = fig.add_subplot(gs[6])
h = ax.imshow(s22_fn_intp, vmin=0.1, vmax=0.3)
ax.set_title("FEM")
ax.set_xlabel('x')
ax.set_ylabel('y')
fig.colorbar(h, ax=ax,orientation='horizontal')

## fig 8: SPH
ax = fig.add_subplot(gs[7])
h = ax.imshow(s22_sph_intp, vmin=0.1, vmax=0.3)
ax.set_title("SPH")
fig.colorbar(h, ax=ax,orientation='horizontal')

# ## fig 9: Err
ax = fig.add_subplot(gs[8])
ax.imshow(abs(s22_sph_intp - s22_fn_intp), vmin=0.0, vmax=0.02)
ax.set_title("Error s22")
fig.colorbar(h, ax=ax,orientation='horizontal')

plt.tight_layout()
fig.savefig('./Results.png')
plt.close()    

