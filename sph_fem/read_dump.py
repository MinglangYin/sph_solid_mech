import numpy as np
import matplotlib.pyplot as plt

# def CurveFit(x_data, y_data, x_new):
#     spl = UnivariateSpline(x_data, y_data)
#     spl.set_smoothing_factor(0.5)
#     y_new = spl(x_new)
#     return y_new

def read_sph_data(path, ii):
    # find ii particle in path
    with open(path, "r") as f:
        disp_y = []
        c_s2 = []
        for line in f:
            data = line.split(' ')
            if data[0] == str(ii):
                disp_y.append(np.float(data[3]))
                c_s2.append(np.float(data[9]))
        f.close()
    return np.asarray(disp_y), np.asarray(c_s2)

def read_sph_data_lin(path, ii):
    # find ii particle in path
    with open(path, "r") as f:
        strain_y = []
        c_s2 = []
        for line in f:
            data = line.split(' ')
            if data[0] == str(ii):
                strain_y.append(np.float(data[13]))
                c_s2.append(np.float(data[9]))
        f.close()
    return np.asarray(strain_y), np.asarray(c_s2)

if __name__ == "__main__":
    ii = 390
    strain_sph_lin, stress_sph_lin = read_sph_data_lin('./sph_data/dump_lin.LAMMPS', ii)
    disp_sph_nk, stress_sph_nk = read_sph_data('./sph_data/dump_nk.LAMMPS', ii)
    disp_sph_hgo_vert, stress_sph_hgo_vert = read_sph_data('./sph_data/dump_hgo_vert.LAMMPS', 400)
    disp_sph_hgo_hori, stress_sph_hgo_hori = read_sph_data('./sph_data/dump_hgo_hori.LAMMPS', 398)
    
    data_fem_lin = np.loadtxt("./fem_data/strain_stress_lin.txt")
    data_fem_nk = np.loadtxt("./fem_data/disp_stress_nk.txt")
    data_fem_hgo_vert = np.loadtxt("./fem_data/disp_stress_hgo_vert.txt")
    data_fem_hgo_hori = np.loadtxt("./fem_data/disp_stress_hgo_hori.txt")

    ### linear
    fig = plt.figure(constrained_layout=False, figsize=(4, 4))
    gs = fig.add_gridspec(1, 1)    

    ax = fig.add_subplot(gs[0])
    ax.plot( data_fem_lin[:, 0]+1, data_fem_lin[:, 1], linestyle = 'solid', color='red', linewidth=3, label='FEM')
    ax.scatter( strain_sph_lin[1::3]+1, stress_sph_lin[1::3], color='blue', label='SPH')

    ax.set_xlim([1.0, 1.1])
    ax.set_ylim([0, 0.15])
    ax.set_xlabel('Stretch')
    ax.set_ylabel('Nominal Stress')
    ax.legend()   
    plt.tight_layout()
    fig.savefig('./linear_clamp.png')
    plt.close()    

    ### neo-hookean
    fig = plt.figure(constrained_layout=False, figsize=(4, 4))
    gs = fig.add_gridspec(1, 1)    

    ax = fig.add_subplot(gs[0])
    ax.plot( data_fem_nk[:, 0]/20+1, data_fem_nk[:, 1], linestyle = 'solid', color='red', linewidth=3, label='FEM')
    ax.scatter( (disp_sph_nk[::10]-9)/20+1, stress_sph_nk[::10], color='blue', label='SPH')

    ax.set_xlim([1.0, 1.5])
    ax.set_ylim([0, 0.5])
    ax.set_xlabel('Strain')
    ax.set_ylabel('Nominal Stress')
    ax.legend()   
    plt.tight_layout()
    fig.savefig('./nk_clamp.png')
    plt.close()    

    ### neo-hookean
    fig = plt.figure(constrained_layout=False, figsize=(4, 4))
    gs = fig.add_gridspec(1, 1)    

    ax = fig.add_subplot(gs[0])
    ax.plot( data_fem_hgo_vert[:, 0]/20+1, data_fem_hgo_vert[:, 1], linestyle = 'solid', color='red', linewidth=3, label=r'FEM $\alpha=90^\circ$')
    ax.scatter( (disp_sph_hgo_vert[::25]-9)/20+1, stress_sph_hgo_vert[::25], color='blue', label=r'SPH $\alpha=90^\circ$')

    ax.plot( data_fem_hgo_hori[:, 0]/20+1, data_fem_hgo_hori[:, 1], linestyle = 'dashed', color='red', linewidth=3, label=r'FEM $\alpha=0^\circ$')
    ax.scatter( (disp_sph_hgo_hori[::10]-9)/20+1, stress_sph_hgo_hori[::10], color='blue', marker='^', label=r'SPH $\alpha=0^\circ$')

    ax.set_xlim([1.0, 1.5])
    ax.set_ylim([0, 12])
    ax.set_xlabel('Stretch')
    ax.set_ylabel('Nominal Stress')
    ax.legend()   
    plt.tight_layout()
    fig.savefig('./hgo_clamp.png')
    plt.close()    