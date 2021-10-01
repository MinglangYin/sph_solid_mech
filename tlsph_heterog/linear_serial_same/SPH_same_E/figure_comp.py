import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import Rbf

## plot stress field
data_sph1 = np.loadtxt('SPH_1type/SMD_id664.dat')
data_sph2 = np.loadtxt('SPH_2type/SMD_id664.dat')

fig = plt.figure(constrained_layout=False, figsize=(5, 5))
gs = fig.add_gridspec(1, 1)    

## fig 1: FEM
ax = fig.add_subplot(gs[0])
ax.plot(data_sph2[:, 3], data_sph2[:, 9], 'b', linewidth=3, label='2 type')
ax.plot(data_sph1[:, 3], data_sph1[:, 9], '--r', linewidth=3, label='1 type')
# ax.set_title("FEM")
ax.set_xlabel("strectch")
ax.set_ylabel("s22")
ax.legend()

plt.tight_layout()
fig.savefig('./Results.png')
plt.close()    

