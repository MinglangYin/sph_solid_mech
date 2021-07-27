import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import UnivariateSpline

# def CurveFit(x_data, y_data, x_new):
#     spl = UnivariateSpline(x_data, y_data)
#     spl.set_smoothing_factor(0.5)
#     y_new = spl(x_new)
#     return y_new

def main():
    data_lin_fem = np.loadtxt("./fem_data/strain_stress_lin.txt")
    data_nk_fem = np.loadtxt("./fem_data/strain_stress_nk.txt")

    data_lin_sph = np.loadtxt("./sph_data/stress_strain_lin.dat")
    data_nk_sph = np.loadtxt("./sph_data/stress_strain_nk.dat")

    ## Linear Model
    fig = plt.figure(constrained_layout=False, figsize=(4, 4))
    gs = fig.add_gridspec(1, 1)    

    x_plot = np.linspace(0, 0.1, 51)
    data_lin_fem_mean = data_lin_fem[:, 1:].mean(axis=1)

    ax = fig.add_subplot(gs[0])
    ax.plot(x_plot+1, x_plot*1.1, 'r',linewidth=3, label='Analytical')
    ax.scatter( (data_lin_sph[::10, 0]-19)/19+1, data_lin_sph[::10, 2], color='blue', label='SPH')
    ax.plot( data_lin_fem[:, 0]/19+1, data_lin_fem_mean, linestyle = 'dashed', color='black', linewidth=3, label='FEM')

    ax.set_xlim([1.0, 1.1])
    ax.set_ylim([0, 0.15])
    ax.set_xlabel('Stretch')
    ax.set_ylabel('Nominal Stress')
    ax.legend()   

    plt.tight_layout()
    fig.savefig('./lin_clamp.png')
    plt.close()    

    ## Neo-Hookean Model
    fig = plt.figure(constrained_layout=False, figsize=(4, 4))
    gs = fig.add_gridspec(1, 1)    

    data_nk_fem_mean = data_nk_fem[:, 1:].mean(axis=1)

    ax = fig.add_subplot(gs[0])
    ax.scatter( (data_nk_sph[::10, 1]-19), data_nk_sph[::10, 2], color='blue', label='SPH')
    ax.plot( (data_nk_sph_new[:, 1]-19), data_nk_sph_new[:, 2], color='red', label='SPH new')
    ax.plot( data_nk_fem[:, 0], data_nk_fem_mean, linestyle = 'dashed', color='black', linewidth=3, label='FEM')

    # ax.set_xlim([1.0, 1.1])
    # ax.set_ylim([0, 0.15])
    ax.set_xlabel('Stretch')
    ax.set_ylabel('Nominal Stress')
    ax.legend()   

    plt.tight_layout()
    fig.savefig('./nk_clamp.png')
    plt.close()    


    ## Neo-Hookean Model
    fig = plt.figure(constrained_layout=False, figsize=(4, 4))
    gs = fig.add_gridspec(1, 1)    

    data_nk_fem_mean = data_nk_fem[:, 1:].mean(axis=1)

    ax = fig.add_subplot(gs[0])
    ax.scatter( data_nk_sph[::10, 0], data_nk_sph[::10, 2], color='blue', label='SPH')

    # ax.plot( data_nk_fem[:, 0], data_nk_fem[:, 2], linestyle = 'dashed', color='black', linewidth=3, label='FEM')

    # ax.set_xlim([1.0, 1.1])
    # ax.set_ylim([0, 0.15])
    ax.set_xlabel('Stretch')
    ax.set_ylabel('Nominal Stress')
    ax.legend()   

    plt.tight_layout()
    fig.savefig('./nk_clamp2.png')
    plt.close()    

if __name__ == "__main__":
    main()
