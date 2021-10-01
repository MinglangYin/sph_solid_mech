import numpy as np
import matplotlib.pyplot as plt

file_name = 'Results/result_FEM.dat'
data_fn = np.loadtxt(file_name)

fig = plt.figure(constrained_layout=False, figsize=(6, 6))
gs = fig.add_gridspec(1, 1)    

## fig 1: s11
ax = fig.add_subplot(gs[0])
ax.scatter(data_fn[:, 0], data_fn[:, 1] , c=data_fn[:, 7], cmap='viridis', s=100)
ax.set_title("s22")

fig_name = 'Results/result.png'
fig.savefig(fig_name)
plt.close()    
